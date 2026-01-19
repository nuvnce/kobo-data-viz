import pandas as pd
from typing import List, Dict, Any


def flatten_submissions(
    submissions: List[Dict[str, Any]],
    sep: str = "__"
) -> pd.DataFrame:
    """
    Aplatit les soumissions Kobo (JSON) en DataFrame pandas.

    :param submissions: Liste de soumissions Kobo
    :param sep: Séparateur pour les champs imbriqués
    :return: DataFrame pandas
    """

    if not submissions:
        return pd.DataFrame()

    # 1️⃣ Aplatir les structures imbriquées
    df = pd.json_normalize(submissions, sep=sep)

    # 2️⃣ Gérer les select_multiple (listes → string)
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(
                lambda x: ", ".join(map(str, x)) if isinstance(x, list) else x
            )

    # 3️⃣ Conversion dates Kobo si présentes
    date_columns = [
        "_submission_time",
        "_start",
        "_end"
    ]

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # 4️⃣ Trier par date de soumission si dispo
    if "_submission_time" in df.columns:
        df = df.sort_values("_submission_time")

    return df
