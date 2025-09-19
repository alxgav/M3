import csv
from rich import print
import re


p4xe = "P4Xe.txt"
store = "Lagerspiegel_full.txt"
#
selected_indices = [1, 2, 4, 5, 10, 27, 21, 22, 23]

field_names = [
    "Article",
    "Description",
    "psc",
    "date_end",
    "note",
    "time",
    "L",
    "H",
    "D",
    "materials"
]


def extract_csv_columns(file_path, columns, delimiter=";") -> list[dict]:

    data = []
    try:
        with open(file_path, "r", encoding="iso-8859-1", newline="") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                filtered_row = {col: row[col] for col in columns if col in row}
                data.append(filtered_row)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except KeyError as e:
        print(f"Error: Column {e} not found in '{file_path}'. Check column names.")
    except StopIteration:
        print(f"Error: The file '{file_path}' is empty or has no header.")
    return data

store = extract_csv_columns(store, ["Artikel", "Menge", "FachName"])

def extract_article_number(article_field) -> list:
    return [re.split(r"[-BA]", article_field)[0], re.split(r"[-BA]", article_field)[0]]

def extract_selected_fields(file_path, selected_indices, field_names):
    data = []
    with open(file_path, "r", encoding="iso-8859-1") as f:
        lines = f.readlines()
        for item in lines:
            fields = item.strip().split("\t")
            selected_fields = [
                fields[i] if i < len(fields) else "" for i in selected_indices
            ]
           

            article = extract_article_number(selected_fields[0])

            # Find matching entry in store by "Artikel"
            material_entries = [entry for entry in store if article[0] in entry["Artikel"] ] 
            if material_entries:
                material_info = material_entries
            else:
                material_info = []
            if len(selected_fields) < len(field_names):
                selected_fields.append(material_info)
            else:
                selected_fields[-1] = material_info
            labeled_fields = dict(zip(field_names, selected_fields))
            data.append(labeled_fields)
    return data

data = extract_selected_fields(p4xe, selected_indices, field_names)
# print(data)

for item in data:
    # for key, value in item.items():
    #     if key == "Article":
    #         value = re.split(r"[-BA]", value)[1]
    #         print (f"{key}: {value}")
    #         break
    artikel = re.split(r"[-BA]", item["Article"])[1]
    print(artikel)
    # for material in item["materials"]:
    #     if artikel in material["Artikel"]:
    #         print(f"Article: {item['Article']}, Material: {material['Artikel']}, Menge: {material['Menge']}, FachName: {material['FachName']}")
            
