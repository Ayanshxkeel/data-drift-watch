# Data Drift Watch

Compare two CSV snapshots and flag data changes worth investigating before reusing a machine learning model.

**Purpose:** A model may receive new data with different columns, missing values, or distributions. This app produces an initial comparison report; it does not measure model accuracy.

## Features

- Compares older and newer CSV files, with samples for a first run.
- Finds missing columns and changes in missing-value rates.
- Compares mostly numeric columns with a Kolmogorov–Smirnov test and their medians.
- Compares columns with up to 30 categories using a chi-square test.
- Downloads findings as a CSV report.

## Run locally

```bash
git clone https://github.com/Ayanshxkeel/data-drift-watch.git
cd data-drift-watch
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. On Windows, activate with `.venv\Scripts\activate`.

## Try it

The bundled `sample_old.csv` and `sample_new.csv` load automatically. `wait_minutes` and `channel` should be **changed**, while `resolved` should be **similar**. Download the report, then upload two versions of a CSV with comparable columns.

## How it works

`compare()` checks each column in both files and requires at least 20 nonblank rows per tested column. Numeric columns use a distribution test; small categorical columns use a count-based test. A field is marked changed when its p-value is below 0.05 or its missing-rate difference is at least 10 percentage points. See [How it works](HOW_IT_WORKS.md) for the code flow.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | CSV comparison and Streamlit report |
| `sample_old.csv`, `sample_new.csv` | Example snapshots |
| `requirements.txt` | Python dependencies |
| `HOW_IT_WORKS.md` | Explanation and hands-on changes |

## Limits

A flag is **not proof that a model has failed**; evaluate the model separately. P-values are sensitive to sample size, and testing many fields can create false alarms. High-cardinality text fields are skipped. Use appropriate data if hosting the app publicly.
