# scoring_modules.py

from .archetype_config import ARCHETYPE_THRESHOLDS, ARCHETYPE_METRIC_WEIGHTS, FALLBACK_ARCHETYPE
from .archetype_explanations import ARCHETYPE_EXPLANATIONS, ARCHETYPE_TAGS
import math

def softmax(score_dict):
    """Apply softmax normalization to the raw scores to yield a probability distribution."""
    exps = {k: math.exp(v) for k, v in score_dict.items()}
    total = sum(exps.values())
    return {k: exps[k] / total for k in exps}

def calculate_archetype_scores(metrics):
    raw_scores = {}

    ### Foodie & Entertainment Spender ###
    foodie_score = 0.0
    # dining_ratio
    thresh = ARCHETYPE_THRESHOLDS.get("dining_ratio", 0.15)
    wt = ARCHETYPE_METRIC_WEIGHTS["Foodie & Entertainment Spender"].get("dining_ratio", 4.0)
    val = metrics.get("dining_ratio", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    foodie_score += contrib

    # entertainment_ratio
    thresh = ARCHETYPE_THRESHOLDS.get("entertainment_ratio", 0.10)
    wt = ARCHETYPE_METRIC_WEIGHTS["Foodie & Entertainment Spender"].get("entertainment_ratio", 1.5)
    val = metrics.get("entertainment_ratio", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    foodie_score += contrib

    # total_discretionary_ratio
    thresh = ARCHETYPE_THRESHOLDS.get("total_discretionary_ratio", 0.40)
    wt = ARCHETYPE_METRIC_WEIGHTS["Foodie & Entertainment Spender"].get("total_discretionary_ratio", 2.0)
    val = metrics.get("total_discretionary_ratio", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    foodie_score += contrib

    # dining_txn_count
    thresh = ARCHETYPE_THRESHOLDS.get("dining_txn_count", 5)
    wt = ARCHETYPE_METRIC_WEIGHTS["Foodie & Entertainment Spender"].get("dining_txn_count", 1.0)
    val = metrics.get("dining_txn_count", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    foodie_score += contrib

    # Apply penalty if savings_rate is high (i.e. if user is thrifty)
    savings = metrics.get("savings_rate", 0)
    if savings > 0.30:
        penalty = 2.0 * (savings - 0.30)
        foodie_score -= penalty

    raw_scores["Foodie & Entertainment Spender"] = foodie_score

    ### Retail Therapy Lover ###
    retail_score = 0.0
    thresh = ARCHETYPE_THRESHOLDS.get("shopping_ratio", 0.25)
    wt = ARCHETYPE_METRIC_WEIGHTS["Retail Therapy Lover"].get("shopping_ratio", 3.0)
    val = metrics.get("shopping_ratio", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    retail_score += contrib

    shopping_txn = metrics.get("transaction_count_by_category", {}).get("Shopping", 0)
    thresh = 5
    wt = ARCHETYPE_METRIC_WEIGHTS["Retail Therapy Lover"].get("shopping_txn_count", 1.5)
    contrib = wt * min(shopping_txn / thresh, 1.0) if thresh > 0 else 0
    retail_score += contrib

    thresh = ARCHETYPE_THRESHOLDS.get("unique_shopping_merchants", 5)
    wt = ARCHETYPE_METRIC_WEIGHTS["Retail Therapy Lover"].get("unique_shopping_merchants", 1.0)
    val = metrics.get("unique_shopping_merchants", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    retail_score += contrib

    raw_scores["Retail Therapy Lover"] = retail_score

    ### Premium Spender ###
    premium_score = 0.0
    thresh = ARCHETYPE_THRESHOLDS.get("income_proxy", 500000)
    wt = ARCHETYPE_METRIC_WEIGHTS["Premium Spender"].get("income_proxy", 1.0)  # Reduced weight
    val = metrics.get("income_proxy", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    premium_score += contrib

    thresh = ARCHETYPE_THRESHOLDS.get("avg_transaction_value", 5000)
    wt = ARCHETYPE_METRIC_WEIGHTS["Premium Spender"].get("avg_transaction_value", 1.0)
    val = metrics.get("avg_transaction_value", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    premium_score += contrib

    thresh = ARCHETYPE_THRESHOLDS.get("premium_spend_ratio", 0.30)
    wt = ARCHETYPE_METRIC_WEIGHTS["Premium Spender"].get("premium_spend_ratio", 0.8)  # Slightly reduced
    val = metrics.get("premium_spend_ratio", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    premium_score += contrib

    thresh = ARCHETYPE_THRESHOLDS.get("luxury_purchase_count", 3)
    wt = ARCHETYPE_METRIC_WEIGHTS["Premium Spender"].get("luxury_purchase_count", 1.0)
    val = metrics.get("luxury_purchase_count", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    premium_score += contrib

    thresh = ARCHETYPE_THRESHOLDS.get("high_value_txn_count", 2)
    wt = ARCHETYPE_METRIC_WEIGHTS["Premium Spender"].get("high_value_txn_count", 1.0)
    val = metrics.get("high_value_txn_count", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    premium_score += contrib

    raw_scores["Premium Spender"] = premium_score

    ### Travel Enthusiast ###
    travel_score = 0.0
    # Boost travel_ratio: adjust threshold to 0.20 and weight to 4.0.
    thresh = ARCHETYPE_THRESHOLDS.get("travel_ratio", 0.20)
    wt = ARCHETYPE_METRIC_WEIGHTS["Travel Enthusiast"].get("travel_ratio", 4.0)
    val = metrics.get("travel_ratio", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    travel_score += contrib

    # Boost travel_txn_frequency: assume this is a fraction (e.g., 0.10 means 10% of transactions).
    thresh = ARCHETYPE_THRESHOLDS.get("travel_txn_frequency", 0.10)
    wt = ARCHETYPE_METRIC_WEIGHTS["Travel Enthusiast"].get("travel_txn_frequency", 3.0)
    val = metrics.get("travel_txn_frequency", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    travel_score += contrib

    # Boost avg_travel_value: adjust threshold to 10,000 and weight to 2.0.
    thresh = ARCHETYPE_THRESHOLDS.get("avg_travel_value", 10000)
    wt = ARCHETYPE_METRIC_WEIGHTS["Travel Enthusiast"].get("avg_travel_value", 2.0)
    val = metrics.get("avg_travel_value", 0)
    contrib = wt * min(val / thresh, 1.0) if thresh > 0 else 0
    travel_score += contrib

    raw_scores["Travel Enthusiast"] = travel_score

    ### Debt-Focused/Credit-Builder ###
    debt_score = 0.0
    thresh = ARCHETYPE_THRESHOLDS.get("emi_ratio", 0.30)
    wt = ARCHETYPE_METRIC_WEIGHTS["Debt-Focused/Credit-Builder"].get("emi_ratio", 3.0)
    val = metrics.get("emi_ratio", 0)
    debt_score += wt * min(val / thresh, 1.0) if thresh > 0 else 0

    thresh = ARCHETYPE_THRESHOLDS.get("debt_txn_frequency", 3)
    wt = ARCHETYPE_METRIC_WEIGHTS["Debt-Focused/Credit-Builder"].get("debt_txn_frequency", 2.0)
    val = metrics.get("debt_txn_frequency", 0)
    debt_score += wt * min(val / thresh, 1.0) if thresh > 0 else 0

    thresh = ARCHETYPE_THRESHOLDS.get("credit_payment_flag", 1)
    wt = ARCHETYPE_METRIC_WEIGHTS["Debt-Focused/Credit-Builder"].get("credit_payment_flag", 1.0)
    val = metrics.get("credit_payment_flag", 0)
    debt_score += wt * min(val / thresh, 1.0) if thresh > 0 else 0

    raw_scores["Debt-Focused/Credit-Builder"] = debt_score

    ### Budget-Focused Saver ###
    saver_score = 0.0
    thresh = ARCHETYPE_THRESHOLDS.get("savings_rate", 0.15)
    wt = ARCHETYPE_METRIC_WEIGHTS["Budget-Focused Saver"].get("savings_rate", 3.0)
    val = metrics.get("savings_rate", 0)
    saver_score += wt * min(val / thresh, 1.0) if thresh > 0 else 0

    thresh = ARCHETYPE_THRESHOLDS.get("low_discretionary_ratio", 0.3)
    wt = ARCHETYPE_METRIC_WEIGHTS["Budget-Focused Saver"].get("low_discretionary_ratio", 2.0)
    val = metrics.get("low_discretionary_ratio", 0)
    saver_score += wt * min(val / thresh, 1.0) if thresh > 0 else 0

    thresh = ARCHETYPE_THRESHOLDS.get("average_discretionary_value", 3000)
    wt = ARCHETYPE_METRIC_WEIGHTS["Budget-Focused Saver"].get("average_discretionary_value", 1.0)
    val = metrics.get("average_discretionary_value", 0)
    saver_score += wt * min(thresh / val, 1.0) if val > 0 else wt
    raw_scores["Budget-Focused Saver"] = saver_score

    ### Subscription Enthusiast ###
    sub_score = 0.0
    thresh = ARCHETYPE_THRESHOLDS.get("subscription_ratio", 0.05)
    wt = ARCHETYPE_METRIC_WEIGHTS["Subscription Enthusiast"].get("subscription_ratio", 3.0)
    val = metrics.get("subscription_ratio", 0)
    sub_score += wt * min(val / thresh, 1.0) if thresh > 0 else 0

    thresh = ARCHETYPE_THRESHOLDS.get("unique_subscriptions", 3)
    wt = ARCHETYPE_METRIC_WEIGHTS["Subscription Enthusiast"].get("unique_subscriptions", 2.0)
    val = metrics.get("unique_subscriptions", 0)
    sub_score += wt * min(val / thresh, 1.0) if thresh > 0 else 0

    thresh = ARCHETYPE_THRESHOLDS.get("subscription_frequency", 3)
    wt = ARCHETYPE_METRIC_WEIGHTS["Subscription Enthusiast"].get("subscription_frequency", 1.0)
    val = metrics.get("subscription_frequency", 0)
    sub_score += wt * min(val / thresh, 1.0) if thresh > 0 else 0

    raw_scores["Subscription Enthusiast"] = sub_score

    ### Balanced Spender ###
    balanced_score = 0.0
    # Category variance: lower is better.
    var_val = metrics.get("category_variance", None)
    if var_val is None:
        txn_counts = metrics.get("transaction_count_by_category", {})
        if txn_counts:
            values = list(txn_counts.values())
            mean = sum(values) / len(values) if values else 1.0
            variance = sum((x - mean) ** 2 for x in values) / len(values) if len(values) > 0 else 1.0
            var_val = math.sqrt(variance) / mean if mean > 0 else 1.0
        else:
            var_val = 1.0
    thresh = ARCHETYPE_THRESHOLDS.get("category_variance", 0.10)
    wt = ARCHETYPE_METRIC_WEIGHTS.get("Balanced Spender", {}).get("category_variance", -1.0)
    balanced_score += abs(wt) * (1 - min(var_val / thresh, 1.0))
    
    # Number of categories
    num_cat = metrics.get("number_of_categories", len(metrics.get("transaction_count_by_category", {})))
    thresh = ARCHETYPE_THRESHOLDS.get("number_of_categories", 5)
    wt = ARCHETYPE_METRIC_WEIGHTS.get("Balanced Spender", {}).get("number_of_categories", 1.0)
    balanced_score += wt * min(num_cat / thresh, 1.0)
    
    # Discretionary-to-Essentials Ratio: best when close to 1.
    ratio_val = metrics.get("discretionary_to_essentials_ratio", 1.0)
    ideal = 1.0
    diff = abs(ratio_val - ideal)
    wt = ARCHETYPE_METRIC_WEIGHTS.get("Balanced Spender", {}).get("discretionary_to_essentials_ratio", 0.5)
    balanced_score += wt * (1 - min(diff / ideal, 1.0))
    
    raw_scores["Balanced Spender"] = balanced_score

    return raw_scores

def assign_archetype(metrics):
    raw_scores = calculate_archetype_scores(metrics)

    # Softmax normalization to convert raw scores into a probability distribution.
    exp_scores = {k: math.exp(v) for k, v in raw_scores.items()}
    total_exp = sum(exp_scores.values())
    softmax_scores = {k: exp_scores[k] / total_exp for k in exp_scores}
    
    # For display, scale probabilities to 10.
    normalized_scores = {k: v * 10 for k, v in softmax_scores.items()}

    # Determine top archetype by highest normalized score.
    sorted_norm = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
    if sorted_norm:
        top_archetype, top_score = sorted_norm[0]
    else:
        top_archetype, top_score = FALLBACK_ARCHETYPE, 0.0

    # Enhanced tie-breaker: if scores are within 0.1 of the top score, use composite secondary metrics.
    top_candidates = [x for x in sorted_norm if abs(x[1] - top_score) < 0.1]
    if len(top_candidates) > 1:
        secondary = {
            "Premium Spender": metrics.get("premium_spend_ratio", 0),
            "Foodie & Entertainment Spender": metrics.get("dining_ratio", 0),
            "Retail Therapy Lover": metrics.get("shopping_ratio", 0),
            "Travel Enthusiast": metrics.get("travel_ratio", 0)
        }
        top_candidates = sorted(top_candidates, key=lambda x: secondary.get(x[0], 0), reverse=True)
        top_archetype = top_candidates[0][0]

    # Confidence: softmax probability scaled to 10, divided by 10.
    confidence = round(top_score / 10, 4)

    return {
        "top_archetype": top_archetype,
        "confidence": confidence,
        "explanation": ARCHETYPE_EXPLANATIONS.get(top_archetype, "No explanation available."),
        "tags": ARCHETYPE_TAGS.get(top_archetype, []),
        "score_breakdown": normalized_scores,
        "ranked_scores": [{"archetype": k, "score": v} for k, v in sorted_norm]
    }
