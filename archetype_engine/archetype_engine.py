# assign_archetype.py

"""
This module ties together the metrics calculation and the
scoring logic to assign the user an archetype.
"""

from .metrics import compute_metrics
from .scoring_modules import calculate_archetype_scores
from .scoring_modules import get_archetype_explanation, get_archetype_tags

def assign_user_profile(transactions):
    """
    Main function to compute metrics for the user's transactions,
    calculate scores for each archetype, and determine the top archetype.

    Args:
        transactions (list): A list of transaction dicts, each containing:
            - amount (float)
            - transaction_type ('debit' or 'credit')
            - category (str) e.g. 'Dining', 'Shopping', 'Savings', etc.

    Returns:
        dict: A dictionary containing:
            - top_archetype (str): The best-fitting archetype
            - confidence (float): The ratio of top archetype score to sum of all scores
            - explanation (str): Why the user got this archetype
            - tags (list): Additional labels describing this archetype
            - score_breakdown (dict): The raw scores for each archetype
            - metrics (dict): Key user metrics for reference
            - ranked_scores (list): Archetypes sorted by score in descending order
    """

    # 1. Compute user metrics based on their transaction data
    user_metrics = compute_metrics(transactions)

    # 2. Calculate a score for each archetype
    archetype_scores = calculate_archetype_scores(user_metrics)

    # 3. Sort the archetypes by their scores (descending)
    sorted_scores = sorted(archetype_scores.items(), key=lambda x: x[1], reverse=True)
    if not sorted_scores:
        # In case no archetype scores are generated (unlikely if code is correct)
        return {
            "top_archetype": "No Archetype",
            "confidence": 0.0,
            "explanation": "No archetypes were scored.",
            "tags": [],
            "score_breakdown": {},
            "metrics": user_metrics,
            "ranked_scores": []
        }

    # 4. Identify the best-fitting archetype
    top_archetype, top_score = sorted_scores[0]
    total_score = sum([score for _, score in sorted_scores])
    confidence = round(top_score / total_score, 4) if total_score else 0.0

    # 5. Construct the final output
    explanation = get_archetype_explanation(top_archetype)
    tags = get_archetype_tags(top_archetype)

    result = {
        "top_archetype": top_archetype,
        "confidence": confidence,
        "explanation": explanation,
        "tags": tags,
        "score_breakdown": dict(sorted_scores),
        "metrics": user_metrics,
        "ranked_scores": [{"archetype": a, "score": s} for a, s in sorted_scores]
    }

    return result
