# Data Drift Watch

Compare an older and newer CSV for changes that could affect an ML model. The app checks missing columns and values, compares numeric distributions with a Kolmogorov-Smirnov test, and compares small categorical distributions with a chi-square test. Download a report for follow-up.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Try the bundled sample files first. To compare your own datasets, upload each CSV in the app. At least 20 nonblank rows are needed per tested column. Statistical significance does not prove model quality changed; validate the actual model separately. This app does not train a model.

## Learn the code

See [How it works](HOW_IT_WORKS.md) for the data flow, hands-on checks, limitations, and ideas for your own changes.
