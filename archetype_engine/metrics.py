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
    travel_spend = 0.0   # For travel category
    entertainment_spend = 0.0 # For entertainment category
    
    # Enhanced premium categories with more specificity
    premium_categories = {"Jewelry", "Electronics", "Travel", "Investment", "Luxury", "Designer", "Fine Dining"}
    
    # Initialize a dictionary to count transactions per category
    transaction_counts = {}
    unique_merchants = {}
    monthly_spending = {}  # Track spending by month
    
    # Track transactions by time period for seasonal/time pattern detection
    days_of_week = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}  # Mon-Sun
    weekend_spend = 0.0
    weekday_spend = 0.0

    # Count high-value transactions (above 10000)
    high_value_txn_count = 0
    luxury_purchase_count = 0

    # Credit payments tracking
    credit_payment_count = 0
    
    # Track merchant frequency for repeat visit detection
    merchant_frequency = {}
    merchant_loyalty = {}
    
    from datetime import datetime
    
    for txn in transactions:
        amount = float(txn.get("amount", 0))
        category = txn.get("category", "").strip()
        transaction_type = txn.get("transaction_type", "").lower()
        merchant_name = txn.get("merchant_name", "Unknown")
        
        # Get transaction date for temporal analysis
        try:
            txn_date = datetime.fromisoformat(txn.get("date_time", "").replace('Z', '+00:00'))
            month_key = f"{txn_date.year}-{txn_date.month:02d}"
            day_of_week = txn_date.weekday()  # 0-6 (Monday is 0)
            
            # Track monthly spend
            if transaction_type != "credit":
                monthly_spending[month_key] = monthly_spending.get(month_key, 0) + amount
                
            # Track day of week spending
            days_of_week[day_of_week] = days_of_week.get(day_of_week, 0) + 1
            
            # Track weekend vs weekday spend
            if day_of_week >= 5:  # 5=Saturday, 6=Sunday
                weekend_spend += amount if transaction_type != "credit" else 0
            else:
                weekday_spend += amount if transaction_type != "credit" else 0
        except (ValueError, AttributeError):
            # If date parsing fails, continue without temporal features
            pass

        # Skip credit transactions for spending analysis
        if transaction_type == "credit":
            if category == "Salary":
                total_income += amount
            continue
        
        total_spend += amount
        transaction_counts[category] = transaction_counts.get(category, 0) + 1
        
        # Track unique merchants per category
        if category not in unique_merchants:
            unique_merchants[category] = set()
        unique_merchants[category].add(merchant_name)
        
        # Track merchant frequency for loyalty analysis
        merchant_frequency[merchant_name] = merchant_frequency.get(merchant_name, 0) + 1

        if category == "Subscriptions":
            subscription_spend += amount
        elif category == "Dining":
            dining_spend += amount
        elif category == "Shopping":
            shopping_spend += amount
        elif category == "Savings":
            savings_spend += amount
        elif category == "Loan Emi":
            emi_spend += amount
        elif category == "Travel":
            travel_spend += amount
        elif category == "Entertainment":
            entertainment_spend += amount
        elif category == "Credit Card Payment":
            credit_payment_count += 1

        # Enhanced premium spending detection
        # Check both category and merchant name for premium signals
        is_premium = False
        
        # Check if category is premium
        if category in premium_categories:
            is_premium = True
            
        # Check merchant name for premium keywords
        premium_keywords = ["luxury", "premium", "gourmet", "boutique", "resort", "designer", "spa"]
        if any(keyword in merchant_name.lower() for keyword in premium_keywords):
            is_premium = True
            
        # Consider high-value transactions as premium
        if amount >= 10000:
            is_premium = True
            high_value_txn_count += 1
            
        if is_premium:
            premium_spend += amount
            if amount >= 10000:
                luxury_purchase_count += 1

    transaction_count = len(transactions)
    
    # Calculate ratios and protect against division by zero
    dining_ratio = dining_spend / total_spend if total_spend > 0 else 0
    shopping_ratio = shopping_spend / total_spend if total_spend > 0 else 0
    savings_rate = savings_spend / total_income if total_income > 0 else 0
    emi_ratio = emi_spend / total_income if total_income > 0 else 0
    subscription_ratio = subscription_spend / total_spend if total_spend > 0 else 0
    travel_ratio = travel_spend / total_spend if total_spend > 0 else 0
    entertainment_ratio = entertainment_spend / total_spend if total_spend > 0 else 0

    # Enhanced discretionary vs essential spending
    discretionary_categories = {"Dining", "Shopping", "Entertainment", "Travel", "Luxury"}
    essential_categories = {"Housing", "Utilities", "Groceries", "Healthcare", "Insurance", "Education"}
    
    total_discretionary_spend = sum(amount for txn in transactions 
                                 if txn.get("transaction_type", "").lower() != "credit" and 
                                 txn.get("category", "") in discretionary_categories)
    
    total_essentials_spend = sum(amount for txn in transactions 
                             if txn.get("transaction_type", "").lower() != "credit" and 
                             txn.get("category", "") in essential_categories)
    
    total_discretionary_ratio = total_discretionary_spend / total_spend if total_spend > 0 else 0
    
    # Calculate discretionary to essentials ratio
    discretionary_to_essentials_ratio = (total_discretionary_spend / total_essentials_spend) if total_essentials_spend > 0 else 0
    
    # Calculate average discretionary spend value
    discretionary_txn_count = sum(1 for txn in transactions 
                              if txn.get("transaction_type", "").lower() != "credit" and 
                              txn.get("category", "") in discretionary_categories)
    avg_discretionary_value = (total_discretionary_spend / discretionary_txn_count) if discretionary_txn_count > 0 else 0
    
    # Calculate premium spending ratio: premium_spend / total_spend
    premium_spend_ratio = premium_spend / total_spend if total_spend > 0 else 0

    # Calculate travel transaction frequency and average value
    travel_txn_count = transaction_counts.get("Travel", 0)
    travel_txn_frequency = travel_txn_count / transaction_count if transaction_count > 0 else 0
    avg_travel_value = travel_spend / travel_txn_count if travel_txn_count > 0 else 0

    # Calculate unique subscriptions
    unique_subscriptions = len(unique_merchants.get("Subscriptions", set()))
    
    # Calculate subscription frequency
    subscription_frequency = transaction_counts.get("Subscriptions", 0)

    # Calculate debt transactions (Loan EMI, Credit Card Payment)
    debt_txn_frequency = transaction_counts.get("Loan Emi", 0) + credit_payment_count
    
    # Calculate low discretionary ratio flag
    low_discretionary_ratio = total_discretionary_ratio < 0.30
    
    # Calculate category variance - a key metric for Balanced Spender detection
    if transaction_counts:
        values = list(transaction_counts.values())
        mean = sum(values) / len(values) if values else 1.0
        variance = sum((x - mean) ** 2 for x in values) / len(values) if len(values) > 0 else 1.0
        category_variance = variance / (mean**2) if mean > 0 else 1.0
    else:
        category_variance = 1.0
        
    # Calculate spending consistency (variation between months)
    spending_consistency = 0.0
    if len(monthly_spending) > 1:
        monthly_values = list(monthly_spending.values())
        monthly_mean = sum(monthly_values) / len(monthly_values)
        monthly_variance = sum((x - monthly_mean) ** 2 for x in monthly_values) / len(monthly_values)
        spending_consistency = monthly_variance / (monthly_mean**2) if monthly_mean > 0 else 1.0
    
    # Calculate merchant loyalty - ratio of repeat merchants to total merchants
    repeat_merchants = sum(1 for m, count in merchant_frequency.items() if count > 1)
    merchant_loyalty_ratio = repeat_merchants / len(merchant_frequency) if len(merchant_frequency) > 0 else 0
    
    # Calculate weekend to weekday spending ratio
    weekend_weekday_ratio = weekend_spend / weekday_spend if weekday_spend > 0 else 0

    metrics = {
        "subscription_ratio": subscription_ratio,
        "dining_ratio": dining_ratio,
        "shopping_ratio": shopping_ratio,
        "savings_rate": savings_rate,
        "emi_ratio": emi_ratio,
        "travel_ratio": travel_ratio,
        "entertainment_ratio": entertainment_ratio,
        "total_discretionary_ratio": total_discretionary_ratio,
        "discretionary_to_essentials_ratio": discretionary_to_essentials_ratio,
        "income_proxy": total_income,
        "avg_transaction_value": total_spend / transaction_count if transaction_count > 0 else 0,
        "transaction_count_by_category": transaction_counts,
        "transaction_frequency": transaction_count,
        "low_savings_flag": savings_rate < 0.10,
        "dining_txn_count": transaction_counts.get("Dining", 0),
        "premium_spend_ratio": premium_spend_ratio,
        "total_spend": total_spend,
        "luxury_purchase_count": luxury_purchase_count,
        "high_value_txn_count": high_value_txn_count,
        "unique_shopping_merchants": len(unique_merchants.get("Shopping", set())),
        "travel_txn_frequency": travel_txn_frequency,
        "avg_travel_value": avg_travel_value,
        "unique_subscriptions": unique_subscriptions,
        "subscription_frequency": subscription_frequency,
        "debt_txn_frequency": debt_txn_frequency,
        "credit_payment_flag": credit_payment_count > 0,
        "low_discretionary_ratio": low_discretionary_ratio,
        "average_discretionary_value": avg_discretionary_value,
        "category_variance": category_variance,
        "number_of_categories": len(transaction_counts),
        "spending_consistency": spending_consistency,
        "merchant_loyalty_ratio": merchant_loyalty_ratio,
        "weekend_weekday_ratio": weekend_weekday_ratio,
        "days_of_week_distribution": days_of_week
    }
    
    return metrics

if __name__ == "__main__":
    # Sample transactions for testing
    sample_transactions = [
        {"amount": 500000, "transaction_type": "credit", "category": "Salary"},
        {"amount": 3500, "transaction_type": "debit", "category": "Dining"},
        {"amount": 12000, "transaction_type": "debit", "category": "Shopping"},
        {"amount": 45000, "transaction_type": "debit", "category": "Jewelry"},  # Premium spend
        {"amount": 2500, "transaction_type": "debit", "category": "Dining"},
        {"amount": 18000, "transaction_type": "debit", "category": "Travel"},     # Premium spend
        {"amount": 35000, "transaction_type": "debit", "category": "Travel"},       # Premium spend
        {"amount": 1500, "transaction_type": "debit", "category": "Dining"},
        {"amount": 1500, "transaction_type": "debit", "category": "Shopping"},
        {"amount": 299, "transaction_type": "debit", "category": "Subscriptions"}
    ]
    
    metrics_result = compute_metrics(sample_transactions)
    print(metrics_result)
