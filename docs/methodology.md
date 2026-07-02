# Methodology: HHI and Merger Simulation

This document explains how the toolkit computes market concentration, simulates mergers, and maps results to qualitative risk labels. It is intended for competition economists, data scientists, and regulators who want to understand exactly what the code does.

---

## Market Shares and Normalization

The engine expects market shares expressed as percentages that sum to approximately 100.

- Input shares are taken from the `Market_Share` column of the input data frame.
- Shares are checked for obvious issues:
  - Negative values are rejected.
  - Totals significantly above 100 (e.g. more than 100.1) raise an error.

When data comes from revenue rather than shares:

- BigQuery ingestion maps `Revenue` to market shares by dividing firm revenue by total revenue and multiplying by 100.
- The resulting shares are treated exactly as if they had been provided directly.

---

## Herfindahl–Hirschman Index (HHI)

For a market with N firms and shares s₁, s₂, ..., sₙ (in percent), the Herfindahl–Hirschman Index is:

```text
HHI = s₁² + s₂² + ... + sₙ²
```

In this implementation:

- Shares are squared as given, so a 30% share contributes 900 to the index.
- The sum of squared shares is returned as a floating-point value.
- No further rescaling is applied, so an HHI of 10,000 corresponds to a pure monopoly.

The `calculate_hhi` function in `metrics.py` encapsulates this logic and performs the basic validation described above.

---

## Merger Simulation Logic

A merger simulation proceeds in three steps:

1. **Identify the acquirer and target**

   - The user passes two firm names (e.g. `"Firm B"`, `"Firm C"`).
   - The data frame is filtered to find rows for those firms and verify they exist.
2. **Construct the post‑merger market**

   - The acquirer and target are combined into a single line.
   - Their shares are added together.
   - Other firms remain unchanged.
3. **Compute pre‑ and post‑merger HHI**

   - Pre‑merger HHI is computed from the original shares.
   - Post‑merger HHI is computed from the combined shares.
   - The change \(\Delta HHI = HHI_{\text{post}} - HHI_{\text{pre}}\) is reported.

The `simulate_merger` function in `simulation.py` wraps these steps, returning a structured result that includes `hhi_pre`, `hhi_post`, `delta`, `concentration_level`, and `regulatory_risk`.

---

## Concentration Categories and Risk Tiers

The toolkit uses configurable thresholds (via the `THRESHOLDS` object in `config.py`) to categorize concentration and assess risk.

### Concentration categories

Post‑merger HHI is mapped to three qualitative categories:

- **Unconcentrated** – HHI below `UNCONCENTRATED_MAX`.
- **Moderately Concentrated** – HHI between `UNCONCENTRATED_MAX` and `HIGHLY_CONCENTRATED_MIN`.
- **Highly Concentrated** – HHI above `HIGHLY_CONCENTRATED_MIN`.

These cutoffs are intended to match commonly used ranges in merger guidelines but can be changed in `config.py` if a jurisdiction uses different thresholds.

### Risk tiers

The change in HHI (\(\Delta HHI\)) is evaluated jointly with the concentration category:

- **Low Risk**

  - \(\Delta HHI\) below `DELTA_LOW_RISK_MAX`.
  - Typically interpreted as unlikely to generate adverse competitive effects.
- **Moderate Risk**

  - Market is “Moderately Concentrated” and \(\Delta HHI\) above `DELTA_LOW_RISK_MAX`.
  - May warrant closer scrutiny depending on context.
- **Moderate / High Risk**

  - Market is “Highly Concentrated” and \(\Delta HHI\) between `DELTA_LOW_RISK_MAX` and `DELTA_HIGH_RISK_MIN`.
  - Often viewed as potentially raising significant concerns.
- **High Risk (Red Flag)**

  - Market is “Highly Concentrated” and \(\Delta HHI\) above `DELTA_HIGH_RISK_MIN`.
  - Typically interpreted as a strong indicator that the merger enhances market power.

If none of these conditions apply, a conservative “Low Risk / Safe harbor” label is returned by `evaluate_antitrust_risk`.

---

## Jurisdictional Flexibility

While the thresholds are inspired by widely cited guidance, enforcement practice varies across jurisdictions. This toolkit treats thresholds as **model parameters**, not legal advice.

You can:

- Adjust them in `config.py` to match your institution’s internal standards.
- Define alternative threshold sets for different countries and select them at runtime.
- Extend the logic to add more nuanced labels if your workflow requires them.

---

## Limitations and Intended Use

This project focuses on **static concentration** measures:

- It does not model dynamic entry or exit, multi‑market contact, or complex demand systems.
- It does not replace full‑scale merger simulation models (e.g. structural demand estimation).
- It is designed for quick screening, scenario exploration, and didactic case studies.

For high‑stakes cases, HHI should be treated as one input into a broader analysis rather than the sole decision rule.

---

## References and Further Reading

See `docs/examples.md` and the notebooks in `notebooks/` for worked examples and historical case studies, and consult official merger guidelines for your jurisdiction for authoritative thresholds and interpretation.
