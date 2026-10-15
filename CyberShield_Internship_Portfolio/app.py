from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.analytics import load_incidents, load_messages, dataset_quality, category_summary
from src.risk_engine import analyze_message
from src.case_library import CASE_LIBRARY

st.set_page_config(page_title="CyberShield", page_icon="🛡️", layout="wide")
st.title("🛡️ CyberShield")
st.caption("Cyber threat awareness • explainable message screening • synthetic incident analytics")
st.warning("Educational prototype only. Scores are heuristic indicators, not probabilities or definitive verdicts. Do not enter real victim, financial, credential, or investigation data.")

incidents = load_incidents()
messages = load_messages()

tab_overview, tab_checker, tab_analytics, tab_library, tab_response, tab_about = st.tabs([
    "Overview", "Message Risk Checker", "Incident Analytics", "Threat Library", "Incident Response", "Method & Limits"
])

with tab_overview:
    st.subheader("Project overview")
    st.write("Explore synthetic case records, screen sample message text for common warning signs, and review safe response guidance.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Synthetic incident records", f"{len(incidents):,}")
    c2.metric("Threat categories", f"{incidents['category'].nunique():,}")
    c3.metric("Synthetic message examples", f"{len(messages):,}")
    c4.metric("Case library entries", f"{len(CASE_LIBRARY):,}")
    st.info("These counts describe this bundled teaching dataset only. They are not real-world cybercrime statistics.")
    st.subheader("Incident categories in the sample")
    cat = category_summary(incidents)
    fig = px.bar(cat.head(12).sort_values("records"), x="records", y="category", orientation="h",
                 title="Most represented categories in the synthetic dataset",
                 labels={"records":"Synthetic records","category":"Category"})
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Sample records")
    st.dataframe(incidents.head(10), use_container_width=True, hide_index=True)

with tab_checker:
    st.subheader("Rule-based message risk screening")
    st.write("Paste only a fictional/example message. The checker performs local text matching; it does not open links or submit text to an external service.")
    sample = st.selectbox("Try a fictional example", [
        "Choose an example…",
        "URGENT: Your bank account will be blocked. Click here to verify your password and OTP immediately.",
        "This is a reminder that your library book is due tomorrow. Please return it to the front desk.",
        "A caller claiming to be police says I am under digital arrest and must transfer money. Do not tell anyone.",
        "Your parcel is delayed. Pay a small delivery fee using this unfamiliar link.",
        "Your colleague asks you to review the agenda for tomorrow's meeting."
    ])
    default_text = "" if sample == "Choose an example…" else sample
    text_input = st.text_area("Message text", value=default_text, height=160, placeholder="Paste a fictional message here…")
    if st.button("Analyze message", type="primary"):
        if not text_input.strip():
            st.error("Enter a message or choose an example.")
        else:
            result = analyze_message(text_input)
            col1, col2 = st.columns([1, 2])
            col1.metric("Heuristic score", f"{result['score']} / 20")
            col1.metric("Screening level", result["level"])
            col2.write("**Suggested next step**")
            col2.write(result["advice"])
            if result["signals"]:
                st.write("**Triggered indicators**")
                st.dataframe(pd.DataFrame(result["signals"]), use_container_width=True, hide_index=True)
            else:
                st.info("No configured indicator matched. This is not proof that the message is safe.")
            if result["urls_found"]:
                st.write("**Text-shaped URLs found (not opened or checked):**")
                for u in result["urls_found"]:
                    st.code(u)
            st.caption(result["disclaimer"])

with tab_analytics:
    st.subheader("Synthetic incident analytics")
    left, right = st.columns(2)
    with left:
        kind_filter = st.multiselect("Filter by incident kind", sorted(incidents["kind"].dropna().unique()), default=sorted(incidents["kind"].dropna().unique()))
    with right:
        severity_filter = st.slider("Minimum severity score", min_value=1, max_value=5, value=1)
    filtered = incidents[incidents["kind"].isin(kind_filter) & (incidents["severity_score"] >= severity_filter)]
    m1, m2, m3 = st.columns(3)
    m1.metric("Filtered synthetic records", len(filtered))
    m2.metric("Categories represented", filtered["category"].nunique())
    m3.metric("Mean severity (1–5)", f"{filtered['severity_score'].mean():.2f}" if len(filtered) else "N/A")
    if len(filtered):
        a, b = st.columns(2)
        with a:
            fig = px.bar(filtered.groupby("category").size().reset_index(name="records").sort_values("records", ascending=False).head(15),
                         x="records", y="category", orientation="h", title="Records by category (top 15)")
            st.plotly_chart(fig, use_container_width=True)
        with b:
            fig = px.histogram(filtered, x="severity_score", nbins=5, title="Synthetic severity-score distribution",
                               labels={"severity_score":"Severity score"})
            st.plotly_chart(fig, use_container_width=True)
        timeline = filtered.dropna(subset=["date"]).groupby(filtered["date"].dt.to_period("M").astype(str)).size().reset_index(name="records")
        timeline.columns = ["month", "records"]
        fig = px.line(timeline, x="month", y="records", markers=True, title="Synthetic records by month")
        st.plotly_chart(fig, use_container_width=True)
        st.download_button("Download filtered synthetic records (CSV)", filtered.to_csv(index=False).encode("utf-8"), "cybershield_filtered_synthetic_incidents.csv", "text/csv")
        st.dataframe(filtered, use_container_width=True, hide_index=True)
    else:
        st.info("No records match these filters.")
    st.caption("Charts describe the generated sample only; they do not estimate actual prevalence or financial loss.")

