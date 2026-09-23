# Understand and extend Data Drift Watch

## The problem
A model trained on older data may receive different data later. This app flags columns that deserve investigation before the model is reused.

## Code path
1. Read the older and newer CSV files with pandas.
2. Compare column names, missing-value rates, and nonblank row counts.
3. For mostly numeric columns, use the Kolmogorov-Smirnov test and show old/new medians.
4. For categorical columns with at most 30 distinct values, use a chi-square test.
5. Mark a field changed when its p-value is below 0.05 or its missing-rate difference is at least 10 percentage points.

## Try it yourself
The bundled sample flags `wait_minutes` and `channel`, while `resolved` remains similar. Edit `sample_new.csv` so its wait times resemble the old file, then rerun and see which flag changes. Upload two real CSV snapshots with the same columns.

## A useful change you could make
Add a chart for the selected column and expose the 0.05 threshold as a control. Test cases with missing columns and too few rows.

## Interview questions
Does a low p-value mean the model failed? No. It indicates evidence of a distribution change; you still need a model evaluation. Why show medians? Statistical significance alone does not show the size or practical meaning of the change. What happens with many columns? Some false alarms are expected when making many tests.
