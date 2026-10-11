"""Customer Value Intelligence: illustrative, rules-based portfolio analytics."""
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Customer Value Intelligence", page_icon="📊", layout="wide")
REQUIRED = ["customer", "industry", "annual_revenue", "days_to_renewal", "adoption_pct", "satisfaction_score", "critical_issues", "adoption_trend", "expansion_potential"]

@st.cache_data
def load_data():
    df = pd.read_csv(Path(__file__).parent / "customer_data.csv")
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    for field in ["annual_revenue", "days_to_renewal", "adoption_pct", "satisfaction_score", "critical_issues"]:
        df[field] = pd.to_numeric(df[field], errors="raise")
    if df["customer"].duplicated().any():
        raise ValueError("Customer names must be unique")
    if (df["annual_revenue"] < 0).any() or (df["critical_issues"] < 0).any() or (df["days_to_renewal"] < 0).any():
        raise ValueError("Revenue, critical issues, and days to renewal must be nonnegative")
    if (~df["adoption_pct"].between(0, 100)).any() or (~df["satisfaction_score"].between(0, 5)).any():
        raise ValueError("Adoption must be 0–100 and satisfaction must be 0–5")
    return df

def recommend(row, expansion):
    """Return an ordered, evidence-based action; top priority wins."""
    if row.critical_issues >= 2:
        return "Assign an escalation owner, resolve critical issues, and agree on recovery milestones."
    if row.satisfaction_score < 3.8:
        return "Schedule a customer listening session and agree on a satisfaction recovery plan."
    if row.adoption_pct < 60 or row.adoption_trend == "Declining":
        return "Diagnose adoption barriers and agree on targeted enablement milestones."
    if row.critical_issues > 0:
        return "Resolve the open critical issue and confirm the customer's experience has recovered."
    if row.days_to_renewal <= 90:
        return "Begin renewal planning, validate realized value, and align executive stakeholders."
    if expansion:
        return "Explore additional use cases and build a quantified expansion business case."
    return "Continue monitoring adoption, satisfaction, and business outcomes."

def evaluate(row):
    adoption = row.adoption_pct / 100 * 30
    satisfaction = row.satisfaction_score / 5 * 25
    issues = max(0, 20 - row.critical_issues * 7)
    trend = {"Increasing": 15, "Stable": 10, "Declining": 0}.get(str(row.adoption_trend), 5)
    # Renewal timing represents readiness/urgency, not relationship quality.
    renewal = 10 if row.days_to_renewal > 120 else 6 if row.days_to_renewal > 60 else 2
    score = round(adoption + satisfaction + issues + trend + renewal)
    status = "Healthy" if score >= 75 else "Watchlist" if score >= 50 else "At risk"
    reasons = []
    if row.adoption_pct < 60: reasons.append("Low product adoption")
    if row.adoption_trend == "Declining": reasons.append("Declining adoption")
    if row.satisfaction_score < 3.8: reasons.append("Low satisfaction")
    if row.critical_issues > 0: reasons.append(f"{int(row.critical_issues)} critical issue(s)")
    if row.days_to_renewal <= 90: reasons.append("Renewal within 90 days")
    expansion = (row.expansion_potential == "High" and row.adoption_pct >= 70 and row.satisfaction_score >= 4 and row.critical_issues == 0)
    renewal_priority = "Due within 30 days" if row.days_to_renewal <= 30 else "Due within 90 days" if row.days_to_renewal <= 90 else "Beyond 90 days"
    return pd.Series({"health_score": score, "health_status": status, "renewal_priority": renewal_priority, "risk_drivers": "; ".join(reasons) or "No defined risk triggers", "expansion_candidate": expansion, "recommended_action": recommend(row, expansion)})

st.title("Customer Value Intelligence")
st.caption("Portfolio demonstration · Fictional customer data · Rules-based analytics (no live generative AI)")
st.info("Illustrative scoring and recommendations; not validated against actual customer outcomes. Revenue exposure is not a prediction of loss.")
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

at_risk = view[view.health_status == "At risk"]
watch = view[view.health_status == "Watchlist"]
expansion = view[view.expansion_candidate]
renewing = view[view.days_to_renewal <= 90]
total_revenue = view.annual_revenue.sum()
risk_revenue = at_risk.annual_revenue.sum()
renewal_revenue = renewing.annual_revenue.sum()

st.subheader("Portfolio overview")
a, b, c, d = st.columns(4)
a.metric("Annual revenue", f"${total_revenue:,.0f}")
b.metric("Accounts", len(view))
c.metric("At-risk accounts", len(at_risk))
d.metric("Expansion candidates", len(expansion))
e, f, g = st.columns(3)
e.metric("Revenue associated with at-risk accounts", f"${risk_revenue:,.0f}")
f.metric("At-risk share of portfolio", f"{risk_revenue / total_revenue:.1%}" if total_revenue else "N/A")
g.metric("Revenue renewing within 90 days", f"${renewal_revenue:,.0f}")
st.caption("Revenue figures represent the selected accounts. At-risk revenue and near-term renewal revenue can overlap; do not add them together.")

