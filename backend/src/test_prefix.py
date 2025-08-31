import sys
import os
sys.path.append(os.path.join('..', 'model'))
from medicine_list_auto import MEDICINE_LIST

# Test the new prefix matching logic
test_word = "acela"
clean_line = test_word.lower().strip()

print(f"Testing prefix matching for: '{test_word}'")
print(f"Clean line: '{clean_line}'")

# Test 2-letter prefix
prefix2 = clean_line[:2]
print(f"2-letter prefix: '{prefix2}'")

direct_match = None
for med in MEDICINE_LIST:
    med_lower = med.lower()
    if med_lower.startswith(prefix2):
        direct_match = med
        print(f"[FOUND] 2-letter prefix matched '{test_word}' to '{med}'")
        break

if not direct_match:
    print("No 2-letter prefix match found")
else:
    print(f"SUCCESS: {direct_match}")

# Also test 3-letter
prefix3 = clean_line[:3] if len(clean_line) >= 3 else clean_line
print(f"3-letter prefix: '{prefix3}'")
for med in MEDICINE_LIST:
    med_lower = med.lower()
    if med_lower.startswith(prefix3):
        print(f"[FOUND] 3-letter prefix matched '{test_word}' to '{med}'")
        break
