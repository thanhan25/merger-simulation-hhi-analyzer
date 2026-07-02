from typer.testing import CliRunner
from merger_sim.cli import app

runner = CliRunner()


def test_cli_mock_headless():
    """Ensure the CLI runs successfully in headless mode with mock data."""
    result = runner.invoke(app, ["analyze", "Firm B", "Firm C", "--mock", "--no-plots"])

    # If the test fails, print the actual stdout and re-raise the exception for debugging
    if result.exit_code != 0:
        print(result.stdout)
        if result.exception:
            raise result.exception

    assert result.exit_code == 0
    assert "Pre-Merger HHI" in result.stdout
    assert "Post-Merger HHI" in result.stdout
