from rapidfuzz import fuzz
import sys
import os
sys.path.append(os.path.join('..', 'model'))
from medicine_list_auto import MEDICINE_LIST

# Test the new partial matching approach
test_word = "acela"
print(f"Testing partial fuzzy matching for: '{test_word}'")

best_match = None
best_score = 0
for med in MEDICINE_LIST:
    score = fuzz.partial_ratio(test_word, med.lower())
    if score > best_score and score >= 60:
        best_score = score
        best_match = med

print(f"Best partial match: '{best_match}' with score {best_score}")

# Also test some other common partial matches
test_cases = ["acela", "acetam", "amox", "ibupro"]
for test in test_cases:
    best_match = None
    best_score = 0
    for med in MEDICINE_LIST:
        score = fuzz.partial_ratio(test, med.lower())
        if score > best_score and score >= 60:
            best_score = score
            best_match = med
    print(f"'{test}' -> '{best_match}' (score: {best_score})")
