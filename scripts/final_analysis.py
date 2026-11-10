"""Run Final Project analysis: K-Means, ICP scoring, baseline, and sensitivity."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"
FIG = ROOT / "figures"

COMP_COLS = [
    "komp_ukuran_pasar",
    "komp_kepadatan_sektor",
    "komp_kesiapan_digital",
    "komp_adopsi_digital",
    "komp_aktivitas_ekonomi",
]
COMP_LABELS = {
    "komp_ukuran_pasar": "Ukuran Pasar",
    "komp_kepadatan_sektor": "Kepadatan Sektor",
    "komp_kesiapan_digital": "Kesiapan Digital",
    "komp_adopsi_digital": "Adopsi Digital",
    "komp_aktivitas_ekonomi": "Aktivitas Ekonomi",
}
SECTOR_COLORS = {"Ritel": "#2c7a8c", "F&B": "#d98c3f", "Jasa": "#6c5b9e"}
BASE_WEIGHTS = {
    "ukuran": 0.25,
    "kepadatan": 0.25,
    "digital": 0.20,
    "adopsi": 0.15,
    "ekonomi": 0.15,
}

sns.set_theme(style="whitegrid", palette="deep", font_scale=0.9)
plt.rcParams["figure.dpi"] = 140
plt.rcParams["axes.titlesize"] = 11.5
plt.rcParams["axes.titleweight"] = "bold"


def fmt_int(value):
    return f"{value:,.0f}".replace(",", ".")


def fmt_dec(value, digits=2):
    return f"{value:.{digits}f}".replace(".", ",")


def minmax(series):
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(0.5, index=series.index)
    return (series - lo) / (hi - lo)


def score_segments(seg, weights):
    return (
        weights["ukuran"] * seg["ukuran_n"]
        + weights["kepadatan"] * seg["kepadatan_n"]
        + weights["digital"] * seg["komp_kesiapan_digital"]
        + weights["adopsi"] * seg["komp_adopsi_digital"]
        + weights["ekonomi"] * seg["komp_aktivitas_ekonomi"]
    )


def cluster_labels(profile):
    digital_top = profile["komp_kesiapan_digital"].idxmax()
    remaining = profile.drop(index=digital_top)
    market_top = remaining["komp_ukuran_pasar"].idxmax()
    low = remaining.drop(index=market_top).index[0]
    return {
        digital_top: "Hub Digital Matang",
        market_top: "Sentra Perdagangan Padat",
        low: "Wilayah Rintisan",
    }


def main():
    df = pd.read_csv(OUT / "master_final.csv")
    seg = pd.read_csv(OUT / "segments_final.csv")

    df = df.drop(
        columns=["klaster", "label_klaster", "jarak_ke_centroid", "pc1", "pc2"],
        errors="ignore",
    )
    seg = seg.drop(columns=["klaster", "label_klaster"], errors="ignore")

    X = df[COMP_COLS].to_numpy()
    eval_rows = []
    for k in range(2, 7):
        model = KMeans(n_clusters=k, random_state=42, n_init=50)
        labels = model.fit_predict(X)
        eval_rows.append(
            {
                "k": k,
                "inertia": model.inertia_,
                "silhouette": silhouette_score(X, labels),
            }
        )
    evaluation = pd.DataFrame(eval_rows)
    evaluation.to_csv(OUT / "kmeans_evaluation.csv", index=False)

    allowed = evaluation[evaluation["k"].between(3, 5)]
    best_k = int(allowed.loc[allowed["silhouette"].idxmax(), "k"])
    model = KMeans(n_clusters=best_k, random_state=42, n_init=50)
    df["klaster"] = model.fit_predict(X) + 1

    profile = df.groupby("klaster")[COMP_COLS].mean()
    profile["jumlah_wilayah"] = df.groupby("klaster").size()
    labels = cluster_labels(profile)
    df["label_klaster"] = df["klaster"].map(labels)
    profile["label_klaster"] = profile.index.map(labels)
    profile = profile[["label_klaster", "jumlah_wilayah"] + COMP_COLS]
    profile.to_csv(OUT / "cluster_profile.csv")

    df["jarak_ke_centroid"] = np.linalg.norm(
        X - model.cluster_centers_[df["klaster"] - 1], axis=1
    )

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    axes[0].plot(evaluation["k"], evaluation["inertia"], marker="o", color="#2c7a8c")
    axes[0].axvline(best_k, color="#d98c3f", linestyle="--", linewidth=1)
    axes[0].set_title("Elbow Method")
    axes[0].set_xlabel("Jumlah klaster (k)")
    axes[0].set_ylabel("Inertia / WCSS")
    axes[0].set_xticks(evaluation["k"])
    axes[1].plot(evaluation["k"], evaluation["silhouette"], marker="o", color="#6c5b9e")
    axes[1].axvline(best_k, color="#d98c3f", linestyle="--", linewidth=1)
    axes[1].set_title("Silhouette Analysis")
    axes[1].set_xlabel("Jumlah klaster (k)")
    axes[1].set_ylabel("Skor silhouette")
    axes[1].set_xticks(evaluation["k"])
    fig.suptitle("Pemilihan Jumlah Klaster Wilayah", fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIG / "final_elbow_silhouette.png", bbox_inches="tight")
    plt.close(fig)

    pca = PCA(n_components=2, random_state=42)
    pcs = pca.fit_transform(X)
    df["pc1"], df["pc2"] = pcs[:, 0], pcs[:, 1]
    fig, ax = plt.subplots(figsize=(9.2, 6.4))
    palette = sns.color_palette("Set2", n_colors=best_k)
    for i, label in enumerate(df["label_klaster"].unique(), start=0):
        sub = df[df["label_klaster"] == label]
        ax.scatter(
            sub["pc1"],
            sub["pc2"],
            s=55 + sub["komp_aktivitas_ekonomi"] * 90,
            color=palette[i],
            alpha=0.82,
            edgecolor="white",
            linewidth=0.7,
            label=label,
        )
        for _, row in sub.iterrows():
            ax.annotate(
                row["wilayah"].replace("Kabupaten ", "").replace("Kota ", "Kota "),
                (row["pc1"], row["pc2"]),
                xytext=(4, 3),
                textcoords="offset points",
                fontsize=6.4,
                color="#243447",
            )
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.0%} variasi)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.0%} variasi)")
    ax.set_title("Peta Klaster Wilayah Berdasarkan Lima Komponen ICP")
    ax.legend(title="Tipe wilayah", fontsize=8, title_fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "final_clusters_pca.png", bbox_inches="tight")
    plt.close(fig)

    heat = profile.set_index("label_klaster")[COMP_COLS].rename(columns=COMP_LABELS)
    fig, ax = plt.subplots(figsize=(9.2, 3.6))
    sns.heatmap(
        heat,
        annot=True,
        fmt=".2f",
        cmap="YlGnBu",
        vmin=0,
        vmax=1,
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "Rata-rata komponen (0-1)"},
        ax=ax,
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("Profil Rata-rata Komponen per Tipe Wilayah")
    fig.tight_layout()
    fig.savefig(FIG / "final_cluster_profile.png", bbox_inches="tight")
    plt.close(fig)

    seg = seg.merge(
        df[["kode_wilayah", "klaster", "label_klaster"]],
        on="kode_wilayah",
        how="left",
        validate="many_to_one",
    )

    top5 = seg.nsmallest(5, "peringkat").copy()
    top5["alasan"] = top5.apply(
        lambda r: (
            f"Volume {r['sektor']} {fmt_int(r['unit_sektor'])} usaha; "
            f"kepadatan {fmt_int(r['kepadatan_sektor'])}/100k; "
            f"IPM {fmt_dec(r['ipm'], 1)}; "
            f"PDRB Rp{fmt_dec(r['pdrb_per_kapita_2024'] / 1000, 1)} juta/kapita; "
            f"{r['label_klaster']}."
        ),
        axis=1,
    )
    top5_out = top5[
        [
            "peringkat",
            "sektor",
            "wilayah",
            "skor_icp",
            "unit_sektor",
            "kepadatan_sektor",
            "label_klaster",
            "alasan",
        ]
    ].rename(
        columns={
            "peringkat": "Peringkat",
            "sektor": "Sektor",
            "wilayah": "Wilayah",
            "skor_icp": "Skor Prioritas",
            "unit_sektor": "Estimasi Jumlah UMKM",
            "kepadatan_sektor": "Kepadatan per 100k",
            "label_klaster": "Tipe Wilayah",
            "alasan": "Alasan",
        }
    )
    top5_out.to_csv(OUT / "top5_segments.csv", index=False)

    fig, ax = plt.subplots(figsize=(9.2, 4.4))
    plot_top = top5.sort_values("skor_icp")
    labels_bar = [f"{r.sektor} - {r.wilayah}" for r in plot_top.itertuples()]
    colors = [SECTOR_COLORS[s] for s in plot_top["sektor"]]
    bars = ax.barh(labels_bar, plot_top["skor_icp"], color=colors, height=0.62)
    for bar, value in zip(bars, plot_top["skor_icp"]):
        ax.text(
            value + 0.008,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.3f}",
            va="center",
            fontsize=8.5,
        )
    ax.set_xlim(0, max(plot_top["skor_icp"]) + 0.08)
    ax.set_xlabel("Skor prioritas ICP (0-1)")
    ax.set_title("Top 5 Segmen Target Klay")
    ax.tick_params(axis="y", labelsize=8.5)
    fig.tight_layout()
    fig.savefig(FIG / "final_top5_segments.png", bbox_inches="tight")
    plt.close(fig)

    seg["baseline_rank"] = seg["unit_sektor"].rank(ascending=False, method="min").astype(int)
    base_top = seg.nsmallest(5, "baseline_rank")
    overlap = len(set(top5["sektor"] + "|" + top5["wilayah"]) & set(base_top["sektor"] + "|" + base_top["wilayah"]))
    rho = spearmanr(seg["skor_icp"], seg["unit_sektor"]).statistic

    baseline_rows = []
    for i in range(5):
        icp = top5.iloc[i]
        base = base_top.iloc[i]
        baseline_rows.append(
            {
                "Peringkat": i + 1,
                "ICP_Sektor": icp["sektor"],
                "ICP_Wilayah": icp["wilayah"],
                "ICP_Skor": round(icp["skor_icp"], 3),
                "Baseline_Sektor": base["sektor"],
                "Baseline_Wilayah": base["wilayah"],
                "Baseline_Unit": int(base["unit_sektor"]),
            }
        )
    baseline_table = pd.DataFrame(baseline_rows)
    baseline_table.to_csv(OUT / "baseline_comparison.csv", index=False)

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    ax.scatter(
        seg["baseline_rank"],
        seg["peringkat"],
        s=28,
        alpha=0.55,
        color="#8ea6b8",
        edgecolor="white",
        linewidth=0.5,
    )
    highlight = seg[seg["peringkat"] <= 5]
    ax.scatter(
        highlight["baseline_rank"],
        highlight["peringkat"],
        s=70,
        color="#d98c3f",
        edgecolor="white",
        linewidth=0.7,
    )
    ax.plot([1, len(seg)], [1, len(seg)], color="#203a5e", linestyle="--", linewidth=1)
    ax.set_xlabel("Peringkat baseline (jumlah unit sektor)")
    ax.set_ylabel("Peringkat skor ICP")
    ax.set_title("Skor ICP vs Baseline: Peringkat Segmen")
    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.text(
        0.98,
        0.04,
        f"Overlap Top 5 = {overlap}/5\nSpearman ρ = {rho:.2f}",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#ccd6df"},
    )
    fig.tight_layout()
    fig.savefig(FIG / "final_baseline.png", bbox_inches="tight")
    plt.close(fig)

    scenarios = {
        "Base": BASE_WEIGHTS,
        "Adopsi +5": {**BASE_WEIGHTS, "ukuran": 0.20, "adopsi": 0.20},
        "Adopsi -5": {**BASE_WEIGHTS, "ukuran": 0.30, "adopsi": 0.10},
        "PDRB +5": {**BASE_WEIGHTS, "kepadatan": 0.20, "ekonomi": 0.20},
        "PDRB -5": {**BASE_WEIGHTS, "kepadatan": 0.30, "ekonomi": 0.10},
        "Digital +10": {**BASE_WEIGHTS, "ukuran": 0.15, "digital": 0.30},
        "Digital -10": {**BASE_WEIGHTS, "ukuran": 0.35, "digital": 0.10},
    }

    base_scores = seg["skor_icp"].copy()
    base_rank = base_scores.rank(ascending=False, method="min")
    base_set = set(top5["sektor"] + "|" + top5["wilayah"])
    sens_rows = []
    for name, weights in scenarios.items():
        scores = score_segments(seg, weights)
        ranks = scores.rank(ascending=False, method="min")
        chosen = seg.assign(_score=scores, _rank=ranks).nsmallest(5, "_rank")
        chosen_set = set(chosen["sektor"] + "|" + chosen["wilayah"])
        change = int((ranks != base_rank).sum())
        sens_rows.append(
            {
                "Skenario": name,
                "Overlap_Top5": len(base_set & chosen_set),
                "Spearman_vs_Base": round(spearmanr(base_scores, scores).statistic, 3),
                "Segmen_Berubah_Peringkat": change,
            }
        )
    sensitivity = pd.DataFrame(sens_rows)
    sensitivity.to_csv(OUT / "sensitivity_scenarios.csv", index=False)

    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    colors = ["#2c7a8c" if x == 5 else "#d98c3f" for x in sensitivity["Overlap_Top5"]]
    bars = ax.barh(sensitivity["Skenario"], sensitivity["Overlap_Top5"], color=colors)
    for bar, overlap_value, rho_value in zip(
        bars, sensitivity["Overlap_Top5"], sensitivity["Spearman_vs_Base"]
    ):
        ax.text(
            overlap_value + 0.08,
            bar.get_y() + bar.get_height() / 2,
            f"{overlap_value}/5 (ρ={rho_value:.3f})",
            va="center",
            fontsize=8,
        )
    ax.set_xlim(0, 5.8)
    ax.set_xlabel("Jumlah segmen Top 5 yang tetap")
    ax.set_title("Uji Sensitivitas Bobot ICP")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(FIG / "final_sensitivity.png", bbox_inches="tight")
    plt.close(fig)

    cluster_summary = (
        seg.groupby(["klaster", "label_klaster"])
        .agg(
            jumlah_segmen=("sektor", "size"),
            rata_skor=("skor_icp", "mean"),
            skor_maks=("skor_icp", "max"),
            segmen_teratas=("skor_icp", lambda s: seg.loc[s.idxmax(), "sektor"] + " - " + seg.loc[s.idxmax(), "wilayah"]),
        )
        .reset_index()
        .sort_values("rata_skor", ascending=False)
    )
    cluster_summary.round(3).to_csv(OUT / "cluster_score_summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(8.2, 4.0))
    sns.boxplot(
        data=seg,
        x="label_klaster",
        y="skor_icp",
        color="#9fc5d3",
        width=0.5,
        ax=ax,
    )
    sns.stripplot(
        data=seg,
        x="label_klaster",
        y="skor_icp",
        color="#203a5e",
        size=3,
        alpha=0.55,
        ax=ax,
    )
    ax.set_xlabel("")
    ax.set_ylabel("Skor prioritas segmen")
    ax.set_title("Sebaran Skor Segmen per Tipe Wilayah")
    ax.tick_params(axis="x", rotation=8)
    fig.tight_layout()
    fig.savefig(FIG / "final_cluster_score.png", bbox_inches="tight")
    plt.close(fig)

    df.to_csv(OUT / "master_final.csv", index=False)
    seg.to_csv(OUT / "segments_final.csv", index=False)

    print(f"k optimal: {best_k}")
    print(evaluation.to_string(index=False))
    print("\nCluster profile:")
    print(profile.round(3).to_string(index=False))
    print("\nTop 5:")
    print(top5_out.to_string(index=False))
    print(f"\nBaseline overlap: {overlap}/5; Spearman rho: {rho:.3f}")
    print("\nSensitivity:")
    print(sensitivity.to_string(index=False))


if __name__ == "__main__":
    main()
