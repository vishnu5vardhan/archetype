# assign_archetype.py

"""
This module ties together the metrics calculation and the
scoring logic to assign the user an archetype.
"""

from .metrics import compute_metrics
from .scoring_modules import assign_archetype as score_and_assign_archetype

def assign_user_profile(transactions):
    """
    Main function to compute metrics for the user's transactions,
    calculate scores for each archetype, and determine the top archetype.

    Args:
        transactions (list): A list of transaction dicts, each containing:
            - amount (float)
            - transaction_type ('debit' or 'credit')
            - category (str) e.g. 'Dining', 'Shopping', 'Savings', etc.
            - date_time (str) ISO format date/time
            - merchant_name (str) optional name of merchant

    Returns:
        dict: A dictionary containing:
            - top_archetype (str): The best-fitting archetype
            - confidence (float): Confidence score between 0 and 1
            - explanation (str): Why the user got this archetype
            - tags (list): Additional labels describing this archetype
            - score_breakdown (dict): The normalized scores for each archetype
            - metrics (dict): Key user metrics for reference
            - ranked_scores (list): Archetypes sorted by score in descending order
            - composite_archetypes (dict, optional): Any detected composite archetypes
    """

    # 1. Compute user metrics based on their transaction data
    user_metrics = compute_metrics(transactions)

    # 2. Score and assign archetype (including composite detection)
    profile = score_and_assign_archetype(user_metrics)
    
    # 3. Add the metrics to the result for reference and debugging
    profile["metrics"] = user_metrics
    
    # 4. Format the metrics for better readability in output
    formatted_metrics = format_key_metrics(user_metrics)
    profile["formatted_metrics"] = formatted_metrics
    
    # 5. Add extended info for the assigned archetype
    add_extended_archetype_info(profile)
    
    return profile

def format_key_metrics(metrics):
    """Format key metrics for better readability in output."""
    formatted = {}
    
    # Format ratio metrics as percentages
    ratio_metrics = [
        "dining_ratio", "shopping_ratio", "travel_ratio", 
        "entertainment_ratio", "subscription_ratio", "savings_rate", 
        "total_discretionary_ratio", "premium_spend_ratio"
    ]
    
    for metric in ratio_metrics:
        if metric in metrics:
            formatted[metric] = f"{metrics[metric]*100:.1f}%"
    
    # Format currency values
    currency_metrics = [
        "total_spend", "avg_transaction_value", "average_discretionary_value", 
        "income_proxy", "avg_travel_value"
    ]
    
    for metric in currency_metrics:
        if metric in metrics:
            formatted[metric] = f"₹{metrics[metric]:,.2f}"
    
    # Add count metrics
    count_metrics = [
        "transaction_frequency", "dining_txn_count", "unique_subscriptions",
        "luxury_purchase_count", "number_of_categories", "unique_shopping_merchants"
    ]
    
    for metric in count_metrics:
        if metric in metrics:
            formatted[metric] = str(metrics[metric])
    
    return formatted

def add_extended_archetype_info(profile):
    """Add extended information for the assigned archetype."""
    archetype = profile.get("top_archetype", "")
    metrics = profile.get("metrics", {})
    
    if not archetype or not metrics:
        return
    
    # Add financial health indicators based on archetype
    financial_health = {}
    
    if archetype == "Budget-Focused Saver":
        financial_health["savings_performance"] = "Strong"
        financial_health["long_term_outlook"] = "Excellent"
        financial_health["budget_discipline"] = "High"
    elif archetype == "Foodie & Entertainment Spender":
        financial_health["discretionary_spending"] = "High"
        if metrics.get("savings_rate", 0) < 0.1:
            financial_health["savings_alert"] = "Consider increasing your savings rate"
    elif archetype == "Premium Spender":
        if metrics.get("income_proxy", 0) > 500000:
            financial_health["income_utilization"] = "Aligned with income level"
        else:
            financial_health["spending_alert"] = "Premium spending may be outpacing income"
    elif archetype == "Balanced Spender":
        financial_health["financial_balance"] = "Good"
        financial_health["spending_awareness"] = "High"
    
    # Add to profile if we have insights
    if financial_health:
        profile["financial_health_indicators"] = financial_health
    
    # Add next steps recommendations
    if "composite_archetypes" in profile:
        profile["composite_analysis"] = "Your spending patterns show traits of multiple archetypes, " + \
                                       "indicating a nuanced financial personality."
