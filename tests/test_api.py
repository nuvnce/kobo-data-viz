import pytest
from kobo.client import KoboClient

import sys
import os

# Ajoute la racine du projet au PYTHONPATH
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

def test_client_requires_api_key():
    with pytest.raises(ValueError):
        KoboClient(api_key="")


def test_client_init():
    client = KoboClient(api_key="fake_key")
    assert client.api_key == "fake_key"
