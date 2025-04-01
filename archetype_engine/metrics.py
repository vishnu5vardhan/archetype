# metrics.py

def compute_metrics(transactions):
    """
    Compute various metrics based on the transactions data.
    This includes ratios for dining, shopping, savings, EMI, and premium spending.
    
    Args:
      transactions (list): A list of transaction dictionaries.
    
    Returns:
      dict: A dictionary containing calculated metrics.
    """
    
    # Initialize cumulative variables
    subscription_spend = 0.0
    total_spend = 0.0
    total_income = 0.0
    dining_spend = 0.0
    shopping_spend = 0.0
    savings_spend = 0.0
    emi_spend = 0.0
    premium_spend = 0.0  # For premium categories
    
    # Define premium categories (case-sensitive as per your data)
    premium_categories = {"Jewelry", "Electronics", "Travel", "Investment"}
    
    # Initialize a dictionary to count transactions per category
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

        # Sum up premium spending if the category is premium
        if category in premium_categories:
            premium_spend += amount

    transaction_count = len(transactions)
    
    # Calculate ratios and protect against division by zero
    dining_ratio = dining_spend / total_spend if total_spend > 0 else 0
    shopping_ratio = shopping_spend / total_spend if total_spend > 0 else 0
    savings_rate = savings_spend / total_income if total_income > 0 else 0
    emi_ratio = emi_spend / total_income if total_income > 0 else 0
    subscription_ratio = subscription_spend / total_spend if total_spend > 0 else 0

    total_discretionary_spend = dining_spend + shopping_spend
    total_essentials_spend = total_spend - total_discretionary_spend
    total_discretionary_ratio = total_discretionary_spend / total_spend if total_spend > 0 else 0
    discretionary_to_essentials_ratio = (total_discretionary_spend / total_essentials_spend) if total_essentials_spend > 0 else 0
    
    # Calculate premium spending ratio: premium_spend / total_spend
    premium_spend_ratio = premium_spend / total_spend if total_spend > 0 else 0

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
        "premium_spend_ratio": premium_spend_ratio,
        "total_spend": total_spend
    }
    
    return metrics

if __name__ == "__main__":
    # Sample transactions for testing
    sample_transactions = [
        {"amount": 500000, "category": "Salary"},
        {"amount": 3500, "category": "Dining"},
        {"amount": 12000, "category": "Shopping"},
        {"amount": 45000, "category": "Jewelry"},  # Premium spend
        {"amount": 2500, "category": "Dining"},
        {"amount": 18000, "category": "Travel"},     # Premium spend
        {"amount": 35000, "category": "Travel"},       # Premium spend
        {"amount": 1500, "category": "Dining"},
        {"amount": 1500, "category": "Shopping"},
        {"amount": 299, "category": "Subscriptions"}
    ]
    
    metrics_result = compute_metrics(sample_transactions)
    print(metrics_result)