left, right = st.columns([1, 2])
with left:
    st.subheader("Health distribution")
    counts = view.health_status.value_counts().reindex(["At risk", "Watchlist", "Healthy"], fill_value=0)
    st.bar_chart(counts.rename("Accounts"))
with right:
    st.subheader("Accounts requiring attention")
    priority = view[view.health_status != "Healthy"].sort_values(["health_score", "days_to_renewal"])
    if priority.empty:
        st.success("No accounts are currently classified as Watchlist or At risk under these illustrative rules.")
    else:
        for row in priority.itertuples():
            with st.expander(f"{row.customer} · {row.health_status} ({row.health_score}/100) · ${row.annual_revenue:,.0f}", expanded=row.health_status == "At risk"):
                st.write(f"**Risk signals:** {row.risk_drivers}")
                st.write(f"**Next action:** {row.recommended_action}")

st.subheader("Account analysis")
columns = ["customer", "industry", "annual_revenue", "days_to_renewal", "renewal_priority", "adoption_pct", "satisfaction_score", "critical_issues", "health_score", "health_status", "expansion_candidate", "risk_drivers", "recommended_action"]
ordered = view[columns].sort_values(["health_score", "days_to_renewal"])
st.dataframe(
    ordered, hide_index=True, use_container_width=True,
    column_config={
        "customer": st.column_config.TextColumn("Customer"),
        "industry": st.column_config.TextColumn("Industry"),
        "annual_revenue": st.column_config.NumberColumn("Annual Revenue", format="$%d"),
        "days_to_renewal": st.column_config.NumberColumn("Days to Renewal", format="%d"),
        "renewal_priority": st.column_config.TextColumn("Renewal Timing", width="medium"),
        "adoption_pct": st.column_config.NumberColumn("Adoption (%)", format="%d%%"),
        "satisfaction_score": st.column_config.NumberColumn("Satisfaction (0–5)", format="%.1f"),
        "critical_issues": st.column_config.NumberColumn("Critical Issues", format="%d"),
        "health_score": st.column_config.ProgressColumn("Health Score", min_value=0, max_value=100, format="%d"),
        "health_status": st.column_config.TextColumn("Health Status"),
        "expansion_candidate": st.column_config.CheckboxColumn("Expansion Candidate"),
        "risk_drivers": st.column_config.TextColumn("Key Risk Factors", width="large"),
        "recommended_action": st.column_config.TextColumn("Recommended Action", width="large"),
    },
)
st.download_button("Download scored portfolio (CSV)", ordered.to_csv(index=False).encode("utf-8"), "customer_intelligence_results.csv", "text/csv")

st.subheader("Executive decision brief")
st.write(f"**Portfolio assessment:** {len(at_risk)} at-risk, {len(watch)} watchlist, and {len(expansion)} expansion candidate accounts across ${total_revenue:,.0f} in illustrative annual revenue.")
p1, p2, p3 = st.columns(3)
with p1:
    st.markdown("#### 1. Protect revenue")
    st.write(f"${risk_revenue:,.0f} is associated with at-risk accounts ({risk_revenue / total_revenue:.1%} of selected portfolio)." if total_revenue else "No revenue available.")
    if not at_risk.empty:
        st.write("Prioritize: " + ", ".join(at_risk.sort_values("health_score").customer) + ". Assign owners and recovery milestones.")
    else:
        st.write("No accounts currently meet the at-risk threshold.")
with p2:
    st.markdown("#### 2. Explore growth")
    if not expansion.empty:
        st.write("Evaluate " + ", ".join(expansion.customer) + " for additional use cases and a validated business case.")
    else:
        st.write("No accounts currently meet the expansion-screening criteria.")
    st.caption("Screening signals are not revenue forecasts.")
with p3:
    st.markdown("#### 3. Monitor and prepare")
    st.write(f"{len(watch)} watchlist account(s) need targeted follow-up; ${renewal_revenue:,.0f} in annual revenue renews within 90 days.")
    st.write("Validate realized value, adoption trends, and open issues ahead of renewal.")

with st.expander("Scoring methodology and limitations"):
    st.write("Adoption (30 points), satisfaction (25), critical issues (20), adoption trend (15), and renewal timing (10). Healthy ≥75; Watchlist 50–74; At risk <50.")
    st.write("The thresholds and weights are illustrative. Renewal proximity influences this composite score as a readiness signal, but it is not a direct measure of relationship health. A separate renewal timing column makes that distinction visible.")
    st.write("All customer names and metrics are synthetic. This app uses deterministic rules and was developed with AI assistance; it does not call an AI model at runtime.")
