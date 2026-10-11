# Efficiency Benchmark — Customer Value Intelligence

## Recorded results

- **Manual workflow:** 60 minutes
- **Dashboard-assisted workflow:** 15 minutes
- **Difference:** 45 minutes
- **Time reduction:** (60 − 15) / 60 × 100 = **75%**
- **Speed ratio:** 60 / 15 = **4×**
- **Source:** Project creator's self-reported timings; one comparison.

## Workflow evaluated

Both methods were intended to complete the same five tasks on the same fictional 12-account customer portfolio:

1. Determine portfolio annual revenue and account count.
2. Identify accounts needing attention based on adoption, satisfaction, support issues, and renewal timing.
3. Identify expansion screening candidates.
4. Calculate revenue associated with at-risk accounts.
5. Prepare a short executive summary with the top priorities and recommended actions.

**Manual method:** Review `customer_data.csv` in a spreadsheet, apply the documented rules, calculate results, and prepare the summary without using the dashboard.

**Dashboard method:** Review the same portfolio through the deployed Streamlit dashboard, inspect/validate the analysis, and prepare the summary.

## Interpretation

The observed time reduction in this single synthetic-data exercise was **75%**, equivalent to **45 minutes saved**. This is a demonstration benchmark, not a production claim or a forecast of enterprise-wide savings.

## Limitations and future improvements

- Timings were self-reported; no independent observation or timestamped run logs were collected.
- Only one run of each workflow was reported; practice/order effects may influence the results.
- No detailed notes or error counts were recorded.
- Task equivalence and use of identical scoring rules were prescribed, but not independently audited.
- Synthetic data does not represent the complexity of production customer systems.

For stronger evidence, repeat both workflows several times, alternate their order where practical, use a fixed output template, compare answer accuracy, and record individual task timings. Report the median time and any discrepancies.
