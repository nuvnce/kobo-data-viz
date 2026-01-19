import plotly.express as px
import pandas as pd


# --------------------------------------------------
# 📊 Bar chart (catégoriel)
# --------------------------------------------------
'''def bar_chart(
    df: pd.DataFrame,
    x: str ="value",
    y: str = "frequency",
    title: str | None = None
):
    return px.bar(
        df,
        x=x,
        y=y,
        title=title or f"Distribution de {x}"
    )'''
def bar_chart(df, title=None):
    return px.bar(
        df,
        x="label",
        y="frequency",
        title=title or "Distribution"
    )



# --------------------------------------------------
# 🥧 Pie chart
# --------------------------------------------------
'''def pie_chart(
    df: pd.DataFrame,
    names: str ="value",
    values: str = "frequency",
    title: str | None = None
):
    return px.pie(
        df,
        names=names,
        values=values,
        title=title or f"Répartition de {names}"
    )'''
def pie_chart(df, title=None):
    return px.pie(
        df,
        names="label",
        values="frequency",
        title=title or "Répartition"
    )



# --------------------------------------------------
# 📈 Série temporelle
# --------------------------------------------------
def time_series(
    df: pd.DataFrame,
    x: str,
    y: str = "count",
    title: str | None = None
):
    return px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=title or "Évolution des soumissions dans le temps"
    )


# --------------------------------------------------
# 📊 Histogramme (numérique)
# --------------------------------------------------
def histogram(
    df: pd.DataFrame,
    column: str,
    title: str | None = None,
    bins: int = 20
):
    return px.histogram(
        df,
        x=column,
        nbins=bins,
        title=title or f"Distribution de {column}"
    )
