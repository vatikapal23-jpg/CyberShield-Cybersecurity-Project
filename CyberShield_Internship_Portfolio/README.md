# CyberShield — Cybersecurity Learning & Case Analytics Lab

**Portfolio project | Python · Streamlit · Pandas · Plotly · scikit-learn**

CyberShield is an educational cybersecurity dashboard that brings together a curated public-case timeline (2010–2025), an explainable text-based message screener, synthetic incident analytics, a threat reference library, and an initial incident-response checklist.

> **Important data note:** the incident and message examples are synthetic. Historical cases are a selected public-record sample, not an exhaustive database. Screening scores are heuristics, not probabilities or proof.

## Features

- **Historical Cases (2010–2025):** filter selected cases by year, category, sector, record type, and free-text search; inspect defensive lessons and source links; export filtered CSV.
- **Message Risk Checker:** transparent rule-based screening with matched indicators, score explanation, text-only URL extraction, and practical next steps. It does not open links or contact external services.
- **Synthetic Incident Analytics:** filter generated incident examples, view category/severity/month charts, inspect data quality, and export filtered records.
- **Threat Library:** searchable summaries of common cyber threats and safer responses.
- **Incident Response Playbook:** general evidence-preservation, containment, account-security, and reporting checklist.
- **Optional ML teaching demo:** TF-IDF + Logistic Regression evaluated on a small synthetic dataset. The reported metrics are for learning only and are not evidence of real-world detection performance.
- **Reports and tests:** methodology, historical-case review, data dictionary, response playbook, and automated tests for the rule engine.

## Requirements

- Python 3.10 or newer
- Internet access only to install Python dependencies; the app itself does not need an external API
- A modern browser

## Run on Windows (PowerShell / VS Code)

1. Extract the ZIP archive.
2. Open the extracted `CyberShield_Internship_Portfolio` folder in VS Code.
3. Open a terminal in that folder.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Start the dashboard:

   ```powershell
   streamlit run app.py
   ```

7. Open the local URL printed in the terminal (usually `http://localhost:8501`).

If PowerShell blocks environment activation, use Command Prompt or call the virtual environment executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Stop the app with `Ctrl+C`.

## Run tests

From the project root:

```powershell
python -m unittest discover -s tests -v
```

## Project structure

```text
CyberShield_Internship_Portfolio/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── documented_cases_2010_2025.csv
│   ├── synthetic_incidents.csv
│   ├── synthetic_messages.csv
│   └── DATA_DICTIONARY.md
├── src/
│   ├── __init__.py
│   ├── analytics.py
│   ├── risk_engine.py
│   └── case_library.py
├── tests/
│   └── test_risk_engine.py
└── reports/
    ├── methodology.md
    ├── historical_cases_2010_2025.md
    ├── incident_response_playbook.md
    ├── project_report_template.md
    └── validation_report.txt
```

## Data and methodology

### Historical cases
The historical CSV includes year, case name, category, sector, summary, defensive lesson, source name, source URL, and record type. It is a curated sample of public reporting, not an exhaustive or statistically representative dataset. Some rows may describe campaigns, exploitation waves, or grouped entries rather than one incident. Follow source links and locate case-specific primary sources before formal citation.

### Synthetic records
The incident and message datasets are fictional examples built to demonstrate filtering, data cleaning, charts, and a basic text-classification workflow. Do not present their counts or charts as real cybercrime statistics.

### Message screening
A fixed set of regular-expression rules assigns weighted points to textual warning signs. Scores are capped at 20 and grouped into explanatory levels. The tool does not open URLs, inspect files, scan for malware, check domain reputation, query threat feeds, or guarantee that a message is safe.

## Suggested presentation flow

1. Introduce the objective and explain the difference between the historical sample and synthetic teaching data.
2. Demonstrate the historical timeline and filtering/export workflow.
3. Test the message checker with a fictional phishing example and explain the triggered rules.
4. Explore synthetic analytics and explicitly state that the charts are not real-world prevalence estimates.
5. Review the threat library and incident-response checklist.
6. Discuss limitations, ethics, and future improvements.

## Limitations and future work

- Historical coverage and source depth vary; verify primary references before academic use.
- Rule-based text matching can produce false positives and false negatives.
- Synthetic examples are not representative of real messages or incidents.
- The optional ML evaluation is not production validation.
- No live threat intelligence, URL reputation checks, malware analysis, automated response, or case-management integration is implemented.

Future improvements could include a documented/licensed real dataset, stronger schema validation, more robust tests, privacy-preserving uploads, error analysis, and evaluation against representative held-out data.

## Responsible use

Use only synthetic or authorised data. Do not enter credentials, financial information, personal data, or confidential incident details. Do not use outputs to accuse individuals or make automated legal, employment, or access decisions. Follow applicable law and organisational policy.

## References / starting points

- CSIS, Significant Cyber Incidents: https://www.csis.org/programs/strategic-technologies-program/significant-cyber-incidents
- CISA Cybersecurity Advisories: https://www.cisa.gov/news-events/cybersecurity-advisories
- CISA Phishing Guidance: https://www.cisa.gov/resources-tools/resources/phishing-postcard
- NIST Incident Response Resources: https://csrc.nist.gov/Projects/incident-response/preparation-resources
- CERT-In: https://www.cert-in.org.in/
- National Cyber Crime Reporting Portal (India): https://cybercrime.gov.in/

