"""Customer Value Intelligence — synthetic-data portfolio demonstration."""
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Customer Value Intelligence", page_icon="📊", layout="wide")
REQUIRED = ["customer", "industry", "annual_revenue", "days_to_renewal", "adoption_pct", "satisfaction_score", "critical_issues", "adoption_trend", "expansion_potential"]

@st.cache_data
def load_data():
    path = Path(__file__).parent / "customer_data.csv"
    df = pd.read_csv(path)
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    for col in ["annual_revenue", "days_to_renewal", "adoption_pct", "satisfaction_score", "critical_issues"]:
        df[col] = pd.to_numeric(df[col], errors="raise")
    return df

def evaluate(row):
    adoption = max(0, min(100, row.adoption_pct)) / 100 * 30
    satisfaction = max(0, min(5, row.satisfaction_score)) / 5 * 25
    issues = max(0, 20 - max(0, row.critical_issues) * 7)
    trend = {"Increasing": 15, "Stable": 10, "Declining": 0}.get(str(row.adoption_trend), 5)
    # Renewal proximity is a *risk-readiness* proxy, not a measure of customer satisfaction.
    renewal = 10 if row.days_to_renewal > 120 else 6 if row.days_to_renewal > 60 else 2
    score = round(adoption + satisfaction + issues + trend + renewal)
    status = "Healthy" if score >= 75 else "Watchlist" if score >= 50 else "At risk"
    reasons = []
    if row.adoption_pct < 60: reasons.append("low product adoption")
    if row.adoption_trend == "Declining": reasons.append("declining adoption")
    if row.satisfaction_score < 3.8: reasons.append("low satisfaction")
    if row.critical_issues > 0: reasons.append(f"{int(row.critical_issues)} critical issue(s)")
    if row.days_to_renewal <= 90: reasons.append("renewal within 90 days")
    expansion = (row.expansion_potential == "High" and row.adoption_pct >= 70 and row.satisfaction_score >= 4 and row.critical_issues == 0)
    if row.critical_issues > 0:
        action = "Resolve critical issues and confirm an executive recovery plan."
    elif row.days_to_renewal <= 90 and status != "Healthy":
        action = "Schedule a renewal-risk review and document a recovery plan."
    elif row.adoption_trend == "Declining":
        action = "Investigate adoption decline and agree on a success plan."
    elif expansion:
        action = "Validate additional use cases and quantify potential expansion value."
    else:
        action = "Continue monitoring account health and business outcomes."
    return pd.Series({"health_score": score, "health_status": status, "risk_drivers": "; ".join(reasons) or "No defined risk triggers", "expansion_candidate": expansion, "recommended_action": action})

st.title("Customer Value Intelligence")
st.caption("Portfolio demonstration • Synthetic customer data • Rules-based analytics, not a live AI model")
st.info("This is a learning project. Scores and thresholds are illustrative and have not been validated against real customer outcomes.")
try:
    data = load_data()
except Exception as exc:
    st.error(f"Could not load customer_data.csv: {exc}")
    st.stop()

scored = pd.concat([data, data.apply(evaluate, axis=1)], axis=1)
industries = sorted(scored["industry"].unique())
selected = st.multiselect("Filter by industry", industries, default=industries)
view = scored[scored["industry"].isin(selected)].copy()
if view.empty:
    st.warning("Select at least one industry to display the portfolio.")
    st.stop()

st.subheader("Portfolio overview")
a, b, c, d = st.columns(4)
a.metric("Annual revenue", f"${view['annual_revenue'].sum():,.0f}")
b.metric("Accounts", len(view))
c.metric("At-risk accounts", int((view.health_status == "At risk").sum()))
d.metric("Expansion candidates", int(view.expansion_candidate.sum()))

left, right = st.columns([1, 2])
with left:
    st.subheader("Health distribution")
    st.bar_chart(view.health_status.value_counts().reindex(["Healthy", "Watchlist", "At risk"], fill_value=0))
with right:
    st.subheader("Accounts requiring attention")
    priority = view[view.health_status != "Healthy"].sort_values(["health_score", "days_to_renewal"])
    if priority.empty:
        st.success("No accounts are classified as Watchlist or At risk under the current rules.")
    else:
        for row in priority.itertuples():
            st.markdown(f"**{row.customer}** — {row.health_status} ({row.health_score}/100)  \n{row.risk_drivers}  \n*Action:* {row.recommended_action}")

st.subheader("Account analysis")
columns = ["customer", "industry", "annual_revenue", "days_to_renewal", "adoption_pct", "satisfaction_score", "critical_issues", "health_score", "health_status", "expansion_candidate", "risk_drivers", "recommended_action"]
st.dataframe(view[columns].sort_values("health_score"), hide_index=True, use_container_width=True)
st.download_button("Download scored portfolio (CSV)", view[columns].to_csv(index=False).encode("utf-8"), "customer_intelligence_results.csv", "text/csv")

st.subheader("Executive decision brief")
at_risk = view[view.health_status == "At risk"]
watch = view[view.health_status == "Watchlist"]
expansion = view[view.expansion_candidate]
st.markdown(f"**Portfolio assessment:** {len(at_risk)} at-risk account(s), {len(watch)} watchlist account(s), and {len(expansion)} expansion candidate(s) across ${view.annual_revenue.sum():,.0f} in illustrative annual revenue.")
if not at_risk.empty:
    names = ", ".join(at_risk.sort_values("health_score").customer.head(3))
    st.markdown(f"**Immediate priority:** Review {names}. Confirm root causes, owners, and recovery milestones before making commercial decisions.")
if not expansion.empty:
    names = ", ".join(expansion.customer.head(4))
    st.markdown(f"**Growth exploration:** Assess {names} for additional use cases. Expansion eligibility is a screening signal, not a revenue forecast.")
st.caption("Method: adoption (30 pts), satisfaction (25), critical issues (20), adoption trend (15), renewal timing (10). Higher scores indicate fewer defined risk signals. All thresholds are illustrative.")
