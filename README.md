# Kobo Data Visualizer

A Python application to visualize data collected with KoboToolbox forms using an API key.

## Features
- Connects to KoboToolbox via API token
- Lists all available forms
- Loads form submissions dynamically
- Cleans and flattens Kobo JSON data
- Interactive visualizations (bar charts, pie charts, time series)
- KPI indicators (submission count, validation status, completion rate)

## Tech Stack
- Python
- Streamlit
- Pandas
- Plotly

## Project Structure

kobo-data-viz/
├── app.py
├── kobo/
├── processing/
├── viz/
├── utils/
├── tests/
├── requirements.txt
├── .env.example
└── README.md


## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/kobo-data-viz.git
cd kobo-data-viz

2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate     # Windows

3. Install dependencies
pip install -r requirements.txt

4. Run the application
streamlit run app.py

Security Notes

API keys are never stored

No credentials are committed to the repository

Environment variables are managed via .env

Status

MVP – stable and functional.
Architecture and tests will be improved in future versions.


👉 C’est **suffisant**, clair, et honnête.

---

## 5️⃣ Initialisation Git (local)

À la racine du projet :

```bash
git init
git status
