import csv
from rich import print


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


# data = []
#
# with open(p4xe, "r", encoding="iso-8859-1") as f:
#     lines = f.readlines()
#     for item in lines:
#         fields = item.strip().split("\t")
#         selected_fields = [
#             fields[i] if i < len(fields) else "" for i in selected_indices
#         ]
#         labeled_fields = dict(zip(field_names, selected_fields))
#         data.append(labeled_fields)

# print(data)
