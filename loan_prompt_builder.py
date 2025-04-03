# prompt_from_profile.py

import json

def build_loan_prompt_from_profile(profile: dict, loan_purpose: str, preferred_features: list, loan_products: list) -> str:
    """
    Generates a structured GPT prompt for loan recommendations based on the user profile,
    loan purpose, preferred features, and available loan products.
    
    Args:
        profile (dict): The user profile output from the archetype engine.
        loan_purpose (str): The stated purpose for the loan.
        preferred_features (list[str]): Preferred loan features.
        loan_products (list[dict]): List of available loan products.
    
    Returns:
        str: A complete prompt to be sent to GPT.
    """
    
    # Extract key persona details from the profile.
    persona_label = profile.get("top_archetype", "N/A")
    # Optionally, you can incorporate other metrics from score_breakdown or additional fields if available.
    # For example, you might show a summary of key ratios or scores.
    
    # Build the "User Persona" section.
    persona_section = (
        "**User Persona:**\n"
        f"- Persona Label: {persona_label}\n"
        f"- Confidence: {profile.get('confidence', 'N/A') * 100:.1f}%\n"
    )
    
    # You might add additional details from profile if available.
    
    # Build the "User Stated Need" section.
    need_section = (
        "**User Stated Need:**\n"
        f"- Loan Purpose: {loan_purpose}\n"
        f"- Preferred Loan Features: {', '.join(preferred_features)}\n"
    )
    
    # Build the "Available Loan Products" section.
    product_lines = ["**Available Loan Products:**"]
    for idx, product in enumerate(loan_products, start=1):
        product_lines.append(f"Product {idx}:")
        product_lines.append(f"  - Lender Name: {product.get('lender_name', 'N/A')}")
        product_lines.append(f"  - Product Name: {product.get('product_name', 'N/A')}")
        product_lines.append(f"  - Loan Type: {product.get('loan_type', 'N/A')}")
        product_lines.append(f"  - APR Range: {product.get('apr_range', 'N/A')}")
        product_lines.append(f"  - Fees: {product.get('fees', 'N/A')}")
        features = product.get("features", [])
        product_lines.append(f"  - Features: {', '.join(features) if features else 'N/A'}")
        product_lines.append(f"  - Reputability: {product.get('reputability', 'N/A')}")
        product_lines.append(f"  - Other Details: {product.get('other_details', 'N/A')}")
        product_lines.append("")  # Blank line between products
    products_section = "\n".join(product_lines)
    
    # Build the "Instructions to GPT" section.
    instructions = [
        "Analyze the user persona and identify the key spending behaviors and risk category.",
        "Interpret the user's stated loan purpose and preferred loan features.",
        "Review the list of available loan products.",
        "Match the best loan products to the user persona and stated need.",
        "Justify your recommendations using the persona metrics and product features.",
        "Format the response as a numbered list with clear explanations."
    ]
    instructions_section = "**Instructions to GPT:**\n" + "\n".join([f"{i+1}. {instr}" for i, instr in enumerate(instructions)])
    
    # Combine all sections into the final prompt.
    final_prompt = (
        "Task: Recommend up to 3 best loan options based on the following information.\n\n"
        f"{persona_section}\n"
        f"{need_section}\n"
        f"{products_section}\n"
        f"{instructions_section}\n\n"
        "Please provide your answer as a numbered list with clear explanations for each recommendation."
    )
    
    return final_prompt

if __name__ == "__main__":
    # Load the profile output from the archetype engine.
    PROFILE_FILE = "output.json"
    with open(PROFILE_FILE, "r") as f:
        profile = json.load(f)
    
    # Example inputs for loan need and products.
    loan_purpose = "Home Renovation"
    preferred_features = ["Low Fees", "Fixed Interest Rate", "Reputable Lender"]
    
    loan_products = [
        {
            "lender_name": "ABC Bank",
            "product_name": "Smart Home Loan",
            "loan_type": "Home Improvement",
            "apr_range": "9% - 11%",
            "fees": "Processing Fee: ₹999",
            "features": ["Fixed Interest Rate", "Flexible Tenure"],
            "reputability": "High",
            "other_details": "Available to salaried and self-employed"
        },
        {
            "lender_name": "XYZ Finance",
            "product_name": "RenovatePlus Loan",
            "loan_type": "Home Renovation",
            "apr_range": "8.5% - 10%",
            "fees": "Processing Fee: ₹799, Prepayment charges apply",
            "features": ["Low Processing Fee", "No Prepayment Penalty"],
            "reputability": "Medium",
            "other_details": "Quick approval for renovation projects"
        }
    ]
    
    prompt = build_loan_prompt_from_profile(profile, loan_purpose, preferred_features, loan_products)
    
    # Save the generated prompt to a file for review.
    with open("loan_prompt.txt", "w") as f:
        f.write(prompt)
    
    print("Prompt generated and saved to loan_prompt.txt")
    print(prompt)
