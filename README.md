
# Merger Simulation & Market Concentration Analyzer

[![CI/CD Pipeline](https://github.com/thanhan25/merger-simulation-hhi-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/thanhan25/merger-simulation-hhi-analyzer/actions/workflows/ci.yml)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

An enterprise-grade quantitative antitrust toolkit engineered for competition economists, pricing strategists, and regulatory analysts. This package automates the calculation of the Herfindahl-Hirschman Index (HHI), flags regulatory risks, and simulates the market impact of corporate mergers under the joint U.S. DOJ and FTC Horizontal Merger Guidelines.

## 📊 Core Architecture & Capabilities

* **Interactive Streamlit Dashboard:** A localized web interface for real-time scenario modeling, drag-and-drop CSV ingestion, and dynamic market concentration visualization via Plotly.
* **Institutional Data Pipelines:** Natively integrates with Google Cloud BigQuery, allowing users to execute simulations directly against cloud data warehouses using standard SQL queries, bypassing local memory limits.
* **Rigorous Econometrics Engine:** Calculates precise Pre-Merger, Post-Merger, and $\Delta$ metrics, mapping outputs directly to actionable regulatory risk tiers (Safe Harbor, Moderate Risk, High Risk).
* **Historical Case Studies:** Includes executable Jupyter notebooks analyzing landmark blocked mergers (e.g., AT&T and T-Mobile).

## 🧮 Mathematical Methodology (HHI)

The Herfindahl-Hirschman Index is calculated by squaring the market share of each firm competing in the market and then summing the resulting numbers.

$HHI = \sum_{i=1}^{N} s_i^2$

Where $s_i$ is the market share of firm $i$, and $N$ is the total number of firms. The index ranges from near zero (perfect competition) to 10,000 (a pure monopoly).

**Regulatory Thresholds (DOJ & FTC Guidelines):**

* **Unconcentrated Markets:** HHI below 1,500.
* **Moderately Concentrated:** HHI between 1,500 and 2,500.
* **Highly Concentrated:** HHI above 2,500. (Mergers producing a $\Delta$ HHI > 200 in this tier are presumed likely to enhance market power).

For detailed methodological breakdown and examples, refer to the `docs/` directory.

## ⚙️ Installation & Setup

This repository requires Python 3.13+ and utilizes [uv](https://github.com/astral-sh/uv) for high-speed environment management.

```bash
# Clone the repository
git clone [https://github.com/thanhan25/merger-simulation-hhi-analyzer.git](https://github.com/thanhan25/merger-simulation-hhi-analyzer.git)
cd merger-simulation-hhi-analyzer

# Sync dependencies and install the project in isolated virtual environment
uv sync --all-extras
```

## 🚀 Usage Guide

### 1. The Interactive Web Dashboard (Recommended)

Launch the Streamlit interface for visual scenario modeling:

```bash
# Windows
.\scripts\run_app.ps1

# Linux/Mac
./scripts/run_app.sh

# Or directly via uv
uv run merger-sim ui
```

### 2. The Command Line Interface (CLI)

For automated workflows and rapid terminal analysis, utilize the `analyze` command.

**Option A: Local CSV Analysis**
Target historical or proprietary local data.

```bash
uv run merger-sim analyze "T-Mobile" "Sprint" --file data/raw/telecom_market_2019.csv
```

**Option B: Enterprise BigQuery Execution**
Execute standard SQL against Google Cloud infrastructure. *(Requires Google Cloud Authentication)*.

```bash
uv run merger-sim analyze "AT&T" "Verizon" --query "SELECT firm, revenue FROM \`merger-sim-project.markets.telecom_2026\`"
```

**Option C: Rapid Prototyping**
Generate synthesized mock data to validate the mathematical engine instantly.

```bash
uv run merger-sim analyze "Firm B" "Firm C" --mock
```

## 📂 Repository Structure

```text
merger-simulation-market-concentration-analyzer/
├── .github/workflows/       # CI/CD pipelines (Pytest & Release automations)
├── docs/                    # Econometric methodology and execution examples
├── notebooks/               # Jupyter case studies (e.g., AT&T + T-Mobile simulation)
├── scripts/                 # Cross-platform deployment scripts (run_app.ps1, run_app.sh)
├── src/merger_sim/          # Core package source code
│   ├── app.py               # Streamlit web frontend
│   ├── cli.py               # Typer command-line routing
│   ├── io.py                # CSV and BigQuery ingestion pipelines
│   ├── metrics.py           # Mathematical logic and HHI functions
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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
