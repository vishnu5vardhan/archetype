# scoring_modules.py

from .archetype_config import ARCHETYPE_THRESHOLDS
from .archetype_explanations import ARCHETYPE_EXPLANATIONS, ARCHETYPE_TAGS

def calculate_archetype_scores(metrics):
    scores = {}
    
    # Score for Foodie & Entertainment Spender
    foodie_score = 0
    if metrics.get("dining_ratio", 0) >= ARCHETYPE_THRESHOLDS["dining_ratio"]:
        foodie_score += 1
    if metrics.get("total_discretionary_ratio", 0) >= ARCHETYPE_THRESHOLDS["total_discretionary_ratio"]:
        foodie_score += 1
    if metrics.get("dining_txn_count", 0) >= ARCHETYPE_THRESHOLDS["dining_txn_count"]:
        foodie_score += 1
    scores["Foodie & Entertainment Spender"] = foodie_score

    # Score for Retail Therapy Lover
    shopping_score = 0
    if metrics.get("shopping_ratio", 0) >= ARCHETYPE_THRESHOLDS["shopping_ratio"]:
        shopping_score += 1
    scores["Retail Therapy Lover"] = shopping_score

    # Other archetypes: (for now, they are not scoring any conditions)
    scores["Debt-Focused/Credit-Builder"] = 0
    scores["Budget-Focused Saver"] = 0
    scores["Premium Spender"] = 0
    scores["Balanced Spender"] = 0
    scores["Subscription Enthusiast"] = 0
    scores["Travel Enthusiast"] = 0

    return scores

def assign_archetype(metrics):
    scores = calculate_archetype_scores(metrics)
    total_score = sum(scores.values())
    
    # If no conditions are met, assign a default/fallback archetype.
    if total_score == 0:
        top_archetype = "Balanced Spender"  # or any default archetype you prefer
        confidence = 0.0
        score_breakdown = scores
        sorted_scores = [{"archetype": k, "score": v} for k, v in scores.items()]
    else:
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_archetype, top_score = sorted_scores[0]
    
        # Tie-breaker logic if needed
        top_candidates = [x for x in sorted_scores if x[1] == top_score]
        if len(top_candidates) > 1:
            discretionary_weights = {
                "Foodie & Entertainment Spender": metrics.get("dining_ratio", 0),
                "Retail Therapy Lover": metrics.get("shopping_ratio", 0),
                "Travel Enthusiast": metrics.get("avg_transaction_value", 0),
                "Premium Spender": metrics.get("avg_transaction_value", 0),
            }
            top_candidates = sorted(
                top_candidates,
                key=lambda x: discretionary_weights.get(x[0], 0),
                reverse=True
            )
            top_archetype = top_candidates[0][0]
    
        confidence = round(top_score / (total_score + 1e-6), 4)
        score_breakdown = dict(sorted_scores)
        # Convert sorted_scores back into the expected list format
        sorted_scores = [{"archetype": k, "score": v} for k, v in sorted_scores]
    
    return {
        "top_archetype": top_archetype,
        "confidence": confidence,
        "explanation": ARCHETYPE_EXPLANATIONS.get(top_archetype, "No explanation available."),
        "tags": ARCHETYPE_TAGS.get(top_archetype, []),
        "score_breakdown": score_breakdown,
        "ranked_scores": sorted_scores
    }
