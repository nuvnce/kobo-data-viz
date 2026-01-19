import pandas as pd
from typing import Dict


# --------------------------------------------------
# 📈 Indicateurs globaux
# --------------------------------------------------
def global_metrics(df: pd.DataFrame) -> Dict[str, int]:
    """
    Indicateurs globaux sur les soumissions.
    """
    metrics = {
        "total_submissions": len(df),
    }

    if "_validation_status" in df.columns:
        metrics["validated"] = (df["_validation_status"] == "validated").sum()
        metrics["not_validated"] = (df["_validation_status"] != "validated").sum()

    if "_status" in df.columns:
        metrics["submitted"] = (df["_status"] == "submitted").sum()
        metrics["draft"] = (df["_status"] == "draft").sum()

    return metrics


# --------------------------------------------------
# 📊 Distribution par colonne
# --------------------------------------------------
'''def value_counts(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if column not in df.columns:
        raise ValueError(f"Colonne '{column}' introuvable")

    return (
        df[column]
        .value_counts(dropna=False)
        .reset_index()
        .rename(columns={
            "index": "value",
            column: "frequency"
        })
    )'''
def value_counts(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if column not in df.columns:
        raise ValueError(f"Colonne '{column}' introuvable")

    vc = df[column].value_counts(dropna=False)

    return pd.DataFrame({
        "label": vc.index.astype(str),
        "frequency": vc.values
    })



# --------------------------------------------------
# ⏱️ Soumissions dans le temps
# --------------------------------------------------
def submissions_over_time(
    df: pd.DataFrame,
    freq: str = "D"
) -> pd.DataFrame:
    """
    Agrège les soumissions par période.
    freq: D (jour), M (mois), Y (année)
    """
    if "_submission_time" not in df.columns:
        raise ValueError("_submission_time absent")

    return (
        df
        .set_index("_submission_time")
        .resample(freq)
        .size()
        .reset_index(name="count")
    )


# --------------------------------------------------
# 🧪 Taux de complétion par colonne
# --------------------------------------------------
def completion_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule le taux de complétion par question.
    """
    total = len(df)

    rates = []
    for col in df.columns:
        non_null = df[col].notna().sum()
        rates.append({
            "column": col,
            "completion_rate": round((non_null / total) * 100, 2)
        })

    return pd.DataFrame(rates).sort_values("completion_rate", ascending=False)
