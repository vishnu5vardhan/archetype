# archetype_weights.py

"""
This file defines how much each metric contributes to each archetype's score.
You can tweak these values to fine-tune the classification.
"""

ARCHETYPE_METRIC_WEIGHTS = {
    "Foodie & Entertainment Spender": {
        "dining_ratio": 3.0,
        "shopping_ratio": 1.0,
        "savings_rate": 0.5,
        "emi_ratio": 0.5,
        "total_discretionary_ratio": 2.0
    },
    "Retail Therapy Lover": {
        "dining_ratio": 1.0,
        "shopping_ratio": 3.0,
        "savings_rate": 0.5,
        "emi_ratio": 0.5,
        "total_discretionary_ratio": 2.0
    },
    "Debt-Focused/Credit-Builder": {
        "dining_ratio": 0.5,
        "shopping_ratio": 0.5,
        "savings_rate": 1.0,
        "emi_ratio": 3.0,
        "total_discretionary_ratio": 0.5
    },
    "Budget-Focused Saver": {
        "dining_ratio": 0.5,
        "shopping_ratio": 0.5,
        "savings_rate": 3.0,
        "emi_ratio": 1.0,
        "total_discretionary_ratio": 1.0
    },
    "Subscription Enthusiast": {
        "dining_ratio": 0.5,
        "shopping_ratio": 1.0,
        "savings_rate": 1.0,
        "emi_ratio": 1.0,
        "total_discretionary_ratio": 1.0,
        "subscription_ratio": 3.0  # Additional weight for subscription ratio if you're tracking it
    },
    "Travel Enthusiast": {
        "dining_ratio": 1.0,
        "shopping_ratio": 1.0,
        "savings_rate": 1.0,
        "emi_ratio": 0.5,
        "total_discretionary_ratio": 1.5,
        "travel_ratio": 3.0        # If you track travel ratio
    },
    "Balanced Spender": {
        "dining_ratio": 1.0,
        "shopping_ratio": 1.0,
        "savings_rate": 1.0,
        "emi_ratio": 1.0,
        "total_discretionary_ratio": 1.0
    },
    "Premium Spender": {
        "dining_ratio": 2.0,
        "shopping_ratio": 2.0,
        "savings_rate": 1.0,
        "emi_ratio": 1.0,
        "total_discretionary_ratio": 2.0,
        "income_proxy": 3.0         # If high income is part of 'premium'
    }
}

"""
Usage Example:

# In your scoring logic (e.g., `scoring_modules.py`),
# you might do something like this:

for archetype, metric_weights in ARCHETYPE_METRIC_WEIGHTS.items():
    score = 0
    for metric, weight in metric_weights.items():
        score += user_metrics.get(metric, 0) * weight
    archetype_scores[archetype] = score
"""
