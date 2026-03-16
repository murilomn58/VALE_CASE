"""Generate visual outputs for the VALE_CASE repository README."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 150

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# --- Load data ---
collar = pd.read_csv(os.path.join(DATA_DIR, "collar.csv"))
assays = pd.read_csv(os.path.join(DATA_DIR, "assays.csv"))
block_model = pd.read_csv(os.path.join(DATA_DIR, "block_model.csv"))

geochem_cols = ["FE", "SI", "G1", "G2", "G3"]

# Fix swapped coordinates
collar_plot = collar.copy()
mask = collar_plot["X"] > 1_000_000
collar_plot.loc[mask, ["X", "Y"]] = collar_plot.loc[mask, ["Y", "X"]].values

# Clean sentinel values
assays_clean = assays.copy()
for col in geochem_cols:
    assays_clean[col] = assays_clean[col].replace(-99, np.nan)

# ============================================================
# PLOT 1: Drill Hole Map + Depth Distribution
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].scatter(collar_plot["X"], collar_plot["Y"], s=15, c="steelblue", edgecolors="k", linewidths=0.3)
axes[0].set_xlabel("Easting (m)", fontsize=11)
axes[0].set_ylabel("Northing (m)", fontsize=11)
axes[0].set_title("Drill Hole Collar Locations — Plan View", fontsize=13, fontweight="bold")
axes[0].ticklabel_format(style="plain")

axes[1].hist(collar_plot["PROF"], bins=30, color="steelblue", edgecolor="white")
axes[1].set_xlabel("Total Depth (m)", fontsize=11)
axes[1].set_ylabel("Number of Drill Holes", fontsize=11)
axes[1].set_title("Distribution of Drill Hole Depths", fontsize=13, fontweight="bold")

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "01_drillhole_map.png"), bbox_inches="tight", facecolor="white")
plt.close()
print("01_drillhole_map.png OK")

# ============================================================
# PLOT 2: Fe and SiO2 Distributions
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

fe_data = assays_clean["FE"].dropna()
axes[0].hist(fe_data, bins=40, color="#c0392b", edgecolor="white", alpha=0.85)
axes[0].axvline(fe_data.mean(), color="black", linestyle="--", linewidth=1.5, label=f"Mean = {fe_data.mean():.1f}%")
axes[0].set_xlabel("Fe (%)", fontsize=11)
axes[0].set_ylabel("Frequency", fontsize=11)
axes[0].set_title("Iron (Fe) Grade Distribution", fontsize=13, fontweight="bold")
axes[0].legend(fontsize=10)

si_data = assays_clean["SI"].dropna()
axes[1].hist(si_data, bins=40, color="#2980b9", edgecolor="white", alpha=0.85)
axes[1].axvline(si_data.mean(), color="black", linestyle="--", linewidth=1.5, label=f"Mean = {si_data.mean():.1f}%")
axes[1].set_xlabel("SiO\u2082 (%)", fontsize=11)
axes[1].set_ylabel("Frequency", fontsize=11)
axes[1].set_title("Silica (SiO\u2082) Grade Distribution", fontsize=13, fontweight="bold")
axes[1].legend(fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "02_fe_si_distributions.png"), bbox_inches="tight", facecolor="white")
plt.close()
print("02_fe_si_distributions.png OK")

# ============================================================
# PLOT 3: Fe vs SiO2 Scatter Plot
# ============================================================
valid = assays_clean.dropna(subset=["FE", "SI"])

fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(valid["FE"], valid["SI"], c=valid["FE"], cmap="RdYlGn", s=8, alpha=0.6, edgecolors="none")
ax.set_xlabel("Fe (%)", fontsize=12)
ax.set_ylabel("SiO\u2082 (%)", fontsize=12)
corr = valid["FE"].corr(valid["SI"])
ax.set_title(f"Fe vs SiO\u2082 — Inverse Correlation (r = {corr:.3f})", fontsize=14, fontweight="bold")
plt.colorbar(scatter, ax=ax, label="Fe (%)")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "03_fe_vs_si_scatter.png"), bbox_inches="tight", facecolor="white")
plt.close()
print("03_fe_vs_si_scatter.png OK")

# ============================================================
# PLOT 4: Correlation Matrix
# ============================================================
corr_matrix = assays_clean[geochem_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
mask_tri = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask_tri, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, square=True, linewidths=1, ax=ax, vmin=-1, vmax=1,
            annot_kws={"size": 12})
ax.set_title("Correlation Matrix — Geochemical Variables", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "04_correlation_matrix.png"), bbox_inches="tight", facecolor="white")
plt.close()
print("04_correlation_matrix.png OK")

# ============================================================
# PLOT 5: Fe by Lithotype Boxplot
# ============================================================
lito_order = assays_clean.groupby("Lito_Final")["FE"].median().sort_values(ascending=False).index

fig, ax = plt.subplots(figsize=(14, 6))
sns.boxplot(data=assays_clean, x="Lito_Final", y="FE", order=lito_order, ax=ax,
            palette="RdYlGn", fliersize=2)
ax.axhline(y=56, color="red", linestyle="--", linewidth=1, label="Cutoff Fe = 56%")
ax.set_xlabel("Lithotype", fontsize=11)
ax.set_ylabel("Fe (%)", fontsize=11)
ax.set_title("Fe Grade Distribution by Lithotype", fontsize=13, fontweight="bold")
ax.legend(fontsize=10)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "05_fe_by_lithotype.png"), bbox_inches="tight", facecolor="white")
plt.close()
print("05_fe_by_lithotype.png OK")

# ============================================================
# PLOT 6: Lithotype Bar Chart
# ============================================================
lito_counts = assays["Lito_Final"].value_counts()

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(lito_counts.index, lito_counts.values, color="steelblue", edgecolor="white")
ax.set_xlabel("Lithotype", fontsize=11)
ax.set_ylabel("Sample Count", fontsize=11)
ax.set_title("Lithotype Distribution in Assay Database", fontsize=13, fontweight="bold")
ax.bar_label(bars, fontsize=9)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "06_lithotype_distribution.png"), bbox_inches="tight", facecolor="white")
plt.close()
print("06_lithotype_distribution.png OK")

# ============================================================
# PLOT 7: Granulometry Distributions
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
granulometry = {"G1 (Coarse)": "G1", "G2 (Medium)": "G2", "G3 (Fine)": "G3"}
colors = ["#27ae60", "#f39c12", "#8e44ad"]

for ax, (label, col), color in zip(axes, granulometry.items(), colors):
    data = assays_clean[col].dropna()
    if len(data) > 0:
        ax.hist(data, bins=30, color=color, edgecolor="white", alpha=0.85)
        ax.axvline(data.mean(), color="black", linestyle="--", linewidth=1.5, label=f"Mean = {data.mean():.1f}%")
        ax.set_xlabel(f"{label} (%)", fontsize=11)
        ax.set_ylabel("Frequency", fontsize=11)
        ax.set_title(f"{label} Distribution", fontsize=13, fontweight="bold")
        ax.legend(fontsize=10)
    else:
        ax.set_title(f"{label} — No valid data")

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "07_granulometry.png"), bbox_inches="tight", facecolor="white")
plt.close()
print("07_granulometry.png OK")

# ============================================================
# PLOT 8: Block Model Plan View (colored by lithotype)
# ============================================================
lito_colors = {lito: plt.cm.Set2(i / max(len(block_model["LITOTIPO"].unique()) - 1, 1))
               for i, lito in enumerate(sorted(block_model["LITOTIPO"].unique()))}

fig, ax = plt.subplots(figsize=(12, 8))
for lito, group in block_model.groupby("LITOTIPO"):
    ax.scatter(group["X"], group["Y"], s=12, label=lito, alpha=0.7,
               color=lito_colors[lito], edgecolors="none")
ax.set_xlabel("Easting (m)", fontsize=11)
ax.set_ylabel("Northing (m)", fontsize=11)
ax.set_title("Block Model — Plan View by Lithotype", fontsize=13, fontweight="bold")
ax.legend(title="Lithotype", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=9)
ax.ticklabel_format(style="plain")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "08_block_model_plan.png"), bbox_inches="tight", facecolor="white")
plt.close()
print("08_block_model_plan.png OK")

print("\nAll outputs generated successfully!")
