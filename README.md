# Merger Simulation & Market Concentration Analyzer

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, quantitative antitrust toolkit designed for competition economists, pricing strategists, and regulatory analysts. This package automates the calculation of the Herfindahl-Hirschman Index (HHI), flags regulatory risks, and simulates the market impact of corporate mergers.

## Core Capabilities

* **Rigorous Econometrics:** Instantly calculates Pre-Merger HHI, Post-Merger HHI, and $\Delta$ HHI based on U.S. DOJ and FTC Horizontal Merger Guidelines.
* **Enterprise Data Pipelines:** Natively integrates with **Google BigQuery** to run simulations directly against cloud data warehouses via standard SQL.
* **Boardroom-Ready Visuals:** Generates executive-grade terminal UI reports (via `Rich`) and exports publication-ready statistical charts (via `Matplotlib` & `Seaborn`).
* **High-Performance Architecture:** Built with modern Python tooling (`uv`, `typer`, `ruff`, `pytest`) for maximum execution speed and reliability.

## Installation

This project utilizes `uv` for lightning-fast dependency management.

```bash
# Clone the repository
git clone [https://github.com/thanhan25/merger-simulation-hhi-analyzer.git](https://github.com/thanhan25/merger-simulation-hhi-analyzer.git)
cd merger-simulation-hhi-analyzer

# Install the project and its dependencies
uv sync --all-extras
```
