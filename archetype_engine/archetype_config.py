# archetype_config.py

ARCHETYPE_THRESHOLDS = {
    "dining_ratio": 0.15,
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
    "travel_ratio": 0.20,          # Increased threshold so that high travel spend (above 20%) yields full points.
    "travel_txn_frequency": 0.10,  # Expressed as fraction of transactions (e.g., 10% of txns)
    "avg_travel_value": 10000,     # Adjusted threshold for high travel-value transactions.
    "category_variance": 0.10,
    "number_of_categories": 5,
    "discretionary_to_essentials_ratio": 0.8,
    "income_proxy": 500000,
    "avg_transaction_value": 5000,
    "premium_spend_ratio": 0.30,
    "luxury_purchase_count": 3,
    "high_value_txn_count": 2
}

ARCHETYPE_METRIC_WEIGHTS = {
    "Foodie & Entertainment Spender": {
        "dining_ratio": 4.0,
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
        "average_discretionary_value": 1.0
    },
    "Subscription Enthusiast": {
        "subscription_ratio": 3.0,
        "unique_subscriptions": 2.0,
        "subscription_frequency": 1.0
    },
    "Travel Enthusiast": {
        "travel_ratio": 4.0,         # Increased weight for travel_ratio
        "travel_txn_frequency": 3.0,   # Boost travel transaction frequency
        "avg_travel_value": 2.0        # Boost average travel transaction value
    },
    "Balanced Spender": {
        "category_variance": -1.0,
        "number_of_categories": 1.0,
        "discretionary_to_essentials_ratio": 0.5
    },
    "Premium Spender": {
        "income_proxy": 1.0,         # Reduced weight so high income doesn't dominate
        "avg_transaction_value": 1.0,
        "premium_spend_ratio": 0.8,    # Slightly reduced weight for premium spend ratio
        "luxury_purchase_count": 1.0,
        "high_value_txn_count": 1.0
    }
}

FALLBACK_ARCHETYPE = "Balanced Spender"
