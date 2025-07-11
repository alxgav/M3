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
    return (pd,)


@app.cell
def _(mo):
    mo.md(r"""clean first file""")
    return


@app.cell
def _(pd):
    p_data = pd.read_csv("P4Xe.txt", sep="\t", encoding="iso-8859-1", header=None)
    p_data_clean = p_data[[1,2,4,5,10,27,21,22,23]].copy()
    p_data_clean.columns = ['artikel', 'description', 'menge', 'datum', 'note', 'time_work', 'w', 'h', 'w2']
    p_data_clean['datum'] = p_data_clean['datum'].str.split().str[0]
    p_data_clean[['A1', 'A2']] = p_data_clean['artikel'].str.extract(r'^(.*?)(?:[-B](\d+))?$')
    p_data_clean['A2'] = p_data_clean['A2'].fillna('')
    return (p_data_clean,)


@app.cell
def _(p_data_clean):
    p_data_clean.head(20)
    return


@app.cell
def _(pd):
    p_store = pd.read_csv("Lagerspiegel_full.txt", sep=";", encoding="iso-8859-1")
    p_store = p_store[p_store['Artikel'].str.contains(r'[A-Za-z\-]')]
    exclude_patterns = "leer|empty|n/a"
    p_store = p_store[~p_store["Artikel"].str.contains(exclude_patterns, na=False, case=False)].copy()
    p_store = p_store[p_store['Artikel'].str.contains(r'[-A]', na=False)].copy()
    p_store[['A1', 'A2']] = p_store['Artikel'].str.extract(r'^(.*?)[-A]([^-A]*)$')
    p_store_selected = p_store[['Artikel', 'A1', "A2", 'Menge', 'FachName']]


    return (p_store_selected,)


@app.cell
def _(p_store_selected):
    p_store_selected.tail(10)
    return


if __name__ == "__main__":
    app.run()
