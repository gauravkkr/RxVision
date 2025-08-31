import pandas as pd
import json

# Load Excel file
excel_path = 'product.xlsx'
df = pd.read_excel(excel_path)

# Expecting columns: 'Generic', 'Brand' (adjust if your columns are named differently)

generic_col = 'Generic Name'
brand_col = None  # No brand column in this sheet



# Build medicine list (no alias map since no brand column)
import re
def is_valid_medicine(val):
    val = str(val).strip()
    # Exclude empty, numbers, and 'Sl No' (case-insensitive)
    if not val or val.lower() == 'sl no':
        return False
    if re.fullmatch(r'\d+', val):
        return False
    return True

generic_names = set(
    val for val in df[generic_col].dropna().astype(str).str.strip() if is_valid_medicine(val)
)
brand_to_generic = {}

# Save as Python code for medicine_list.py
with open('medicine_list_auto.py', 'w', encoding='utf-8') as f:
    f.write('# Auto-generated medicine list\n')
    f.write('MEDICINE_LIST = [\n')

    for med in sorted(generic_names):
        # Clean medicine name: escape quotes, replace newlines, strip
        med_clean = str(med).replace('"', '\"').replace("'", "\\'").replace('\n', ' ').replace('\r', ' ').strip()
        f.write(f'    "{med_clean}",\n')
    f.write(']\n\n')
    f.write('MEDICINE_ALIAS_MAP = {}\n')

print('medicine_list_auto.py generated.')
