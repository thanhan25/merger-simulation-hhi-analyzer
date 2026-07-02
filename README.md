# 📉 Merger Simulation & Market Concentration Analyzer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black/ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![CI Pipeline](https://github.com/thanhan25/merger-simulation-hhi-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/thanhan25/merger-simulation-hhi-analyzer/actions)

An enterprise-grade, quantitative antitrust toolkit designed to calculate market concentration metrics and simulate the competitive effects of hypothetical corporate mergers.

Built for competition economists, antitrust regulatory analysts, and corporate strategy teams to rapidly model M&A scenarios.

## ✨ Features

* **Regulatory Compliance:** Algorithms mapped directly to DOJ/FTC and EU Commission antitrust thresholds.
* **Causal HHI $\Delta$ Modeling:** Instantly isolates the mathematical market shift caused by a merger.
* **Executive Visualization:** Automatically generates publication-ready seaborn/matplotlib charts.
* **Dual Interface:** Accessible via a beautiful, interactive CLI (`Typer`/`Rich`) or as a Python API for Jupyter Notebooks.
* **Modern DevOps Stack:** Fully typed, tested with `pytest`, and managed via `uv`.

## 📖 Methodology: The Herfindahl-Hirschman Index (HHI)

This toolkit evaluates market concentration utilizing the **HHI**, calculated by squaring the market share of each firm competing in a market and summing the results:

$$
HHI = \sum_{i=1}^{N} s_i^2
$$

The simulation engine classifies post-merger markets into regulatory risk categories:

* **Unconcentrated:** HHI < 1500
* **Moderately Concentrated:** HHI between 1500 and 2500
* **Highly Concentrated:** HHI > 2500 (Triggers Antitrust Scrutiny)

## 🚀 Installation

We use `uv` for blazing-fast dependency management.

```bash
git clone [https://github.com/thanhan25/merger-simulation-hhi-analyzer.git](https://github.com/thanhan25/merger-simulation-hhi-analyzer.git)
cd merger-simulation-hhi-analyzer
make install
```

## 💻 Usage

1. Command Line Interface (CLI)
   Run rapid simulations directly from your terminal using mock data or CSVs.

```bash
uv run merger-sim analyze "Firm B" "Firm C" --mock
```

### Output:
╭──────────────────────────────────────────────────╮
│ Merger Simulation: Firm B + Firm C               │
╰──────────────────────────────────────────────────╯
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric              ┃ Value                                            ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Pre-Merger HHI      │ 2263.0                                           │
│ Post-Merger HHI     │ 3013.0                                           │
│ HHI Delta (Δ)       │ +750.0                                           │
│ Concentration Level │ Highly Concentrated                              │
│ Regulatory Risk     │ High Risk: Presumed to enhance market power      │
└─────────────────────┴──────────────────────────────────────────────────┘
(A high-resolution comparison chart is automatically saved to output/figures/).

2. Python API (For Jupyter Notebooks)
Import the toolkit into your own economic research pipelines.
```Python
import pandas as pd
from merger_sim import simulate_merger, plot_merger_impact

# Load your market dataset
df = pd.read_csv("data/raw/telecom_market.csv")

# Simulate a merger between T-Mobile and Sprint
results = simulate_merger(df, firm_col="Firm", share_col="Market_Share", acquirer="T-Mobile", target="Sprint")

print(f"HHI Change: +{results['delta']}")
plot_merger_impact(results, output_path="output/tmobile_sprint_impact.png")
```

## 🤝 Contributing
Contributions are highly encouraged. Please run make test and make lint before submitting a Pull Request. See CONTRIBUTING.md for more details.
