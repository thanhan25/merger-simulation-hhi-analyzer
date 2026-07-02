# Econometric Methodology: Horizontal Merger Guidelines

This simulator mathematically enforces the joint antitrust frameworks established by the U.S. Department of Justice (DOJ) and the Federal Trade Commission (FTC).

## The Herfindahl-Hirschman Index (HHI)
The core metric for market concentration is the HHI. It is calculated by squaring the market share of each firm and summing the results:

$$HHI = \sum_{i=1}^{N} s_i^2$$

Where $s_i$ is the market share of firm $i$, and $N$ is the total number of firms in the relevant market.

## Regulatory Risk Thresholds (2023 Guidelines)
The simulator evaluates antitrust risk based on the $\Delta$ HHI resulting from the simulated merger.

1. **Unconcentrated Markets ($HHI < 1500$)**
   * Mergers are generally unconcealed and rarely require further analysis.
2. **Moderately Concentrated Markets ($1500 \le HHI \le 2500$)**
   * $\Delta HHI > 100$: Mergers warrant scrutiny and potential Phase II investigations.
3. **Highly Concentrated Markets ($HHI > 2500$)**
   * $\Delta HHI > 100$: Mergers are presumed to substantially lessen competition.
   * $\Delta HHI > 200$: Mergers are subject to strict regulatory blocks and require significant divestiture to proceed.
