import streamlit as st
import pandas as pd

from kobo.client import KoboClient
from processing.flatten import flatten_submissions
from processing.cleaning import clean_kobo_dataframe
from viz.metrics import (
    global_metrics,
    value_counts,
    submissions_over_time,
    completion_rate
)
from viz.charts import (
    bar_chart,
    pie_chart,
    time_series,
    histogram
)

# --------------------------------------------------
# ⚙️ Configuration Streamlit
# --------------------------------------------------
st.set_page_config(
    page_title="Kobo Data Visualizer",
    layout="wide"
)

st.title("📊 Kobo Data Visualizer")
st.caption("Visualisation des données KoboToolbox via API")

# --------------------------------------------------
# 🔑 API KEY (sécurisé)
# --------------------------------------------------
api_key = st.text_input(
    "🔑 Entrez votre API Key Kobo",
    type="password"
)

if not api_key:
    st.info("Veuillez saisir votre API Key pour continuer.")
    st.stop()

# --------------------------------------------------
# 📋 Connexion & chargement des formulaires
# --------------------------------------------------
try:
    client = KoboClient(api_key)
    if not client.test_connection():
        st.error("API Key invalide ou problème de connexion.")
        st.stop()

    forms = client.list_forms()

except Exception as e:
    st.error(str(e))
    st.stop()

if not forms:
    st.warning("Aucun formulaire trouvé.")
    st.stop()

form_names = [f["name"] for f in forms]

selected_form = st.selectbox(
    "📋 Choisissez un formulaire",
    form_names
)

form_uid = next(
    f["uid"] for f in forms if f["name"] == selected_form
)

# --------------------------------------------------
# 📥 Chargement des soumissions
# --------------------------------------------------
with st.spinner("Chargement des soumissions..."):
    submissions = client.get_submissions(form_uid)

if not submissions:
    st.warning("Aucune soumission pour ce formulaire.")
    st.stop()

# --------------------------------------------------
# 🧹 Pipeline Data
# --------------------------------------------------
df_raw = flatten_submissions(submissions)
df = clean_kobo_dataframe(df_raw)

# --------------------------------------------------
# 👀 Aperçu des données
# --------------------------------------------------
with st.expander("👀 Aperçu des données"):
    st.dataframe(df.head(50))

# --------------------------------------------------
# 📊 KPI
# --------------------------------------------------
st.subheader("📌 Indicateurs clés")

metrics = global_metrics(df)

cols = st.columns(len(metrics))
for col, (key, value) in zip(cols, metrics.items()):
    col.metric(key.replace("_", " ").title(), value)

# --------------------------------------------------
# 📈 Visualisations
# --------------------------------------------------
st.subheader("📈 Visualisations")

# Colonnes exploitables
categorical_cols = [
    c for c in df.columns
    if df[c].dtype == "object" and not c.startswith("_")
]

numeric_cols = [
    c for c in df.columns
    if pd.api.types.is_numeric_dtype(df[c])
]

# ---- Sélecteur de variable catégorielle
if categorical_cols:
    cat_col = st.selectbox(
        "Variable catégorielle",
        categorical_cols
    )



    counts_df = value_counts(df, cat_col)

    st.plotly_chart(
        bar_chart(
            counts_df,
            title=f"Distribution de {cat_col}"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        pie_chart(
            counts_df,
            title=f"Répartition de {cat_col}"
        ),
        use_container_width=True
    )


# ---- Variable numérique
if numeric_cols:
    num_col = st.selectbox(
        "Variable numérique",
        numeric_cols
    )

    st.plotly_chart(
        histogram(df, num_col),
        use_container_width=True
    )

# ---- Série temporelle
if "_submission_time" in df.columns:
    st.subheader("⏱️ Évolution des soumissions")

    FREQ_MAPPING = {
        "Jour": "D",
        "Mois": "M",
        "Année": "Y"
    }

    freq_label = st.selectbox(
        "Période",
        list(FREQ_MAPPING.keys())
    )

    freq = FREQ_MAPPING[freq_label]

    time_df = submissions_over_time(df, freq=freq)

    st.plotly_chart(
        time_series(time_df, "_submission_time"),
        use_container_width=True
    )

# --------------------------------------------------
# 🧪 Taux de complétion
# --------------------------------------------------
with st.expander("🧪 Taux de complétion des questions"):
    completion_df = completion_rate(df)
    st.dataframe(completion_df)
