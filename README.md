# VALE_CASE — Iron Ore Drill Hole Data Analysis

Exploratory analysis, data treatment, and block model estimation for the **Vale Desenvolver** iron ore deposit using Python.

## Project Overview

This project demonstrates a complete geochemical data analysis pipeline for mineral resource evaluation:

1. **Exploratory Data Analysis** — Statistical profiling, distribution analysis, and data quality assessment of drill hole assays
2. **Data Treatment** — Sentinel value replacement, coordinate correction, 3D sample positioning via direction cosines
3. **Block Model Estimation** — Length-weighted grade averaging and product classification (Lump Ore, Sinter Feed, Pellet Feed)

## Repository Structure

```
VALE_CASE/
├── data/
│   ├── collar.csv                 # Drill hole collar coordinates (365 holes)
│   ├── assays.csv                 # Geochemical assay intervals (5,487 samples)
│   └── block_model.csv           # Pre-existing block model grid (2,594 blocks)
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_data_treatment.ipynb
│   └── 03_block_model_estimation.ipynb
├── requirements.txt
└── README.md
```

## Datasets

| File | Records | Description |
|------|---------|-------------|
| `collar.csv` | 365 | Drill hole collar positions (Easting, Northing, Elevation, Depth) |
| `assays.csv` | 5,487 | Downhole geochemical intervals (Fe, SiO2, G1, G2, G3, Lithotype) |
| `block_model.csv` | 2,594 | Regular 50x50x25m block grid with lithotype classification |

## Methodology

### Data Treatment
- **Sentinel replacement:** `-99` values converted to `NaN` for proper statistical handling
- **Coordinate correction:** Detected and fixed rows with swapped X/Y UTM coordinates
- **3D positioning:** Computed sample midpoint coordinates using azimuth/dip direction cosines

### Block Model Estimation
- **Grid assignment:** Samples mapped to blocks via integer grid indices `(i, j, k)`
- **Weighted averaging:** Length-weighted mean grades computed per block
- **Product classification:** Blocks classified into ore products based on Fe, SiO2, and granulometry thresholds

## Tech Stack

- **Python 3.11+**
- **pandas** — Data manipulation and analysis
- **NumPy** — Numerical computation and vector operations
- **Matplotlib / Seaborn** — Data visualization
- **Jupyter** — Interactive notebook environment

## How to Run

```bash
# Clone the repository
git clone https://github.com/murilomn58/VALE_CASE.git
cd VALE_CASE

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook notebooks/
```

## Author

**Murilo Narciso**