with tab_library:
    st.subheader("Threat and case library")
    query = st.text_input("Search categories, signals, or guidance")
    kinds = sorted({x["kind"] for x in CASE_LIBRARY})
    selected_kind = st.selectbox("Threat family", ["All"] + kinds)
    filtered_cases = [x for x in CASE_LIBRARY if (selected_kind == "All" or x["kind"] == selected_kind)]
    if query.strip():
        q = query.casefold()
        filtered_cases = [x for x in filtered_cases if q in " ".join(x.values()).casefold()]
    st.write(f"Showing {len(filtered_cases)} case guides.")
    for case in filtered_cases:
        with st.expander(f"{case['category']} — {case['kind']}"):
            st.write(case["description"])
            st.write("**Possible signals**")
            st.write(case["signals"])
            st.write("**Safer response**")
            st.write(case["response"])

with tab_response:
    st.subheader("Initial incident-response checklist")
    st.write("Use organisational policy and specialist advice where applicable. Actions depend on the incident and safety context.")
    checklist = [
        ("Protect people and stop ongoing harm", "If there is immediate danger, seek local emergency assistance. Do not confront suspected offenders."),
        ("Stop risky interaction", "Do not send money, share OTPs/PINs/passwords, approve login prompts, or open further links/attachments."),
        ("Contact relevant provider quickly", "For suspected payment fraud, contact the bank/payment provider immediately using an official channel."),
        ("Report in India where applicable", "Use the official National Cyber Crime Reporting Portal at https://cybercrime.gov.in/. For financial cyber fraud, the 1930 helpline is commonly used; follow current official guidance."),
        ("Preserve evidence", "Keep original messages, sender details, transaction IDs, dates/times, screenshots, and relevant URLs. Do not edit evidence or publish private details."),
        ("Secure accounts and devices", "From a trusted device, change exposed passwords, revoke sessions, enable MFA, update software, and check recovery details."),
        ("Escalate technical incidents", "For malware/ransomware, notify qualified IT/security responders; isolate affected systems as appropriate and protect known-clean backups."),
        ("Document actions", "Record who did what and when, decisions taken, systems/accounts affected, and outstanding risks.")
    ]
    for title, detail in checklist:
        st.markdown(f"- [ ] **{title}:** {detail}")
    st.info("Do not factory-reset, delete files, or run improvised cleanup tools before considering evidence preservation and receiving appropriate advice.")
    st.markdown("Official starting points: [National Cyber Crime Reporting Portal](https://cybercrime.gov.in/) · [CERT-In](https://www.cert-in.org.in/) · [CISA phishing guidance](https://www.cisa.gov/resources-tools/resources/phishing-postcard)")

with tab_about:
    st.subheader("Methodology, quality checks, and limitations")
    quality = dataset_quality(incidents)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", quality["rows"])
    c2.metric("Columns", quality["columns"])
    c3.metric("Missing cells", quality["missing_cells"])
    c4.metric("Duplicate rows", quality["duplicate_rows"])
    st.markdown("""
**Screening method**
- Transparent regular-expression rules look for urgency, credential requests, payment pressure, authority impersonation, prize claims, remote-access language, attachments, suspicious-link wording, secrecy, identity data requests, recruitment fees, and investment lures.
- A score is a sum of configured rule weights capped at 20. It is not calibrated to a probability.
- URL extraction is text-only. The app does not visit URLs, resolve domains, inspect files, query threat feeds, or guarantee safety.

**Dataset limitations**
- All incident records and labelled messages are synthetic examples.
- The dataset is not representative of real cyber incidents, and the sample distribution is intentionally educational.
- Do not interpret the charts as real trends, prevalence, loss estimates, or evidence of model effectiveness.

**Responsible use**
- Use only with synthetic or authorised data.
- Do not use this tool to accuse a person, make legal decisions, or automatically block users.
- For operational security work, use approved tools, validated data, documented procedures, and qualified review.
""")
    st.subheader("Optional ML demonstration")
    if st.button("Run a teaching-only ML evaluation"):
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.linear_model import LogisticRegression
            from sklearn.model_selection import train_test_split
            from sklearn.pipeline import Pipeline
            from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
            X = messages["text"].astype(str)
            y = messages["label"].astype(str)
            if y.nunique() < 2 or y.value_counts().min() < 2:
                st.error("Not enough examples per class for a stratified demonstration.")
            else:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.25, random_state=42, stratify=y
                )
                model = Pipeline([
                    ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=1)),
                    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
                ])
                model.fit(X_train, y_train)
                pred = model.predict(X_test)
                st.metric("Accuracy on held-out synthetic examples", f"{accuracy_score(y_test, pred):.1%}")
                st.text("Classification report (synthetic teaching sample):")
                st.code(classification_report(y_test, pred, zero_division=0))
                labels = sorted(y.unique())
                cm = confusion_matrix(y_test, pred, labels=labels)
                st.write("Confusion matrix (rows = actual, columns = predicted; label order shown below):")
                st.write(labels)
                st.dataframe(pd.DataFrame(cm, index=labels, columns=labels), use_container_width=True)
                st.warning("This score is not real-world performance. Repeated synthetic patterns can make results misleading. Do not claim production-grade detection.")
        except Exception as exc:
            st.error(f"Could not run optional ML demo: {exc}")
