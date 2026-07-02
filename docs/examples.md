# Execution Examples

## 1. Cloud Infrastructure Integration (BigQuery)
For large-scale casework, bypass local flat files and query directly against Google Cloud:

```bash
uv run merger-sim analyze "TargetFirm" "AcquiringFirm" --query "SELECT firm, revenue FROM \`project.dataset.table\` WHERE market_segment = 'Retail'"
