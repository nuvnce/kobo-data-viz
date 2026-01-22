import os
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# 🌐 Kobo API
# --------------------------------------------------
KOBO_API_URL = os.getenv(
    "KOBO_API_URL",
    "https://kf.kobotoolbox.org/api/v2"
)

DEFAULT_TIMEOUT = int(
    os.getenv("DEFAULT_TIMEOUT", 30)
)

# --------------------------------------------------
# 📊 App settings
# --------------------------------------------------
APP_NAME = "Kobo Data Visualizer"
APP_VERSION = "0.1.0"
