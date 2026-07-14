"""
====================================================================
            BERT TRANSACTION CLASSIFICATION MODULE
====================================================================

Description
-----------
This module performs automatic transaction classification from a
bank statement using a fine-tuned BERT model.

The workflow is:

1. Load the trained BERT tokenizer and classification model.
2. Extract transaction descriptions from a bank statement PDF.
3. Clean and preprocess transaction text.
4. Predict the category of each transaction.
5. Group transactions according to their predicted category.
6. Return categorized results for dashboard visualization.

Typical Categories
------------------
• Food
• Shopping
• Travel
• Bills
• Entertainment
• Healthcare
• Fuel
• Salary
• Transfer
• Others

Libraries Used
--------------
- transformers
- torch
- pdfplumber
- pandas
- re

Author
------
Ritam Halder
B.Tech CSE (AI & ML)
The Neotia University
====================================================================
"""

import os
import re
import pdfplumber
import torch

from transformers import BertTokenizer, BertForSequenceClassification

# -------------------------------------------------------------------
# Model Configuration
# -------------------------------------------------------------------

# Folder containing the fine-tuned BERT model
MODEL_PATH = "bert_model"

# Automatically select GPU if available, otherwise CPU
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -------------------------------------------------------------------
# Load Tokenizer and Model
# -------------------------------------------------------------------

print("Loading BERT model...")

tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)

model = BertForSequenceClassification.from_pretrained(MODEL_PATH)

model.to(DEVICE)

# Put the model into evaluation mode
model.eval()

print("BERT model loaded successfully.")

# -------------------------------------------------------------------
# Category Labels
# -------------------------------------------------------------------

CATEGORY_LABELS = {
    0: "Food",
    1: "Shopping",
    2: "Travel",
    3: "Bills",
    4: "Entertainment",
    5: "Healthcare",
    6: "Fuel",
    7: "Salary",
    8: "Transfer",
    9: "Others"
}

# -------------------------------------------------------------------
# Utility Function
# -------------------------------------------------------------------

def clean_text(text):
    """
    Clean transaction description before sending it to BERT.
    """

    text = text.lower()

    # Remove digits
    text = re.sub(r"\d+", " ", text)

    # Remove special symbols
    text = re.sub(r"[^a-zA-Z ]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# -------------------------------------------------------------------
# Extract Transaction Descriptions
# -------------------------------------------------------------------

def extract_transactions(pdf_path):
    """
    Extract transaction descriptions from a bank statement PDF.

    Parameters
    ----------
    pdf_path : str
        Path of uploaded bank statement.

    Returns
    -------
    list
        List of transaction descriptions.
    """

    transactions = []

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if not text:
                    continue

                lines = text.split("\n")

                for line in lines:

                    line = line.strip()

                    if len(line) < 3:
                        continue

                    transactions.append(line)

    except Exception as error:

        print("PDF Extraction Error :", error)

    return transactions


# -------------------------------------------------------------------
# Predict Category
# -------------------------------------------------------------------

def predict_category(transaction):
    """
    Predict transaction category using the fine-tuned BERT model.
    """

    cleaned = clean_text(transaction)

    encoded = tokenizer(
        cleaned,
        max_length=64,
        truncation=True,
        padding="max_length",
        return_tensors="pt"
    )

    encoded = {k: v.to(DEVICE) for k, v in encoded.items()}

    with torch.no_grad():

        output = model(**encoded)

    prediction = torch.argmax(output.logits, dim=1).item()

    return CATEGORY_LABELS.get(prediction, "Others")


# -------------------------------------------------------------------
# Main Analysis Function
# -------------------------------------------------------------------

def analyze_bank_statement(pdf_path):
    """
    Analyze an uploaded bank statement.

    Parameters
    ----------
    pdf_path : str

    Returns
    -------
    dict

    Example

    {
        "Food": 8,
        "Shopping": 4,
        "Bills": 2
    }
    """

    if not os.path.exists(pdf_path):
        return {"Error": "Bank statement not found."}

    transactions = extract_transactions(pdf_path)

    if len(transactions) == 0:
        return {"Error": "No transactions detected."}

    category_summary = {}

    for transaction in transactions:

        category = predict_category(transaction)

        category_summary[category] = (
            category_summary.get(category, 0) + 1
        )

    return category_summary


# -------------------------------------------------------------------
# Standalone Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    sample_pdf = "sample_bank_statement.pdf"

    if os.path.exists(sample_pdf):

        result = analyze_bank_statement(sample_pdf)

        print("\nTransaction Summary\n")

        for category, count in result.items():
            print(f"{category:<15} : {count}")

    else:

        print("Sample bank statement not found.")