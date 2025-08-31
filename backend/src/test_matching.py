from rapidfuzz import process as fuzzy_process
import sys
import os
sys.path.append(os.path.join('..', 'model'))
from medicine_list_auto import MEDICINE_LIST

# Test matching for "Acela"
test_word = "acela"
print(f"Testing fuzzy matching for: '{test_word}'")
print(f"Medicine list contains {len(MEDICINE_LIST)} medicines")

# Check if Acamprosate is in the list
acamprosate_medicines = [med for med in MEDICINE_LIST if 'acamprosate' in med.lower()]
print(f"Acamprosate medicines found: {acamprosate_medicines}")

# Test different score cutoffs
for cutoff in [30, 40, 50, 60]:
    result = fuzzy_process.extractOne(test_word, MEDICINE_LIST, score_cutoff=cutoff)
    print(f"Score cutoff {cutoff}: {result}")

# Get top 5 matches regardless of score
top_matches = fuzzy_process.extract(test_word, MEDICINE_LIST, limit=5)
print(f"Top 5 matches: {top_matches}")

# Specifically test against Acamprosate
from rapidfuzz import fuzz
acamprosate_score = fuzz.ratio("acela", "acamprosate calcium tablets 333mg")
print(f"Direct score for Acamprosate: {acamprosate_score}")

# Test different matching algorithms
print(f"Partial ratio: {fuzz.partial_ratio('acela', 'acamprosate calcium tablets 333mg')}")
print(f"Token sort ratio: {fuzz.token_sort_ratio('acela', 'acamprosate calcium tablets 333mg')}")
print(f"Token set ratio: {fuzz.token_set_ratio('acela', 'acamprosate calcium tablets 333mg')}")
