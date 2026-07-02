"""
Command Line Interface for the Merger Simulation toolkit.
"""

import typer
import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .simulation import simulate_merger
from .plotting import plot_merger_impact
from .io import load_market_data, load_market_data_from_bigquery

app = typer.Typer(
    help="Python library and CLI for HHI market concentration measurement."
)
console = Console()


@app.command()
def analyze(
    acquirer: str = typer.Argument(..., help="Name of the acquiring firm"),
    target: str = typer.Argument(..., help="Name of the target firm"),
    filepath: str | None = typer.Option(None, "--file", "-f", help="Path to CSV"),
    query: str | None = typer.Option(None, "--query", "-q", help="BigQuery SQL"),
    mock_data: bool = typer.Option(False, "--mock", help="Use mock data"),
    output_json: str | None = typer.Option(
        None, "--output-json", help="Export results to JSON"
    ),
    output_csv: str | None = typer.Option(
        None, "--output-csv", help="Export combined market shares to CSV"
    ),
    no_plots: bool = typer.Option(
        False, "--no-plots", help="Disable plotting for headless execution"
    ),
):
    """Simulate a merger and evaluate HHI regulatory risk."""
    if mock_data:
        df = pd.DataFrame(
            {"Firm": ["Firm A", "Firm B", "Firm C"], "Market_Share": [40.0, 30.0, 30.0]}
        )
    elif query:
        df = load_market_data_from_bigquery(query)
    elif filepath:
        df = load_market_data(filepath)
    else:
        console.print("[bold red]Error:[/bold red] Provide --file, --query, or --mock.")
        raise typer.Exit(1)

    try:
        scenario = simulate_merger(df, "Firm", "Market_Share", acquirer, target)

        # UI Rendering
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Pre-Merger HHI", f"{scenario.pre_hhi:.2f}")
        table.add_row("Post-Merger HHI", f"[bold]{scenario.post_hhi:.2f}[/bold]")
        table.add_row("HHI Delta (Δ)", f"[bold red]+{scenario.delta:.2f}[/bold red]")
        table.add_row("Risk", scenario.regulatory_risk)

        console.print(
            Panel(table, title=f"Merger: {acquirer} + {target}", border_style="blue")
        )

        # Exports
        if output_json:
            Path(output_json).write_text(scenario.model_dump_json(indent=2))
            console.print(f"[dim]Saved JSON to {output_json}[/dim]")

        if not no_plots:
            plot_merger_impact(scenario.model_dump())

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        # Re-raise the exception so Pytest can catch the traceback instead of just exiting
        import sys

        if "pytest" in sys.modules:
            raise
        raise typer.Exit(1)


@app.command()
def ui():
    """Launch the interactive Streamlit dashboard."""
    import subprocess
    from pathlib import Path

    app_path = Path(__file__).parent / "app.py"
    subprocess.run(["streamlit", "run", str(app_path)])


if __name__ == "__main__":
    app()
