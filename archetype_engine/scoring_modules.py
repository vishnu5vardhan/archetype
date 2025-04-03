# scoring_modules.py

from .archetype_config import ARCHETYPE_THRESHOLDS, ARCHETYPE_METRIC_WEIGHTS, FALLBACK_ARCHETYPE, PENALTY_FACTORS
from .archetype_config import COMPOSITE_ARCHETYPES, CONFIDENCE_SETTINGS
from .archetype_explanations import ARCHETYPE_EXPLANATIONS, ARCHETYPE_TAGS
import math

def softmax(score_dict):
    """Apply softmax normalization to the raw scores to yield a probability distribution."""
    # Add a small epsilon to prevent underflow
    exps = {k: math.exp(v) for k, v in score_dict.items()}
    total = sum(exps.values())
    return {k: exps[k] / total if total > 0 else 0 for k in exps}

def calculate_metric_contribution(metrics, archetype, metric_name, invert=False):
    """Helper function to calculate the contribution of a metric to an archetype score.
    
    Args:
        metrics (dict): The user metrics
        archetype (str): The archetype name
        metric_name (str): The metric to calculate
        invert (bool): If True, lower values are better (e.g., for variance)
        
    Returns:
        float: The contribution of this metric to the archetype score
    """
    # Get threshold and weight
    thresh = ARCHETYPE_THRESHOLDS.get(metric_name, 0)
    wt = ARCHETYPE_METRIC_WEIGHTS.get(archetype, {}).get(metric_name, 0)
    
    # Get metric value, defaulting to 0 if not found
    val = metrics.get(metric_name, 0)
    
    # If weight is negative, it means lower values are better
    if wt < 0:
        invert = True
        wt = abs(wt)
    
    # Calculate contribution
    if invert:
        # For inverted metrics, a lower value is better
        if thresh > 0:
            contrib = wt * (1 - min(val / thresh, 1.0))
        else:
            contrib = 0
    else:
        # For normal metrics, a higher value is better
        if thresh > 0:
            contrib = wt * min(val / thresh, 1.0)
        else:
            contrib = 0
            
    return contrib

def apply_penalty_factors(metrics, archetype, score):
    """Apply penalty factors to prevent misclassification based on missing key indicators.
    
    Args:
        metrics (dict): User metrics
        archetype (str): The archetype name
        score (float): The current score
        
    Returns:
        float: The adjusted score after penalties
    """
    penalties = PENALTY_FACTORS.get(archetype, {})
    adjusted_score = score
    
    # Apply each penalty factor defined for this archetype
    for factor_name, config in penalties.items():
        threshold = config.get("threshold", 0)
        penalty = config.get("penalty", 0)
        
        # Generic penalty application based on metric name
        if factor_name.startswith("low_") and factor_name.endswith("_ratio"):
            # Extract the metric name from the factor (e.g., "low_dining_ratio" -> "dining_ratio")
            metric_name = factor_name[4:]  # Remove "low_"
            if metrics.get(metric_name, 0) < threshold:
                adjusted_score = max(0, adjusted_score - penalty)
        elif factor_name.startswith("few_"):
            # For factors like "few_subscriptions" check against the relevant metric
            metric_name = factor_name[5:] if factor_name.startswith("few_") else factor_name
            if metrics.get(metric_name, 0) < threshold:
                adjusted_score = max(0, adjusted_score - penalty)
        elif factor_name == "low_avg_transaction":
            if metrics.get("avg_transaction_value", 0) < threshold:
                adjusted_score = max(0, adjusted_score - penalty)
        
    return adjusted_score

