# Data dictionary

## synthetic_incidents.csv
- `case_id`: generated record ID.
- `date`: generated sample date, not a real incident date.
- `category`: specific illustrative threat/case.
- `kind`: broader family for filtering.
- `channel`: illustrative attack/observation channel.
- `severity_score`: synthetic ordinal teaching score from 1 (lower) to 5 (higher); not an assessed real-world severity.
- `status`: illustrative workflow label.
- `potential_impact`: illustrative impact category.
- `scenario_summary`: generated training summary.
- `synthetic_record`: always true for these included rows.

## synthetic_messages.csv
- `message_id`: generated example ID.
- `label`: `suspicious` or `benign` for teaching-only classification.
- `text`: fictional message content.
- `synthetic_example`: always true.
