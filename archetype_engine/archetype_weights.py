# archetype_config.py

# Global thresholds for individual metrics used for normalization.
# These are the values at which a metric contributes its full weight.
ARCHETYPE_THRESHOLDS_PER_METRIC = {
    "dining_ratio": 0.20,
    "shopping_ratio": 0.25,
    "savings_rate": 0.15,
    "emi_ratio": 0.30,
    "total_discretionary_ratio": 0.40,
    "dining_txn_count": 5,
    "entertainment_ratio": 0.10,
    "shopping_txn_count": 5,
    "unique_shopping_merchants": 5,
    "debt_txn_frequency": 3,
    "credit_payment_flag": 1,
    "low_discretionary_ratio": 0.3,
    "average_discretionary_value": 3000,
    "subscription_ratio": 0.05,
    "unique_subscriptions": 3,
    "subscription_frequency": 3,
    "travel_ratio": 0.10,
    "travel_txn_frequency": 2,
    "avg_travel_value": 5000,
    "category_variance": 0.05,        # Lower variance is better
    "number_of_categories": 5,
    "discretionary_to_essentials_ratio": 0.8,
    "income_proxy": 500000,           # Income threshold for premium boost
    "avg_transaction_value": 5000,
    "premium_spend_ratio": 0.30,      # Premium spend ratio threshold
    "luxury_purchase_count": 3,
    "high_value_txn_count": 2
}

# Weights for each archetype broken down by metric.
ARCHETYPE_METRIC_WEIGHTS = {
    "Foodie & Entertainment Spender": {
        "dining_ratio": 3.0,
        "shopping_ratio": 1.0,
        "savings_rate": 0.5,
        "emi_ratio": 0.5,
        "total_discretionary_ratio": 2.0,
        "dining_txn_count": 1.0,
        "entertainment_ratio": 1.5
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
        "travel_ratio": 3.0,
        "travel_txn_frequency": 2.0,
        "avg_travel_value": 1.5
    },
    "Balanced Spender": {
        "category_variance": -2.0,    # Negative weight means lower variance is better
        "number_of_categories": 2.0,
        "discretionary_to_essentials_ratio": 1.0
    },
    "Premium Spender": {
        "income_proxy": 1.5,
        "avg_transaction_value": 1.5,
        "premium_spend_ratio": 1.0,
        "luxury_purchase_count": 1.0,
        "high_value_txn_count": 1.0
    }
}

# Fallback archetype if no metrics produce any score
FALLBACK_ARCHETYPE = "Balanced Spender"
