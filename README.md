# Data Analytics Dashboard

[![Python Tests](https://github.com/Zolnoi/data-dashboard/actions/workflows/tests.yml/badge.svg)](https://github.com/Zolnoi/data-dashboard/actions/workflows/tests.yml)

A Streamlit-based dashboard for exploring and analyzing time-series data. Upload CSV files, pick a datetime column, and use the built-in tabs for trend analysis, correlation, distributions, anomaly detection, and visual exploration. The app is generalized to work with any time-series dataset.

**Data requirement:** Your CSV must have at least one column of type datetime (used for time-based resampling and trend charts). Name it in the sidebar when loading (e.g. `timestamp`).

## Features

- **CSV upload**: Load one or more CSV datasets with a chosen timestamp column; nulls are handled automatically.
- **Raw Data**: View loaded tables in the app.
- **Trend**: Time-series plots with resampling and optional rolling average.
- **Correlation**: Scatter plots and correlation heatmaps between numeric columns.
- **Distribution**: Histograms, KDE, and box plots for numeric columns.
- **Anomaly detection**: IQR, LOESS, or Isolation Forest to flag outliers in series.
- **Explore**: Interactive visual exploration with PyGWalker (when installed).

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Installation

1. Clone the repository.
2. Create a virtual environment and install dependencies with uv:
   ```bash
   uv sync
   ```
   This creates `.venv` (if needed), installs the Python version from `.python-version`, and installs all dependencies from `pyproject.toml` using `uv.lock`.
3. Activate the environment (optional; `uv run` uses it automatically):
   ```bash
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```
## Usage

1. Start the Streamlit app:
   ```bash
   uv run streamlit run dashboard.py
   ```
   Or with the venv activated: `streamlit run dashboard.py`

2. In the sidebar:
   - Enter a **Dataset name** and **upload a CSV file**.
   - Set the **Timestamp column name** to the column that holds datetime values (e.g. `timestamp`). Your CSV must have at least one datetime column for trend and time-based views.
   - Click **Submit** to load the data.

3. Select the loaded dataset from the sidebar, then use the tabs:
   - **Raw Data**: Browse the table.
   - **Trend**: Time-series charts with resampling and rolling average.
   - **Correlation**: Scatter or heatmap of numeric columns.
   - **Distribution**: Histogram, KDE, or box plot for numeric columns.
   - **Anomaly**: Run IQR, LOESS, or Isolation Forest on selected series.
   - **Explore**: Use PyGWalker for ad-hoc visual exploration (if installed).

## Contributing

We welcome contributions from the community. If you’re looking for new features or have found a bug:

- **Bug reports and feature requests:** please [open an issue](https://github.com/SivamPillai/dataved/issues).
- **Code changes:** please open a Pull Request. Fork the repo, create a branch, make your changes, and submit a PR.

## License

This project is released under the **MIT License**. It was built for internal data analysis at [Zolnoi](https://zolnoi.com) and is now open sourced for broader community use. See [LICENSE](LICENSE) for the full text. Credit to **Zolnoi** for the original development and release.
