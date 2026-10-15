from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

def load_incidents():
    df = pd.read_csv(DATA_DIR / "synthetic_incidents.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

def load_messages():
    return pd.read_csv(DATA_DIR / "synthetic_messages.csv").fillna("")

def load_documented_cases():
    df = pd.read_csv(DATA_DIR / "documented_cases_2010_2025.csv")
    df["year"] = pd.to_numeric(df["year"], errors="raise").astype(int)
    return df

def dataset_quality(df):
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }

def category_summary(df):
    return (df.groupby("category", dropna=False)
              .agg(records=("case_id", "count"),
                   average_severity=("severity_score", "mean"))
              .reset_index()
              .sort_values("records", ascending=False))

def annual_counts(df):
    return df.groupby("year").size().reindex(range(2010, 2026), fill_value=0).rename("count").reset_index()

def category_counts(df):
    return df.groupby("category").size().sort_values(ascending=False).rename("count").reset_index()

def sector_counts(df):
    return df.groupby("sector").size().sort_values(ascending=False).rename("count").reset_index()
