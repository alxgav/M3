from rich import print

p4xe = 'P4Xe.txt'
store = 'Lagerspiegel_full.txt'

selected_indices = [1, 2, 4, 5, 10, 27, 21, 22, 23]

field_names = [
    "Article", "Description", "psc", "date_end",
    "note", "time", "L", "H", "D"
]

with open(p4xe, 'r') as f:
    lines = f.readlines()
    for item in lines:
        fields = item.strip().split('\t')
        selected_fields = [fields[i] if i < len(fields) else '' for i in selected_indices]
        labeled_fields = dict(zip(field_names, selected_fields))
        print(labeled_fields)
        



# with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
#     lines1 = f1.readlines()
#     lines2 = f2.readlines()

# if lines1 == lines2:
#     print("Files are identical.")
# else:
#     print("Files are different.")
