# assign_archetype.py

from .metrics import compute_metrics
from .scoring_modules import assign_archetype

def assign_user_profile(transactions):
    user_metrics = compute_metrics(transactions)
    profile = assign_archetype(user_metrics)
    return profile

if __name__ == "__main__":
    # Sample transactions for testing
    sample_transactions = [
        {"amount": 500, "category": "Dining"},
        {"amount": 600, "category": "Dining"},
        {"amount": 1500, "category": "Shopping"},
        {"amount": 2000, "category": "Salary"},
        {"amount": 300, "category": "Subscriptions"}
    ]
    result = assign_user_profile(sample_transactions)
    print(result)
