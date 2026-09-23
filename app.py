"""Compare two CSV snapshots for changes that may affect an ML model."""
import pandas as pd
import streamlit as st
from scipy.stats import ks_2samp, chi2_contingency

MIN_ROWS = 20

def compare(old, new):
    rows = []
    for column in sorted(set(old.columns) | set(new.columns)):
        if column not in old or column not in new:
            rows.append([column, 'schema', 'missing column', None, None, 'review'])
            continue
        a, b = old[column].dropna(), new[column].dropna()
        missing_a, missing_b = old[column].isna().mean(), new[column].isna().mean()
        if len(a) < MIN_ROWS or len(b) < MIN_ROWS:
            rows.append([column, 'insufficient data', 'need 20 nonblank rows in each file', round(missing_a, 3), round(missing_b, 3), 'review'])
            continue
        numeric_a, numeric_b = pd.to_numeric(a, errors='coerce'), pd.to_numeric(b, errors='coerce')
        if numeric_a.notna().mean() > .9 and numeric_b.notna().mean() > .9:
            statistic, p = ks_2samp(numeric_a.dropna(), numeric_b.dropna())
            detail = f'KS distance {statistic:.2f}; old median {numeric_a.median():.2f}, new median {numeric_b.median():.2f}'
            kind = 'numeric'
        else:
            labels = sorted(set(a.astype(str)) | set(b.astype(str)))
            if len(labels) > 30:
                rows.append([column, 'high-cardinality text', 'more than 30 categories; skipped', round(missing_a, 3), round(missing_b, 3), 'review'])
                continue
            table = pd.DataFrame({'old': a.astype(str).value_counts(), 'new': b.astype(str).value_counts()}).fillna(0).T
            _, p, _, _ = chi2_contingency(table)
            detail = f'category distribution test p={p:.4f}'
            kind = 'category'
        flagged = p < .05 or abs(missing_a - missing_b) >= .1
        rows.append([column, kind, detail, round(missing_a, 3), round(missing_b, 3), 'changed' if flagged else 'similar'])
    return pd.DataFrame(rows, columns=['column', 'type', 'comparison', 'old missing', 'new missing', 'status'])

st.set_page_config(page_title='Data Drift Watch', page_icon='📊', layout='wide')
st.title('Data Drift Watch')
st.caption('Compare two versions of a dataset before reusing an ML model.')
left, right = st.columns(2)
with left:
    old_file = st.file_uploader('Older CSV', type='csv', key='old')
with right:
    new_file = st.file_uploader('Newer CSV', type='csv', key='new')
try:
    old = pd.read_csv(old_file) if old_file else pd.read_csv('sample_old.csv')
    new = pd.read_csv(new_file) if new_file else pd.read_csv('sample_new.csv')
    st.write(f'Older: {len(old)} rows × {len(old.columns)} columns · Newer: {len(new)} rows × {len(new.columns)} columns')
    result = compare(old, new)
    st.dataframe(result, hide_index=True, width='stretch')
    st.download_button('Download comparison', result.to_csv(index=False), 'drift_report.csv', 'text/csv')
except (ValueError, pd.errors.ParserError) as error:
    st.error(f'Could not compare these files: {error}')
st.caption('A flag suggests investigation, not that a model is broken. A p-value alone is sensitive to sample size; compare effect sizes and real examples too.')
