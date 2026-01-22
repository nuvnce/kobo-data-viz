from typing import Callable, Dict, List, Optional


def fetch_all_pages(
    fetch_fn: Callable[[Optional[str]], Dict]
) -> List[Dict]:
    """
    Récupère toutes les pages d'une API paginée Kobo.

    fetch_fn doit être une fonction qui prend un endpoint (ou None)
    et retourne un JSON avec 'results' et 'next'.
    """
    all_results = []
    next_endpoint = None

    while True:
        data = fetch_fn(next_endpoint)
        all_results.extend(data.get("results", []))

        next_endpoint = data.get("next")
        if not next_endpoint:
            break

    return all_results
