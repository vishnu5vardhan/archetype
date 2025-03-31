# archetype_config.py

ARCHETYPE_THRESHOLDS = {
    "dining_ratio": 0.20,
    "shopping_ratio": 0.25,
    "emi_ratio": 0.30,
    "savings_rate": 0.15,
    "total_discretionary_ratio": 0.40,
    "subscription_ratio": 0.05,
    "travel_ratio": 0.10,
    "dining_txn_count": 5
}

TIE_BREAKER = {
    "primary_metric": "total_discretionary_ratio",
    "secondary_metric": "shopping_ratio"
}

ARCHETYPE_WEIGHTS = {
    "Foodie & Entertainment Spender": 3,
    "Retail Therapy Lover": 2,
    "Debt-Focused/Credit-Builder": 1,
    "Budget-Focused Saver": 2,
    "Premium Spender": 2,
    "Balanced Spender": 1,
    "Subscription Enthusiast": 1.5,
    "Travel Enthusiast": 2
}
