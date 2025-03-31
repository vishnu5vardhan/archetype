# metrics.py

def compute_metrics(transactions):
    """
    Compute various metrics based on the transactions data.
    This includes ratios for dining, shopping, savings, EMI, and more.
    """
    subscription_spend = 0.0
    total_spend = 0.0
    total_income = 0.0
    dining_spend = 0.0
    shopping_spend = 0.0
    savings_spend = 0.0
    emi_spend = 0.0
    transaction_counts = {}

    for txn in transactions:
        amount = float(txn.get("amount", 0))
        category = txn.get("category", "").strip()
        total_spend += amount
        transaction_counts[category] = transaction_counts.get(category, 0) + 1

        if category == "Subscriptions":
            subscription_spend += amount
        if category == "Salary":
            total_income += amount
        if category == "Dining":
            dining_spend += amount
        elif category == "Shopping":
            shopping_spend += amount
        elif category == "Savings":
            savings_spend += amount
        elif category == "Loan Emi":
            emi_spend += amount

    transaction_count = len(transactions)
    dining_ratio = dining_spend / total_spend if total_spend > 0 else 0
    shopping_ratio = shopping_spend / total_spend if total_spend > 0 else 0
    savings_rate = savings_spend / total_income if total_income > 0 else 0
    emi_ratio = emi_spend / total_income if total_income > 0 else 0
    subscription_ratio = subscription_spend / total_spend if total_spend > 0 else 0

    total_discretionary_spend = dining_spend + shopping_spend
    total_essentials_spend = total_spend - total_discretionary_spend
    total_discretionary_ratio = total_discretionary_spend / total_spend if total_spend > 0 else 0
    discretionary_to_essentials_ratio = total_discretionary_spend / total_essentials_spend if total_essentials_spend > 0 else 0

    metrics = {
        "subscription_ratio": subscription_ratio,
        "dining_ratio": dining_ratio,
        "shopping_ratio": shopping_ratio,
        "savings_rate": savings_rate,
        "emi_ratio": emi_ratio,
        "total_discretionary_ratio": total_discretionary_ratio,
        "discretionary_to_essentials_ratio": discretionary_to_essentials_ratio,
        "income_proxy": total_income,
        "avg_transaction_value": total_spend / transaction_count if transaction_count > 0 else 0,
        "transaction_count_by_category": transaction_counts,
        "transaction_frequency": transaction_count,
        "low_savings_flag": savings_rate < 0.10,
        "dining_txn_count": transaction_counts.get("Dining", 0),
        "total_spend": total_spend
    }
    
    return metrics

if __name__ == "__main__":
    # Example test data
    sample_transactions = [
        {"amount": 500, "category": "Dining"},
        {"amount": 600, "category": "Dining"},
        {"amount": 1500, "category": "Shopping"},
        {"amount": 2000, "category": "Salary"},
        {"amount": 300, "category": "Subscriptions"}
    ]
    
    metrics_result = compute_metrics(sample_transactions)
    print(metrics_result)
