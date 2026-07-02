
# Merger Simulation & Market Concentration Analyzer

[![CI/CD Pipeline](https://github.com/thanhan25/merger-simulation-hhi-analyzer/actions/workflows/ci.yml/badge.svg)](#)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A Python library and interactive dashboard for HHI market concentration measurement and merger impact simulation, featuring native Google Cloud BigQuery integration.

![Dashboard Preview](assets/dashboard-preview.PNG)

## 🧮 Econometric Methodology

This toolkit mathematically enforces the joint antitrust frameworks established by the U.S. Department of Justice (DOJ) and the Federal Trade Commission (FTC).

The core metric is the **Herfindahl-Hirschman Index (HHI)**, calculated by squaring the market share of each firm competing in the market and summing the results:

$$
HHI = \sum_{i=1}^{N} s_i^2
$$

Where $s_i$ is the market share of firm $i$, and $N$ is the total number of firms. The index ranges from near zero (perfect competition) to 10,000 (a pure monopoly).

### Regulatory Risk Thresholds (2023 Guidelines)

The simulator evaluates antitrust risk based on the post-merger concentration and the resulting $\Delta$ HHI:

* **Unconcentrated Markets ($HHI < 1500$):** Safe harbor; mergers rarely require further analysis.
* **Moderately Concentrated ($1500 \le HHI \le 2500$):** Mergers producing a $\Delta HHI > 100$ warrant significant scrutiny and Phase II investigations.
* **Highly Concentrated ($HHI > 2500$):** Mergers producing a $\Delta HHI > 100$ are presumed to enhance market power. A $\Delta HHI > 200$ triggers strict regulatory blocks and necessitates asset divestitures.

*(Note: Alternative jurisdictional thresholds for the EU Commission and Bundeskartellamt are detailed in `docs/jurisdictions.md`).*

## 🚀 Quickstart & Installation

Competition economists and data scientists repeatedly reimplement HHI calculations for each project. `merger-sim` provides a standard, strongly-typed (`Pydantic`) implementation so you can focus on policy rather than pipeline plumbing.

**1. Install via `uv` (Recommended)**

```bash
# Install everything (UI + BigQuery + Data Science Notebooks)
uv sync --all-extras
```

**2. Launch the Web Dashboard**

```bash
uv run merger-sim ui
```

## 💻 CLI Usage Guide

For automated workflows and headless data pipelines, utilize the CLI wrapper.

**Option A: Local CSV Analysis**

```bash
uv run merger-sim analyze "T-Mobile" "Sprint" --file data/raw/telecom_market_2019.csv
```

**Option B: Enterprise BigQuery Execution**
Execute standard SQL against Google Cloud infrastructure to bypass local memory limits.

```bash
uv run merger-sim analyze "AT&T" "Verizon" --query "SELECT firm, revenue FROM \`merger-sim-project.markets.telecom_2026\`"
```

**Option C: Headless Data Export**
Export typed `MergerScenario` models directly to JSON for downstream integration.

```bash
uv run merger-sim analyze "Firm B" "Firm C" --mock --output-json results.json --no-plots
```

## 📂 Repository Structure

```text
merger-simulation-market-concentration-analyzer/
├── .github/workflows/       # CI/CD pipelines (Pytest & Release automations)
├── docs/                    # Methodological deep-dives and execution examples
├── notebooks/               # Jupyter case studies (e.g., AT&T + T-Mobile simulation)
├── scripts/                 # Cross-platform deployment scripts
├── src/merger_sim/          # Core package source code
│   ├── app.py               # Streamlit web frontend
│   ├── cli.py               # Typer command-line routing
│   ├── io.py                # CSV and BigQuery ingestion pipelines
│   ├── metrics.py           # Mathematical logic and HHI functions
│   ├── models.py            # Strict Pydantic data validation structures
│   ├── plotting.py          # Matplotlib/Seaborn static chart generation
│   └── simulation.py        # Merger scenario execution engine
├── tests/                   # Pytest suite validating mathematical precision
├── pyproject.toml           # Project metadata and dependency configuration
└── README.md                # Technical documentation
```

## 🤝 Contributing

Contributions are welcome. Please ensure all modifications pass the standard linting and test suites before submitting a Pull Request.

```bash
uv run pytest tests/ -v
uv run ruff check src/ tests/
```

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
