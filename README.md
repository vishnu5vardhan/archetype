# Financial Archetype Engine

This project is a transaction analysis system that categorizes users into financial archetypes based on their spending patterns and financial behavior.

## Overview

The Financial Archetype Engine analyzes transaction data to determine the most appropriate financial archetype for a user. These archetypes help financial institutions provide personalized product recommendations and services.

## Archetypes

The system identifies the following archetypes:

- **Foodie & Entertainment Spender**: Users who spend significantly on dining and entertainment
- **Retail Therapy Lover**: Users who frequently shop and make retail purchases
- **Premium Spender**: Users with high-value transactions and premium category spending
- **Travel Enthusiast**: Users who spend significantly on travel
- **Debt-Focused/Credit-Builder**: Users with significant debt-related transactions
- **Budget-Focused Saver**: Users who prioritize saving and limit discretionary spending
- **Subscription Enthusiast**: Users with many subscription services
- **Balanced Spender**: Users with well-distributed spending across categories

## Recent Improvements

The archetype engine has been significantly improved with the following changes:

1. **Enhanced Metric Calculation**:
   - Added proper recognition of transaction types (credit vs. debit)
   - Improved detection of premium transactions
   - Added more comprehensive metrics like unique merchants, category variance, and high-value transaction counts

2. **Optimized Scoring Logic**:
   - Consolidated configuration files to eliminate inconsistencies
   - Implemented a more robust scoring algorithm with better normalization
   - Added better tie-breaker logic for close scoring archetypes

3. **Better Confidence Scoring**:
   - New confidence calculation based on the gap between top archetypes
   - More accurate confidence ratings that reflect the certainty of classification

4. **Improved Transaction Processing**:
   - Better handling of transaction categories
   - Proper calculation of discretionary vs essential spending
   - Fixed bugs in category-based metrics

5. **Penalty Factors**:
   - Added penalty factors for archetypes when key indicators are missing
   - Prevents misclassification of users with weak archetype signals
   - Reduces incorrect tagging of users as Foodie & Entertainment when dining spend is minimal

6. **Enhanced Balanced Spender Detection**:
   - Improved category variance calculations
   - Added bonus for good distribution across multiple categories
   - Better recognition of truly balanced spending patterns

## Usage

To use the archetype engine:

```python
from archetype_engine.assign_archetype import assign_user_profile

# Load your transactions (list of transaction dictionaries)
transactions = [
    {"amount": 500, "transaction_type": "debit", "category": "Dining", "merchant_name": "Restaurant A"},
    {"amount": 50000, "transaction_type": "credit", "category": "Salary", "merchant_name": "Employer Inc"},
    # ... more transactions
]

# Get the archetype profile
result = assign_user_profile(transactions)

# Access the results
top_archetype = result["top_archetype"]
confidence = result["confidence"]
explanation = result["explanation"]
```

## Running the CLI Tool

The project includes a command-line tool for quick testing:

```bash
python3 main.py [path_to_sample_file]
```

If no file is provided, it will use the default sample file.

## Transaction Format

Each transaction should be a dictionary with the following fields:

- `amount`: Transaction amount (numeric)
- `transaction_type`: Either "credit" (money in) or "debit" (money out)
- `category`: Category of transaction (e.g., "Dining", "Shopping", "Salary")
- `merchant_name`: Name of the merchant (optional, improves categorization)
- `date_time`: Transaction date and time (optional)

## Debugging

The main CLI tool now provides detailed debugging information:

- Key metrics calculated from transactions
- Raw scores for each archetype (pre-softmax)
- Final normalized scores and confidence level

## Sample Files

The project includes several sample transaction files for testing:
- `sample123r.json`: Premium spender profile
- `sample_balanced_user.json`: Balanced spender profile
- `sample_foodie_entertainment_user.json`: Foodie & entertainment spender profile
- `sample_test_retail_balanced.json`: Retail therapy lover profile
