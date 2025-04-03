# archetype_config.py

ARCHETYPE_THRESHOLDS = {
    # Financial behavior thresholds
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
    "travel_ratio": 0.15,          # Adjusted for better travel detection
    "travel_txn_frequency": 0.10,  # Expressed as fraction of transactions
    "avg_travel_value": 10000,     # Threshold for high travel-value transactions
    "category_variance": 0.10,
    "number_of_categories": 5,
    "discretionary_to_essentials_ratio": 0.8,
    "income_proxy": 500000,
    "avg_transaction_value": 5000,
    "premium_spend_ratio": 0.20,   # Reduced to make premium detection more sensitive
    "luxury_purchase_count": 2,    # Reduced to make luxury purchases more impactful
    "high_value_txn_count": 2,
    # New temporal metrics
    "spending_consistency": 0.15,  # Lower values indicate more consistent spending
    "merchant_loyalty_ratio": 0.30, # Higher values indicate customer loyalty
    "weekend_weekday_ratio": 1.5   # Higher values indicate weekend-heavy spending
}

ARCHETYPE_METRIC_WEIGHTS = {
    "Foodie & Entertainment Spender": {
        "dining_ratio": 3.5,
        "entertainment_ratio": 2.0,
        "total_discretionary_ratio": 2.0,
        "dining_txn_count": 1.5,
        "weekend_weekday_ratio": 0.8  # Foodies tend to dine out more on weekends
    },
    "Retail Therapy Lover": {
        "shopping_ratio": 3.5,
        "shopping_txn_count": 2.0,
        "unique_shopping_merchants": 1.5,
        "total_discretionary_ratio": 1.0,
        "weekend_weekday_ratio": 0.7  # Shopping often happens on weekends
    },
    "Debt-Focused/Credit-Builder": {
        "emi_ratio": 3.5,
        "debt_txn_frequency": 2.0,
        "credit_payment_flag": 1.5,
        "spending_consistency": 1.0  # Consistent spending patterns
    },
    "Budget-Focused Saver": {
        "savings_rate": 3.5,
        "low_discretionary_ratio": 2.0,
        "average_discretionary_value": 1.5,
        "spending_consistency": 1.0  # Consistent spending is a sign of budgeting
    },
    "Subscription Enthusiast": {
        "subscription_ratio": 3.5,
        "unique_subscriptions": 2.0,
        "subscription_frequency": 1.5,
        "spending_consistency": 1.2  # Highly consistent due to recurring payments
    },
    "Travel Enthusiast": {
        "travel_ratio": 3.5,
        "travel_txn_frequency": 2.0,
        "avg_travel_value": 1.5,
        "spending_consistency": -0.5  # Negative weight as travel spending is sporadic
    },
    "Balanced Spender": {
        "category_variance": -4.0,       # Increased negative weight means lower variance is rewarded more
        "number_of_categories": 3.0,      # Increased weight for having many categories
        "discretionary_to_essentials_ratio": 2.5,  # Higher weight for balanced spending ratio
        "merchant_loyalty_ratio": 1.0     # Balanced spenders often have consistent merchants
    },
    "Premium Spender": {
        "income_proxy": 1.5,
        "avg_transaction_value": 2.0,
        "premium_spend_ratio": 3.0,      # Higher weight for premium spending ratio
        "luxury_purchase_count": 2.0,
        "high_value_txn_count": 1.5,
        "weekend_weekday_ratio": 0.5     # Premium spending often on weekends/leisure
    }
}

# Penalty factors for extreme ratios - to prevent misclassification 
PENALTY_FACTORS = {
    # If dining ratio is below 8%, apply a penalty to Foodie & Entertainment
    "Foodie & Entertainment Spender": {
        "low_dining_ratio": {
            "threshold": 0.08,
            "penalty": 3.0  # Subtract this if below threshold
        }
    },
    # If shopping ratio is below 8%, apply a penalty to Retail Therapy
    "Retail Therapy Lover": {
        "low_shopping_ratio": {
            "threshold": 0.08,
            "penalty": 3.0
        }
    },
    # New: Penalize Travel Enthusiast if travel ratio is too low
    "Travel Enthusiast": {
        "low_travel_ratio": {
            "threshold": 0.07,
            "penalty": 3.0
        }
    },
    # New: Penalize Premium Spender if avg_transaction_value is too low
    "Premium Spender": {
        "low_avg_transaction": {
            "threshold": 3000,
            "penalty": 2.5
        }
    },
    # New: Penalize Subscription Enthusiast if not enough unique subscriptions
    "Subscription Enthusiast": {
        "few_subscriptions": {
            "threshold": 2,
            "penalty": 2.0
        }
    }
}

# Composite archetype definitions - for detecting hybrid spending behaviors
COMPOSITE_ARCHETYPES = {
    "Premium Foodie": {
        "primary": "Foodie & Entertainment Spender",
        "secondary": "Premium Spender",
        "threshold": 0.75  # If secondary is at least 75% of primary score
    },
    "Travel Foodie": {
        "primary": "Foodie & Entertainment Spender",
        "secondary": "Travel Enthusiast",
        "threshold": 0.80
    },
    "Digital Minimalist": {
        "primary": "Budget-Focused Saver",
        "secondary": "Subscription Enthusiast",
        "threshold": 0.70
    }
}

# Enhanced confidence calculation settings
CONFIDENCE_SETTINGS = {
    "min_gap_for_high_confidence": 0.20,  # Minimum gap between top scores for high confidence
    "min_confidence_baseline": 0.50,      # Minimum confidence level
    "bonus_for_clear_metrics": 0.10       # Bonus added when key metrics are well above thresholds
}

FALLBACK_ARCHETYPE = "Balanced Spender"
