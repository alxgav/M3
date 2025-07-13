import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import pandas as pd
    import re
    return pd, re


@app.cell
def _(mo):
    mo.md(r"""clean first file""")
    return


@app.cell
def _(re):
    def safe_split(x):
        parts = re.split(r"-|A|B", x)
        return (parts[0] if len(parts) > 0 else "", parts[1] if len(parts) > 1 else "")
    return (safe_split,)


@app.cell
def _(pd, safe_split):
    p_data = pd.read_csv("P4Xe.txt", sep="\t", encoding="iso-8859-1", header=None)
    p_data_clean = p_data[[1,2,4,5,10,27,21,22,23]].copy()
    p_data_clean.columns = ['artikel', 'description', 'menge', 'datum', 'note', 'time_work', 'w', 'h', 'w2']
    p_data_clean['datum'] = p_data_clean['datum'].str.split().str[0]
    p_data_clean['time_work'] = (
        p_data_clean['time_work']
        .str.replace(',', '.', regex=False)
        .pipe(pd.to_numeric, errors='coerce')
        .div(60).round(2)  # Convert minutes to hours
    )
    p_data_clean[["A1", "A2"]] = p_data_clean["artikel"].apply(lambda x: safe_split(x)).apply(pd.Series)

    return (p_data_clean,)


@app.cell
def _(p_data_clean):
    p_data_clean.head(40)
    return


@app.cell
def _(pd, safe_split):
    p_store = pd.read_csv("Lagerspiegel_full.txt", sep=";", encoding="iso-8859-1")
    p_store = p_store[p_store['Artikel'].str.contains(r'[A-Za-z\-]')]
    exclude_patterns = "leer|empty|n/a"
    p_store = p_store[~p_store["Artikel"].str.contains(exclude_patterns, na=False, case=False)].copy()
    p_store[["A1", "A2"]] = p_store["Artikel"].apply(
            lambda x: safe_split(x)
        ).apply(pd.Series)
    p_store["FachName"] = p_store["FachName"].astype(str)

        # Detect "Station" (flexible matching)
    p_store["Station"] = p_store["FachName"].str.contains(
        r'(?i)station',  # Case-insensitive regex
        regex=True,
        na=False
    )
    p_store_selected = p_store[['Artikel', 'A1', "A2", 'Menge', 'FachName', 'Station']]


    return (p_store_selected,)


@app.cell
def _(p_store_selected):
    p_store_selected.head(1500)
    return


@app.cell
def _(p_store_selected):
    stations = p_store_selected['FachName'].str.contains(r'Station 0[1-9]|Station 1[0-2]')
    p_store_station = p_store_selected[stations][["Artikel", "Menge", "FachName"]].sort_values(by='FachName')
    return (p_store_station,)


@app.cell
def _(p_store_station):
    p_store_station.head(100)
    return


if __name__ == "__main__":
    app.run()
