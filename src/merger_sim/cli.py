"""
Command Line Interface for the Merger Simulation toolkit.
"""

import typer
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .simulation import simulate_merger
from .plotting import plot_merger_impact
from .io import load_market_data, load_market_data_from_bigquery

app = typer.Typer(help="Antitrust & Competition Economics Merger Simulator")
console = Console()


@app.callback()
def callback():
    """Quantitative Antitrust Toolkit for Market Concentration."""
    pass


@app.command()
def analyze(
    acquirer: str = typer.Argument(..., help="Name of the acquiring firm"),
    target: str = typer.Argument(..., help="Name of the target firm"),
    filepath: str = typer.Option(
        None, "--file", "-f", help="Path to the market shares CSV"
    ),
    query: str = typer.Option(
        None, "--query", "-q", help="Standard SQL query to execute in BigQuery"
    ),
    mock_data: bool = typer.Option(
        False, "--mock", help="Use generated mock data instead of a CSV"
    ),
):
    """
    Simulate a merger and output HHI concentration metrics.
    """
    # 1. Load Data
    if mock_data:
        data = {
            "Firm": ["Firm A", "Firm B", "Firm C", "Firm D", "Firm E", "Firm F"],
            "Market_Share": [35.0, 25.0, 15.0, 12.0, 8.0, 5.0],
        }
        df = pd.DataFrame(data)
        console.print("[dim]Using mock dataset...[/dim]")
    elif query:
        try:
            console.print(f"[dim]Executing BigQuery SQL: {query}[/dim]")
            df = load_market_data_from_bigquery(query)
            console.print(
                "[dim]Data successfully fetched and parsed from BigQuery.[/dim]"
            )
        except Exception as e:
            console.print(f"[bold red]BigQuery Error:[/bold red] {e}")
            raise typer.Exit(1)
    elif filepath:
        try:
            df = load_market_data(filepath)
            console.print(f"[dim]Loaded data from {filepath}[/dim]")
        except Exception as e:
            console.print(f"[bold red]Failed to load data:[/bold red] {e}")
            raise typer.Exit(1)
    else:
        console.print(
            "[bold red]Error:[/bold red] You must provide --file, --query, or --mock."
        )
        raise typer.Exit(1)

    try:
        # 2. Run Simulation
        results = simulate_merger(df, "Firm", "Market_Share", acquirer, target)

        # 3. Terminal Output via Rich
        console.print(
            Panel.fit(
                f"[bold blue]Merger Simulation:[/bold blue] {acquirer} + {target}",
                border_style="blue",
            )
        )

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric")
        table.add_column("Value")

        table.add_row("Pre-Merger HHI", str(results["hhi_pre"]))
        table.add_row("Post-Merger HHI", f"[bold]{results['hhi_post']}[/bold]")
        table.add_row("HHI Delta (Δ)", f"[bold red]+{results['delta']}[/bold red]")
        table.add_row("Concentration Level", results["concentration_level"])

        risk_color = "red" if "High Risk" in results["regulatory_risk"] else "yellow"
        table.add_row(
            "Regulatory Risk",
            f"[{risk_color}]{results['regulatory_risk']}[/{risk_color}]",
        )

        console.print(table)

        # 4. Generate Plot
        plot_merger_impact(results)

    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