def calculate_archetype_scores(metrics):
    """
    Calculate scores for each archetype based on user metrics.
    
    Args:
        metrics (dict): User metrics calculated from transaction data
        
    Returns:
        dict: Raw scores for each archetype
    """
    raw_scores = {}

    ### Foodie & Entertainment Spender ###
    foodie_score = 0.0
    for metric in ["dining_ratio", "entertainment_ratio", "total_discretionary_ratio", "dining_txn_count", "weekend_weekday_ratio"]:
        foodie_score += calculate_metric_contribution(metrics, "Foodie & Entertainment Spender", metric)
    
    # Apply penalty if savings_rate is high (i.e. if user is thrifty)
    savings = metrics.get("savings_rate", 0)
    if savings > 0.30:
        penalty = 2.0 * (savings - 0.30)
        foodie_score = max(0, foodie_score - penalty)
        
    # Apply specific penalty factors
    foodie_score = apply_penalty_factors(metrics, "Foodie & Entertainment Spender", foodie_score)

    raw_scores["Foodie & Entertainment Spender"] = foodie_score

    ### Retail Therapy Lover ###
    retail_score = 0.0
    for metric in ["shopping_ratio", "shopping_txn_count", "unique_shopping_merchants", "total_discretionary_ratio", "weekend_weekday_ratio"]:
        retail_score += calculate_metric_contribution(metrics, "Retail Therapy Lover", metric)
    
    # Apply specific penalty factors
    retail_score = apply_penalty_factors(metrics, "Retail Therapy Lover", retail_score)
    
    raw_scores["Retail Therapy Lover"] = retail_score

    ### Premium Spender ###
    premium_score = 0.0
    for metric in ["income_proxy", "avg_transaction_value", "premium_spend_ratio", 
                  "luxury_purchase_count", "high_value_txn_count", "weekend_weekday_ratio"]:
        premium_score += calculate_metric_contribution(metrics, "Premium Spender", metric)
    
    # Apply specific penalty factors for Premium Spender
    premium_score = apply_penalty_factors(metrics, "Premium Spender", premium_score)
    
    raw_scores["Premium Spender"] = premium_score

    ### Travel Enthusiast ###
    travel_score = 0.0
    for metric in ["travel_ratio", "travel_txn_frequency", "avg_travel_value", "spending_consistency"]:
        travel_score += calculate_metric_contribution(metrics, "Travel Enthusiast", metric)
    
    # Apply specific penalty factors for Travel Enthusiast
    travel_score = apply_penalty_factors(metrics, "Travel Enthusiast", travel_score)
    
    raw_scores["Travel Enthusiast"] = travel_score

    ### Debt-Focused/Credit-Builder ###
    debt_score = 0.0
    for metric in ["emi_ratio", "debt_txn_frequency", "credit_payment_flag", "spending_consistency"]:
        debt_score += calculate_metric_contribution(metrics, "Debt-Focused/Credit-Builder", metric)
    
    raw_scores["Debt-Focused/Credit-Builder"] = debt_score

    ### Budget-Focused Saver ###
    saver_score = 0.0
    for metric in ["savings_rate", "low_discretionary_ratio", "spending_consistency"]:
        saver_score += calculate_metric_contribution(metrics, "Budget-Focused Saver", metric)
    
    # Special case for average_discretionary_value - lower is better
    saver_score += calculate_metric_contribution(
        metrics, "Budget-Focused Saver", "average_discretionary_value", invert=True)
    
    raw_scores["Budget-Focused Saver"] = saver_score

    ### Subscription Enthusiast ###
    sub_score = 0.0
    for metric in ["subscription_ratio", "unique_subscriptions", "subscription_frequency", "spending_consistency"]:
        sub_score += calculate_metric_contribution(metrics, "Subscription Enthusiast", metric)
    
    # Apply specific penalty factors for Subscription Enthusiast
    sub_score = apply_penalty_factors(metrics, "Subscription Enthusiast", sub_score)
    
    raw_scores["Subscription Enthusiast"] = sub_score

    ### Balanced Spender ###
    balanced_score = 0.0
    
    # Category variance: lower is better (handled by negative weight)
    balanced_score += calculate_metric_contribution(metrics, "Balanced Spender", "category_variance")
    
    # Number of categories
    balanced_score += calculate_metric_contribution(metrics, "Balanced Spender", "number_of_categories")
    
    # Merchant loyalty
    balanced_score += calculate_metric_contribution(metrics, "Balanced Spender", "merchant_loyalty_ratio")
    
    # Discretionary-to-Essentials Ratio: best when close to 1
    ratio_val = metrics.get("discretionary_to_essentials_ratio", 1.0)
    ideal = 1.0
    diff = abs(ratio_val - ideal)
    wt = ARCHETYPE_METRIC_WEIGHTS.get("Balanced Spender", {}).get("discretionary_to_essentials_ratio", 0.5)
    balanced_score += wt * (1 - min(diff / ideal, 1.0))
    
    # Add a bonus for having a good distribution across multiple categories
    category_counts = metrics.get("transaction_count_by_category", {})
    if len(category_counts) >= 4:  # If user has transactions in at least 4 categories
        values = list(category_counts.values())
        mean = sum(values) / len(values) if values else 0
        # Count how many categories are close to the mean (within 30%)
        balanced_categories = sum(1 for v in values if abs(v - mean) <= 0.3 * mean)
        # If at least half the categories are balanced, add a bonus
        if balanced_categories >= len(values) / 2:
            balanced_score += 2.0
    
    raw_scores["Balanced Spender"] = balanced_score

    return raw_scores

