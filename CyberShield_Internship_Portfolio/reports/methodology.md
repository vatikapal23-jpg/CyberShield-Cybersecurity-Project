# Methodology

## Project purpose
CyberShield is an educational dashboard for cybersecurity awareness, case exploration, transparent text screening, and basic data analysis.

## Data sources and scope
The historical case CSV is a curated sample of selected publicly reported events from 2010–2025. It is not exhaustive, and record types differ. Source links are starting points; locate and verify case-specific primary reports before citing factual details. Synthetic incident and message datasets are fictional examples created for demonstrating data processing and visualization.

## Rule-based screening
The screener applies regular-expression patterns and fixed weights to message text. Each matched rule is returned as an explanatory signal. Scores are capped at 20 and mapped to broad caution levels. They are not probabilities. The URL parser extracts URL-shaped text only and does not fetch or reputation-check destinations.

## Analytics
Pandas is used for loading, date parsing, filtering, grouping, and quality summaries. Plotly charts visualize the currently selected records. Historical charts describe the curated sample; synthetic charts describe generated examples. Neither should be used to infer population-level prevalence or trends.

## Optional machine-learning demonstration
TF-IDF and Logistic Regression demonstrate a basic supervised text-classification pipeline. The bundled labels and messages are synthetic and may be repetitive. A small hold-out split is not sufficient evidence of real-world performance. Operational deployment would require licensed representative data, leakage-resistant validation, error analysis, privacy review, monitoring, and human oversight.

## Ethical safeguards
Use only synthetic or authorised data. Do not paste confidential case data into the app. Do not treat a score as proof of malicious intent. Follow local law, organisational policy, and qualified incident-response guidance.
