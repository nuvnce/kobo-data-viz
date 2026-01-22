from typing import Any


def safe_str(value: Any) -> str:
    """
    Convertit une valeur en string sans casser.
    """
    try:
        return str(value)
    except Exception:
        return ""


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Tronque un texte long pour l'affichage.
    """
    if not isinstance(text, str):
        return ""
    return text if len(text) <= max_length else text[:max_length] + "..."