def detect_composite_archetypes(normalized_scores):
    """
    Detect if the user fits into any of the predefined composite archetypes.
    
    Args:
        normalized_scores (dict): The normalized scores for each archetype
        
    Returns:
        dict: Detected composite archetypes with their confidence scores
    """
    composite_results = {}
    
    for composite_name, composite_def in COMPOSITE_ARCHETYPES.items():
        primary = composite_def["primary"]
        secondary = composite_def["secondary"]
        threshold = composite_def["threshold"]
        
        if primary in normalized_scores and secondary in normalized_scores:
            primary_score = normalized_scores[primary]
            secondary_score = normalized_scores[secondary]
            
            # Check if the secondary score is at least the threshold percentage of the primary score
            if primary_score > 0 and secondary_score >= primary_score * threshold:
                # Calculate composite confidence as the average with a bonus
                composite_confidence = (primary_score + secondary_score) / 2 * 1.1
                composite_results[composite_name] = round(composite_confidence, 2)
    
    return composite_results

def calculate_confidence_score(scores, metrics):
    """
    Calculate confidence score based on the difference between top scores
    and how strongly the metrics match the archetypes.
    
    Args:
        scores (dict): Normalized scores for each archetype
        metrics (dict): User metrics used for additional confidence boosting
        
    Returns:
        float: Confidence score between 0 and 1
    """
    if not scores:
        return 0.0
    
    sorted_scores = sorted(scores.values(), reverse=True)
    
    if len(sorted_scores) == 1:
        return 1.0
    
    # Calculate gap between top and second score
    top_score = sorted_scores[0]
    second_score = sorted_scores[1] if len(sorted_scores) > 1 else 0
    
    # Gap as a percentage of the top score
    gap_percentage = (top_score - second_score) / top_score if top_score > 0 else 0
    
    # Get the minimum gap required for high confidence
    min_gap = CONFIDENCE_SETTINGS.get("min_gap_for_high_confidence", 0.2)
    min_confidence = CONFIDENCE_SETTINGS.get("min_confidence_baseline", 0.5)
    bonus = CONFIDENCE_SETTINGS.get("bonus_for_clear_metrics", 0.1)
    
    # Base confidence calculation
    confidence = min_confidence + (gap_percentage / min_gap) * (1 - min_confidence)
    confidence = min(1.0, confidence)  # Cap at 1.0
    
    # Get top archetype
    top_archetype = next(iter([k for k, v in scores.items() if v == top_score]), "")
    
    # Check if key metrics for the top archetype are well above thresholds
    if top_archetype == "Foodie & Entertainment Spender" and metrics.get("dining_ratio", 0) > ARCHETYPE_THRESHOLDS.get("dining_ratio", 0) * 1.5:
        confidence += bonus
    elif top_archetype == "Retail Therapy Lover" and metrics.get("shopping_ratio", 0) > ARCHETYPE_THRESHOLDS.get("shopping_ratio", 0) * 1.5:
        confidence += bonus
    elif top_archetype == "Budget-Focused Saver" and metrics.get("savings_rate", 0) > ARCHETYPE_THRESHOLDS.get("savings_rate", 0) * 1.5:
        confidence += bonus
    elif top_archetype == "Travel Enthusiast" and metrics.get("travel_ratio", 0) > ARCHETYPE_THRESHOLDS.get("travel_ratio", 0) * 1.5:
        confidence += bonus
    
    return min(1.0, confidence)  # Cap at 1.0 in case bonuses pushed it over

