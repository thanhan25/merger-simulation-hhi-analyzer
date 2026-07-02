"""
Visualization modules for market concentration and merger effects.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any
from pathlib import Path

# Set a professional, executive-grade styling
sns.set_theme(style="whitegrid", context="paper")
plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.dpi": 300,
    }
)


def plot_merger_impact(
    sim_results: Dict[str, Any],
    output_path: str = "output/figures/hhi_before_after.png",
):
    """
    Generate an executive-grade bar chart comparing pre- and post-merger market shares.

    Args:
        sim_results (Dict[str, Any]): The output dictionary from simulation.simulate_merger().
        output_path (str): The file path to save the generated figure.
    """
    pre_df = sim_results["pre_merger_df"]
    post_df = sim_results["post_merger_df"]

    # Identify the merged firm name to highlight it
    merged_firm_name = [name for name in post_df.iloc[:, 0].values if "+" in str(name)][
        0
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    # Color palettes: Standard corporate blue, with a specific highlight for the merged firm
    base_color = "#2c3e50"
    highlight_color = "#e74c3c"

    # Plot Pre-Merger
    sns.barplot(
        data=pre_df, x=pre_df.columns[0], y=pre_df.columns[1], color=base_color, ax=ax1
    )
    ax1.set_title(
        f"Pre-Merger Market Shares\n(HHI: {sim_results['hhi_pre']})", fontweight="bold"
    )
    ax1.set_xlabel("Firms")
    ax1.set_ylabel("Market Share (%)")
    ax1.tick_params(axis="x", rotation=45)

    # Plot Post-Merger (FIXED: Added hue and legend=False to comply with Seaborn >= 0.13)
    colors = [
        highlight_color if firm == merged_firm_name else base_color
        for firm in post_df.iloc[:, 0]
    ]
    sns.barplot(
        data=post_df,
        x=post_df.columns[0],
        y=post_df.columns[1],
        hue=post_df.columns[0],
        palette=colors,
        legend=False,
        ax=ax2,
    )
    ax2.set_title(
        f"Post-Merger Market Shares\n(HHI: {sim_results['hhi_post']} | $\\Delta$: +{sim_results['delta']})",
        fontweight="bold",
    )
    ax2.set_xlabel("Firms")
    ax2.tick_params(axis="x", rotation=45)

    # Clean up borders
    sns.despine(left=True, bottom=True)
    plt.tight_layout()

    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    print(f"📊 Visualization saved to: {output_path}")
