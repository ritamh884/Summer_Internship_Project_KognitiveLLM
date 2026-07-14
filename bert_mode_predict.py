"""
====================================================================
            BERT TRANSACTION CATEGORY PREDICTION MODULE
====================================================================

Project:
AI-Powered Financial Document Analysis System

Description
-----------
This module is responsible for classifying bank transaction
descriptions into predefined spending categories using a
fine-tuned BERT (Bidirectional Encoder Representations from
Transformers) model.

The predicted categories help users understand their spending
patterns and are later used for financial analysis, expense
visualization, and dashboard reporting.

Workflow
--------
1. Load the trained BERT tokenizer and classification model.
2. Accept a transaction description as input.
3. Tokenize and preprocess the text.
4. Pass the text through the trained BERT model.
5. Predict the most probable spending category.
6. Return the predicted category.

Supported Categories
--------------------
• ATM Withdrawal
• Bills
• EMI
• Entertainment
• Food
• Fuel
• Groceries
• Insurance
• Investment
• Medical
• Others
• Salary
• Shopping
• Transfer
• Travel

Libraries Used
--------------
- transformers
- torch
- os

Author
------
Ritam Halder
B.Tech CSE (AI & ML)
The Neotia University
====================================================================
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# -------------------------------------------------------------------
# Model Configuration
# -------------------------------------------------------------------

# Path where the trained BERT model is stored
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "transaction_classifier"
)

# Automatically use GPU if available, otherwise use CPU
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -------------------------------------------------------------------
# Load Tokenizer and Model
# -------------------------------------------------------------------

print("Loading transaction classification model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.to(DEVICE)

# Set model to evaluation mode
model.eval()

print("Model loaded successfully.")

# -------------------------------------------------------------------
# Transaction Categories
# -------------------------------------------------------------------
# IMPORTANT:
# The order of these labels MUST exactly match the label IDs used
# during model training.

CATEGORIES = [
    "ATM Withdrawal",
    "Bills",
    "EMI",
    "Entertainment",
    "Food",
    "Fuel",
    "Groceries",
    "Insurance",
    "Investment",
    "Medical",
    "Others",
    "Salary",
    "Shopping",
    "Transfer",
    "Travel"
]

# -------------------------------------------------------------------
# Transaction Category Prediction
# -------------------------------------------------------------------

def predict_category(transaction_description):
    """
    Predict the spending category of a transaction.

    Parameters
    ----------
    transaction_description : str
        Transaction description extracted from the bank statement.

    Returns
    -------
    str
        Predicted spending category.

    Example
    -------
    >>> predict_category("SWIGGY BANGALORE")
    'Food'
    """

    # Check for empty or invalid input
    if not transaction_description or not transaction_description.strip():
        return "Others"

    # Convert transaction text into BERT input format
    encoded_input = tokenizer(
        transaction_description,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64
    )

    # Move tensors to the selected device
    encoded_input = {
        key: value.to(DEVICE)
        for key, value in encoded_input.items()
    }

    # Disable gradient calculation for faster inference
    with torch.no_grad():
        outputs = model(**encoded_input)

    # Select the class with the highest probability
    predicted_index = torch.argmax(outputs.logits, dim=1).item()

    # Return category safely
    if 0 <= predicted_index < len(CATEGORIES):
        return CATEGORIES[predicted_index]

    return "Others"


# -------------------------------------------------------------------
# Standalone Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    sample_transactions = [
        "SWIGGY PAYMENT",
        "AMAZON INDIA",
        "HP PETROL PUMP",
        "SALARY CREDIT",
        "IRCTC BOOKING",
        "NETFLIX SUBSCRIPTION"
    ]

    print("\nSample Predictions\n")

    for transaction in sample_transactions:
        category = predict_category(transaction)
        print(f"{transaction:<30} --> {category}")