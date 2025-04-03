# dynamic_prompt_builder.py
import json
def build_dynamic_prompt(intent: str, persona: dict, user_query: str, extra_context: dict = None) -> str:
    """
    Generates a dynamic GPT prompt based on the user's intent, persona, and additional context.

    Args:
        intent (str): The type of query (e.g., "loan_recommendation", "savings_plan", "salary_inquiry").
        persona (dict): User persona details (e.g., label, ratios, savings_rate, risk_category).
        user_query (str): The user’s natural language query or stated need.
        extra_context (dict): Additional context required for the prompt (e.g., available loan products, 
                              savings options, salary benchmarks).

    Returns:
        str: A fully constructed prompt.
    """
    # Define templates for different intents.
    templates = {
        "loan_recommendation": (
            "Task: Recommend up to 3 best loan options based on the following information.\n\n"
            "**User Persona:**\n"
            "- Persona Label: {persona_label}\n"
            "- Spending Ratios: {spending_ratios}\n"
            "- Savings Rate: {savings_rate}%\n"
            "- Risk Category: {risk_category}\n\n"
            "**User Stated Need:**\n"
            "- Loan Purpose: {user_query}\n"
            "- Preferred Features: {preferred_features}\n\n"
            "**Available Loan Products:**\n"
            "{loan_product_block}\n\n"
            "**Instructions to GPT:**\n"
            "1. Analyze the persona and stated need.\n"
            "2. Match loan products that best fit the user's profile.\n"
            "3. Provide a numbered list of recommendations with explanations."
        ),
        "savings_plan": (
            "Task: Suggest a personalized savings plan based on the following information.\n\n"
            "**User Persona:**\n"
            "- Persona Label: {persona_label}\n"
            "- Spending Ratios: {spending_ratios}\n"
            "- Savings Rate: {savings_rate}%\n"
            "- Risk Category: {risk_category}\n\n"
            "**User Query:** {user_query}\n\n"
            "**Additional Information:**\n"
            "{additional_info}\n\n"
            "**Instructions to GPT:**\n"
            "1. Analyze the persona and spending behavior.\n"
            "2. Recommend savings strategies that balance current spending with future goals.\n"
            "3. Format your recommendations as a numbered list with clear explanations."
        ),
        "salary_inquiry": (
            "Task: Provide insights on salary information and comparisons based on the following data.\n\n"
            "**User Persona:**\n"
            "- Persona Label: {persona_label}\n"
            "- Income Proxy: {income_proxy}\n\n"
            "**User Query:** {user_query}\n\n"
            "**Instructions to GPT:**\n"
            "1. Analyze the income details and compare with industry benchmarks.\n"
            "2. Provide actionable insights or recommendations regarding salary growth or negotiation.\n"
            "3. Present your response in a clear, numbered format."
        )
        # Add additional templates as needed.
    }

    # Choose the appropriate template based on the intent.
    template = templates.get(intent)
    if not template:
        raise ValueError(f"Intent '{intent}' is not supported. Please add a corresponding template.")

    # Prepare variables from persona.
    persona_label = persona.get("label", "N/A")
    ratios = persona.get("ratios", {})
    spending_ratios = ", ".join(f"{cat.capitalize()}: {value}%" for cat, value in ratios.items())
    savings_rate = persona.get("savings_rate", "N/A")
    risk_category = persona.get("risk_category", "N/A")
    income_proxy = persona.get("income_proxy", "N/A")  # If available

    # Prepare extra context depending on intent.
    additional_info = ""
    preferred_features = ""
    loan_product_block = ""

    if intent == "loan_recommendation":
        # Expect extra_context to include 'loan_products' and 'preferred_features'.
        preferred_features = ", ".join(extra_context.get("preferred_features", []))
        products = extra_context.get("loan_products", [])
        product_lines = []
        for idx, product in enumerate(products, start=1):
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
            product_lines.append("")
        loan_product_block = "\n".join(product_lines)
    
    elif intent == "savings_plan":
        additional_info = extra_context.get("additional_info", "")
    
    # Fill in the template using formatted strings.
    prompt = template.format(
        persona_label=persona_label,
        spending_ratios=spending_ratios,
        savings_rate=savings_rate,
        risk_category=risk_category,
        income_proxy=income_proxy,
        user_query=user_query,
        preferred_features=preferred_features,
        loan_product_block=loan_product_block,
        additional_info=additional_info
    )
    return prompt

# --------------------------------
# Example usage:
if __name__ == "__main__":
    # Load user profile from output.json (generated by your archetype engine)
    with open("output.json", "r") as f:
        profile = json.load(f)
    
    # Define a sample user query and extra context.
    # Change 'intent' to "loan_recommendation", "savings_plan", or "salary_inquiry" as needed.
    intent = "loan_recommendation"
    user_query = "I need a loan for home renovation."
    extra_context = {
        "preferred_features": ["Low Fees", "Fixed Interest Rate", "Reputable Lender"],
        "loan_products": [
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
    }
    
    # Build the prompt
    prompt = build_dynamic_prompt(intent, profile, user_query, extra_context)
    
    # Save the prompt to a file
    with open("loan_prompt.txt", "w") as f:
        f.write(prompt)
    
    print("Prompt generated and saved to loan_prompt.txt:")
    print(prompt)
