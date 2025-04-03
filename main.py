# main.py

import json
import os
import sys
from archetype_engine.assign_archetype import assign_user_profile
from archetype_engine.metrics import compute_metrics
from archetype_engine.scoring_modules import calculate_archetype_scores

# Default sample file if none provided
DEFAULT_SAMPLE = "/Users/vishn/Desktop/financial-archetype-engine/archetype_engine/subscription_enthusiast.json"

# Allow passing a sample file as argument
if len(sys.argv) > 1:
    DATA_FILE = sys.argv[1]
else:
    DATA_FILE = DEFAULT_SAMPLE

if not os.path.exists(DATA_FILE):
    print(f"❌ Error: File '{DATA_FILE}' not found.")
    exit(1)

print(f"Processing transactions from: {os.path.basename(DATA_FILE)}")

with open(DATA_FILE, "r") as f:
    transactions = json.load(f)

print(f"Loaded {len(transactions)} transactions")

# Calculate metrics separately for debugging
metrics = compute_metrics(transactions)

# Print key metrics for debugging
print("\n------- Key Metrics -------")
print(f"Dining Ratio: {metrics.get('dining_ratio', 0):.2%}")
print(f"Shopping Ratio: {metrics.get('shopping_ratio', 0):.2%}")
print(f"Entertainment Ratio: {metrics.get('entertainment_ratio', 0):.2%}")
print(f"Travel Ratio: {metrics.get('travel_ratio', 0):.2%}")
print(f"Savings Rate: {metrics.get('savings_rate', 0):.2%}")
print(f"Total Discretionary Ratio: {metrics.get('total_discretionary_ratio', 0):.2%}")
print(f"Premium Spend Ratio: {metrics.get('premium_spend_ratio', 0):.2%}")

# Calculate raw scores
raw_scores = calculate_archetype_scores(metrics)
print("\n------- Raw Scores (Pre-Softmax) -------")
for archetype, score in sorted(raw_scores.items(), key=lambda x: x[1], reverse=True):
    print(f"{archetype}: {score:.2f}")

# Get the full profile
result = assign_user_profile(transactions)

# Save the result to output.json
with open("output.json", "w") as f:
    json.dump(result, f, indent=2)

# Print a summary of the results
print("\n------- Archetype Analysis Results -------")
print(f"Top Archetype: {result['top_archetype']}")
print(f"Confidence: {result['confidence']:.2f}") 
print(f"Explanation: {result['explanation']}")
print("\nTop 3 Archetypes:")
for idx, item in enumerate(result['ranked_scores'][:3], 1):
    print(f"{idx}. {item['archetype']} ({item['score']:.2f})")

print(f"\nFull results saved to output.json")
