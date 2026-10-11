# Customer Value Intelligence

**A free, interactive customer portfolio analytics and decision-support demonstration.**

**[Open the live dashboard](https://customer-value-intelligence-3chqskzrzhznvbrue7uf5r.streamlit.app/)**

> **Transparency:** All 12 customer records are fictional. The dashboard uses deterministic, rules-based analytics and was developed with AI assistance. It does **not** run a generative AI model or connect to customer systems. Scores, weights, and recommendations are illustrative, not validated predictions.

## The business problem

Enterprise customer teams must synthesize adoption, satisfaction, support, renewal, and revenue data into actionable priorities. Manual analysis can delay decisions and make consistent executive reporting difficult.

## What I built

A browser-based Streamlit application that:

- Analyzes a **12-account synthetic portfolio** with **$6.78 million** in illustrative annual revenue.
- Calculates explainable account health scores and classifies accounts as **Healthy**, **Watchlist**, or **At risk**.
- Flags customer-specific risk drivers and suggests rules-based next actions.
- Highlights expansion candidates and renewal timing.
- Quantifies revenue associated with at-risk accounts and renewals due within 90 days.
- Filters by industry and exports scored customer data as CSV.
- Presents an executive decision brief organized around protecting revenue, exploring growth, and monitoring accounts.

## Illustrative dashboard findings

| Measure | Result |
| --- | ---: |
| Accounts analyzed | 12 |
| Annual revenue in synthetic portfolio | $6,780,000 |
| At-risk accounts | 2 |
| Watchlist accounts | 3 |
| Healthy accounts | 7 |
| Expansion screening candidates | 3 |
| Revenue associated with at-risk accounts | $870,000 (12.8%) |
| Revenue renewing within 90 days | $2,355,000 |

**Important:** At-risk revenue and upcoming renewal revenue can overlap. Neither is a forecast of revenue loss.

## How the scoring works

Each account receives an illustrative score out of 100:

| Signal | Maximum points |
| --- | ---: |
| Product adoption | 30 |
| Customer satisfaction | 25 |
| Critical issue burden | 20 |
| Adoption trend | 15 |
| Renewal timing | 10 |

Health classifications: **Healthy ≥75**, **Watchlist 50–74**, **At risk <50**. Rules flag specific drivers and prioritize actions such as critical-issue escalation, adoption enablement, customer listening, renewal planning, or expansion discovery. Renewal timing is an urgency/readiness signal, not a direct measure of customer relationship health.

## Efficiency benchmark — one demonstration

I compared completing a five-task executive portfolio review manually against using the dashboard to complete the same work, including reviewing the output:

| Workflow | Observed time |
| --- | ---: |
| Manual review | 60 minutes |
| Dashboard-assisted review | 15 minutes |
| Time saved | **45 minutes** |
| Time reduction | **75%** |
| Relative speed | **4×** |

Formula: `(60 − 15) / 60 × 100 = 75%`.

**Benchmark limitations:** These are self-reported times from a single exercise using a fictional 12-account dataset. They are not independently verified, repeated-trial results, or evidence of a 75% efficiency gain in a production environment. The comparison is a useful initial demonstration, not a generalized performance claim. See [BENCHMARK.md](BENCHMARK.md) for the task definition and reproducibility guidance.

## Technology

- **Python** — analysis logic
- **Pandas** — data handling and calculations
- **Streamlit** — interactive dashboard and CSV export
- **GitHub** — source control and documentation
- **Streamlit Community Cloud** — public deployment
- **AI-assisted development** — support with code, design, and documentation; no live AI API

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Required files: `app.py`, `customer_data.csv`, and `requirements.txt` in the same directory.

## Test coverage and limitations

Browser checks completed for industry filtering, account recommendations, and CSV export. Dashboard metrics were visually confirmed after deployment. Scoring assumptions are intentionally simplified, and the dataset is synthetic. Before use in a real business setting, a production implementation would require stakeholder-approved metrics, historical validation, security/access controls, monitoring, and integration with approved data systems.

## Why I built this

I wanted to demonstrate how analytical problem-solving, process improvement, and practical AI-assisted development can turn customer data into executive decisions. The project connects enterprise customer success experience with hands-on workflow automation and transparent measurement.
