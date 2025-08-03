import pandas as pd
import re
from app.settings import BASE_DIR

# import logging
from app.settings import logger as log
# logging.basicConfig(level=logging.DEBUG)
from rich import print

#
def get_data(filename: str, sep: str = ";", header=None) -> pd.DataFrame:
    return pd.read_csv(filename, sep=sep, encoding="iso-8859-1")

def safe_split(x):
    parts = re.split(r"-|A|B", x)
    return (parts[0] if len(parts) > 0 else "", parts[1] if len(parts) > 1 else "")

# this function return dataFrame from Lagerspiegel_full.txt

def get_store_data() -> pd.DataFrame:
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
    return p_store[['Artikel', 'A1', "A2", 'Menge', 'FachName', 'Station']]

def get_regal_data() -> pd.DataFrame:
    df_regal = get_data("app/uploads/Lagerspiegel_full.txt", sep=";")
    exclude_patterns = "leer|empty|n/a"
    df_regal_clean = df_regal[~df_regal["Artikel"].str.contains(exclude_patterns, na=False, case=False)].copy()
    df_regal_clean[["artikel_split", "artikel_split_2"]] = df_regal_clean["Artikel"].apply(
        lambda x: safe_split(x)
    ).apply(pd.Series)
    df_regal_clean = df_regal_clean[["Artikel", "artikel_split" , "artikel_split_2", "Menge", "FachName"]]
    log.info("Regal data loaded")
    return df_regal_clean

# this function return dataFrame from P4Xe.txt

def get_job_data() -> pd.DataFrame:
    df_work = pd.read_csv("app/uploads/P4Xe.txt", sep="\t", encoding="iso-8859-1", header=None)
    m_df_clean = df_work[[1,2,4,5,10,27,21,22,23]].copy()
    m_df_clean.columns = ['artikel', 'description', 'menge', 'datum', 'note', 'time_work', 'w', 'h', 'w2']
    m_df_clean['time_work'] = (
        m_df_clean['time_work']
        .str.replace(',', '.', regex=False)
        .pipe(pd.to_numeric, errors='coerce')
        .div(60).round(2)  # Convert minutes to hours
    )
    m_df_clean[["artikel_split", "artikel_split_2"]] = m_df_clean["artikel"].apply(
        lambda x: safe_split(x)).apply(pd.Series)
    log.info("P4Xe data loaded")
    return m_df_clean

def merge_data(df_regal = get_regal_data(), df_job = get_job_data()) -> pd.DataFrame:
    merged_df = pd.merge(df_job,df_regal, on='artikel_split', how='left')
    merged_df['note'] = merged_df['note'].fillna('')
    # merged_df.sort_values(by='datum', inplace=True)
    merged_df.to_csv('app/uploads/merged_data.csv', index=False, sep=';')
    return merged_df


#  responce data for stations
def get_stations() -> list:
    df = get_regal_data()
    filter_condition = df['FachName'].str.contains(r'Station 0[1-9]|Station 1[0-2]')
    sorted_df = df[filter_condition][["Artikel", "Menge", "FachName"]].sort_values(by='FachName')
    result = (
        sorted_df.groupby('FachName', as_index=False)
        .agg(list)
    )
    response = [
        {
            "Station": row.FachName,
            "material": [{"artikel": artikel, "menge": menge} for artikel, menge in zip(row.Artikel, row.Menge)]
        }
        for row in result.itertuples(index=False)
    ]
    return response

def get_final_data(df: pd.DataFrame = merge_data()) -> list:
    # # Group by 'artikel'
    grouped_df = df.groupby('artikel', as_index=False)
    response = []
    filtered_materials = []

    # logging.debug(f"Initial DataFrame: {df.head(10)}")
    for article, group in grouped_df:
        # logging.debug(f"Processing group for article: {article}")
        description = group['description'].iloc[0]
        menge = group['menge'].iloc[0]
        dataWork = group['datum'].iloc[0]
        note = group['note'].iloc[0] if not pd.isna(group['note'].iloc[0]) else ""
        time_work = group['time_work'].iloc[0]

        # Extract materials
        materials = group[['Artikel', 'FachName', 'Menge', 'artikel_split_2_x', 'artikel_split_2_y']].copy()
        # materials = materials[materials['artikel_split_2_x'] == materials['artikel_split_2_y']]

        # materials = materials[
        #     (materials['artikel_split_2_x'] == materials['artikel_split_2_y']) &  # Equal values
        #     ~((materials['artikel_split_2_x'] == '') & (materials['artikel_split_2_y'] == ''))  # Exclude where both are empty
        #     ]
        # Split the article number
        article_parts = re.split("-|B", article)

        # Filter materials based on the article parts
        if len(article_parts)== 2:
            if article_parts[1].isdigit():
                filtered_materials = materials[
                    materials['artikel_split_2_y'].notna() &
                    materials['artikel_split_2_y'].astype(str).str.isdigit()
                    ]
            else:
                filtered_materials = materials[
                    materials['artikel_split_2_y'].notna() &
                    materials['artikel_split_2_y'].astype(str).str.contains('E')
                    ]

            # Convert filtered_materials to a list of dictionaries for JSON serialization
        filtered_materials_list = filtered_materials.to_dict(orient='records')
        # Append to response
        station = any('Station' in record['FachName'] for record in filtered_materials_list)
        response.append({
            "artikel": article,
            "description": description,
            "menge": int(menge),
            "dataWork": str(dataWork),  # Ensure date is serializable
            "note": note,
            "time_work": time_work,
            "materials": filtered_materials_list,
            "w": group['w'].iloc[0],
            "h": group['h'].iloc[0],
            "w2": group['w2'].iloc[0],
            "station": station
        })

    return response
