# main.py

import json
import os
from archetype_engine.assign_archetype import assign_user_profile
from archetype_engine.archetype_explanations import ARCHETYPE_EXPLANATIONS, ARCHETYPE_TAGS


# File containing parsed transaction data (from SMS or test JSON)
DATA_FILE = "/Users/vishn/financial-archetype-engine/archetype_engine/sample_test_retail_balanced.json"  # Change to your desired test file name

# Ensure the file exists
if not os.path.exists(DATA_FILE):
    print(f"❌ Error: File '{DATA_FILE}' not found.")
    exit(1)

# Load transaction data
with open(DATA_FILE, "r") as f:
    transactions = json.load(f)

# Run the archetype assignment engine
result = assign_user_profile(transactions)

# Output the final profile result
print(json.dumps(result, indent=2))
