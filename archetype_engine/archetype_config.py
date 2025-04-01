# archetype_config.py

# Thresholds for normalizing each metric.
ARCHETYPE_THRESHOLDS = {
    "dining_ratio": 0.15,                 # Lowered threshold for Foodie
    "entertainment_ratio": 0.10,
    "total_discretionary_ratio": 0.40,
    "dining_txn_count": 5,
    "shopping_ratio": 0.25,
    "shopping_txn_count": 5,
    "unique_shopping_merchants": 5,
    "emi_ratio": 0.30,
    "debt_txn_frequency": 3,
    "credit_payment_flag": 1,
    "savings_rate": 0.15,
    "low_discretionary_ratio": 0.3,
    "average_discretionary_value": 3000,
    "subscription_ratio": 0.05,
    "unique_subscriptions": 3,
    "subscription_frequency": 3,
    "travel_ratio": 0.10,
    "travel_txn_frequency": 2,
    "avg_travel_value": 5000,
    "category_variance": 0.10,            # Higher is worse; lower variance indicates balanced spending
    "number_of_categories": 5,
    "discretionary_to_essentials_ratio": 0.8,
    "income_proxy": 500000,
    "avg_transaction_value": 5000,
    "premium_spend_ratio": 0.30,
    "luxury_purchase_count": 3,
    "high_value_txn_count": 2
}

# Weights for each metric per archetype.
ARCHETYPE_METRIC_WEIGHTS = {
    "Foodie & Entertainment Spender": {
        "dining_ratio": 4.0,               # Increased weight for dining_ratio
        "entertainment_ratio": 1.5,
        "total_discretionary_ratio": 2.0,
        "dining_txn_count": 1.0
    },
    "Retail Therapy Lover": {
        "shopping_ratio": 3.0,
        "shopping_txn_count": 1.5,
        "unique_shopping_merchants": 1.0,
        "total_discretionary_ratio": 1.5,
        "dining_ratio": 0.5
    },
    "Debt-Focused/Credit-Builder": {
        "emi_ratio": 3.0,
        "debt_txn_frequency": 2.0,
        "credit_payment_flag": 1.0
    },
    "Budget-Focused Saver": {
        "savings_rate": 3.0,
        "low_discretionary_ratio": 2.0,
        "average_discretionary_value": 1.0  # Lower discretionary value is better.
    },
    "Subscription Enthusiast": {
        "subscription_ratio": 3.0,
        "unique_subscriptions": 2.0,
        "subscription_frequency": 1.0
    },
    "Travel Enthusiast": {
        "travel_ratio": 3.0,
        "travel_txn_frequency": 2.0,
        "avg_travel_value": 1.5
    },
    "Balanced Spender": {
        "category_variance": -1.0,         # Negative: lower variance is better.
        "number_of_categories": 1.0,
        "discretionary_to_essentials_ratio": 0.5
    },
    "Premium Spender": {
        "income_proxy": 1.5,
        "avg_transaction_value": 1.5,
        "premium_spend_ratio": 1.0,
        "luxury_purchase_count": 1.0,
        "high_value_txn_count": 1.0
    }
}

# Fallback archetype.
FALLBACK_ARCHETYPE = "Balanced Spender"
