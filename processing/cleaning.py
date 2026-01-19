import pandas as pd
from typing import List, Optional


# --------------------------------------------------
# 🧹 Nettoyage des colonnes techniques Kobo
# --------------------------------------------------
DEFAULT_HIDDEN_COLUMNS = [
    "_id",
    "_uuid",
    "_attachments",
    "_notes",
    "_status",
    "_validation_status",
    "_submitted_by",
    "_xform_id_string",
    "_version"
]


'''def drop_technical_columns(
    df: pd.DataFrame,
    extra_cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Supprime les colonnes techniques Kobo inutiles pour l'analyse.
    """
    cols_to_drop = set(DEFAULT_TECH_COLUMNS)

    if extra_cols:
        cols_to_drop.update(extra_cols)

    existing = [c for c in cols_to_drop if c in df.columns]

    return df.drop(columns=existing, errors="ignore")
'''
    
def hide_columns(
    df: pd.DataFrame,
    hidden_cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Masque les colonnes non essentielles à la visualisation.
    """
    if not hidden_cols:
        hidden_cols = DEFAULT_HIDDEN_COLUMNS

    visible_cols = [c for c in df.columns if c not in hidden_cols]
    return df[visible_cols]



# --------------------------------------------------
# 🏷️ Nettoyage des noms de colonnes
# --------------------------------------------------
def clean_column_names(
    df: pd.DataFrame,
    sep: str = "__"
) -> pd.DataFrame:
    """
    Nettoie les noms de colonnes :
    - minuscules
    - espaces → _
    - suppression des préfixes de groupe
    """
    new_columns = {}

    for col in df.columns:
        clean_col = col.lower()

        if sep in clean_col:
            clean_col = clean_col.split(sep)[-1]

        clean_col = (
            clean_col
            .replace(" ", "_")
            .replace("-", "_")
        )

        new_columns[col] = clean_col

    return df.rename(columns=new_columns)


# --------------------------------------------------
# 🧠 Gestion des valeurs manquantes
# --------------------------------------------------
def handle_missing_values(
    df: pd.DataFrame,
    fill_text: str = "Non renseigné"
) -> pd.DataFrame:
    """
    Remplit les valeurs manquantes selon le type de colonne.
    """
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna(fill_text)
        else:
            df[col] = df[col].fillna(0)

    return df


# --------------------------------------------------
# 🔢 Correction automatique des types
# --------------------------------------------------
def infer_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convertit automatiquement les colonnes numériques stockées en texte.
    """
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass

    return df


# --------------------------------------------------
# ⏱️ Features temporelles utiles
# --------------------------------------------------
def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute des colonnes dérivées à partir de _submission_time.
    """
    if "_submission_time" in df.columns:
        df["submission_date"] = df["_submission_time"].dt.date
        df["submission_month"] = df["_submission_time"].dt.to_period("M").astype(str)
        df["submission_year"] = df["_submission_time"].dt.year
        df["submission_weekday"] = df["_submission_time"].dt.day_name()

    return df


# --------------------------------------------------
# 🚀 Pipeline complet de nettoyage
# --------------------------------------------------
def clean_kobo_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline complet de nettoyage des données Kobo.
    """
    #df = drop_technical_columns(df)
    df = clean_column_names(df)
    df = clean_column_names(df)
    df = infer_numeric_columns(df)
    df = handle_missing_values(df)
    df = add_time_features(df)

    return df

