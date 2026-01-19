import requests
from typing import List, Dict, Optional


class KoboClient:
    """
    Client pour interagir avec l'API KoboToolbox.
    """

    BASE_URL = "https://kf.kobotoolbox.org/api/v2"

    def __init__(self, api_key: str, timeout: int = 30):
        if not api_key:
            raise ValueError("API Key Kobo requise")

        self.api_key = api_key
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        })

    # --------------------------------------------------
    # 🔹 Requête générique
    # --------------------------------------------------
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.BASE_URL}{endpoint}"

        response = self.session.get(
            url,
            params=params,
            timeout=self.timeout
        )

        if response.status_code == 401:
            raise PermissionError("API Key invalide ou expirée")

        if not response.ok:
            raise RuntimeError(
                f"Erreur API Kobo [{response.status_code}] : {response.text}"
            )

        return response.json()

    # --------------------------------------------------
    # 📋 Lister les formulaires
    # --------------------------------------------------
    def list_forms(self) -> List[Dict]:
        """
        Retourne la liste des formulaires (assets type 'survey').
        """
        data = self._get("/assets/")

        forms = [
            {
                "uid": asset["uid"],
                "name": asset["name"],
                "date_created": asset.get("date_created"),
                "date_modified": asset.get("date_modified"),
            }
            for asset in data.get("results", [])
            if asset.get("asset_type") == "survey"
        ]

        return forms

    # --------------------------------------------------
    # 📥 Récupérer toutes les soumissions (pagination)
    # --------------------------------------------------
    def get_submissions(
        self,
        asset_uid: str,
        page_size: int = 1000,
        include_meta: bool = True
    ) -> List[Dict]:
        """
        Récupère toutes les soumissions d'un formulaire Kobo.

        :param asset_uid: UID du formulaire
        :param page_size: Nombre d'éléments par page
        :param include_meta: Inclure métadonnées Kobo (_submission_time, etc.)
        """
        if not asset_uid:
            raise ValueError("asset_uid requis")

        endpoint = f"/assets/{asset_uid}/data/"
        params = {
            "limit": page_size
        }

        all_results = []

        while endpoint:
            data = self._get(endpoint, params=params)

            results = data.get("results", [])
            all_results.extend(results)

            endpoint = data.get("next")
            params = None  # Les pages suivantes contiennent déjà les paramètres

        if not include_meta:
            all_results = [
                {k: v for k, v in r.items() if not k.startswith("_")}
                for r in all_results
            ]

        return all_results

    # --------------------------------------------------
    # 🧪 Vérifier la connexion
    # --------------------------------------------------
    def test_connection(self) -> bool:
        """
        Teste si l'API Key est valide.
        """
        try:
            self._get("/assets/")
            return True
        except Exception:
            return False
        
# Example d'utilisation:
# client = KoboClient(api_key="votre_api_key")
# forms = client.list_forms() 