def get_archetype_explanation(archetype_name):
    """Get the explanation for an archetype."""
    return ARCHETYPE_EXPLANATIONS.get(archetype_name, "No explanation available.")

def get_archetype_tags(archetype_name):
    """Get the tags for an archetype."""
    return ARCHETYPE_TAGS.get(archetype_name, [])

def assign_archetype(metrics):
    """
    Assign an archetype based on user metrics.
    
    Args:
        metrics (dict): User metrics calculated from transaction data
        
    Returns:
        dict: Result containing top archetype, confidence, and scores
    """
    raw_scores = calculate_archetype_scores(metrics)

    # Apply softmax normalization to get probability distribution
    softmax_scores = softmax(raw_scores)
    
    # For display, scale probabilities to 10
    normalized_scores = {k: round(v * 10, 2) for k, v in softmax_scores.items()}

    # Sort archetypes by score
    sorted_norm = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
    
    if sorted_norm:
        top_archetype, top_score = sorted_norm[0]
    else:
        top_archetype, top_score = FALLBACK_ARCHETYPE, 0.0

    # Enhanced tie-breaker for close scores (within 0.5 points)
    close_candidates = [x for x in sorted_norm if (top_score - x[1]) < 0.5]
    
    if len(close_candidates) > 1:
        # Use secondary metrics as tiebreakers for specific archetypes
        secondary_metrics = {
            "Premium Spender": metrics.get("premium_spend_ratio", 0) * 2.0,
            "Foodie & Entertainment Spender": metrics.get("dining_ratio", 0) * 1.5,
            "Retail Therapy Lover": metrics.get("shopping_ratio", 0) * 1.5,
            "Travel Enthusiast": metrics.get("travel_ratio", 0) * 1.5,
            "Budget-Focused Saver": metrics.get("savings_rate", 0) * 1.5,
            "Subscription Enthusiast": metrics.get("subscription_ratio", 0) * 1.5,
            "Debt-Focused/Credit-Builder": metrics.get("emi_ratio", 0) * 1.5,
            "Balanced Spender": (1 - metrics.get("category_variance", 1)) * 0.5
        }
        
        # Adjust scores with secondary metrics
        adjusted_candidates = [(name, score + secondary_metrics.get(name, 0)) 
                             for name, score in close_candidates]
        
        # Re-sort with adjusted scores
        adjusted_candidates.sort(key=lambda x: x[1], reverse=True)
        top_archetype = adjusted_candidates[0][0]

    # Calculate confidence based on score distribution and metrics
    confidence = calculate_confidence_score(normalized_scores, metrics)
    
    # Check for composite archetypes
    composite_archetypes = detect_composite_archetypes(normalized_scores)
    
    # Prepare the result
    result = {
        "top_archetype": top_archetype,
        "confidence": round(confidence, 4),
        "explanation": get_archetype_explanation(top_archetype),
        "tags": get_archetype_tags(top_archetype),
        "score_breakdown": normalized_scores,
        "ranked_scores": [{"archetype": k, "score": v} for k, v in sorted_norm]
    }
    
    # Add composite archetypes if detected
    if composite_archetypes:
        result["composite_archetypes"] = composite_archetypes
    
    return result
