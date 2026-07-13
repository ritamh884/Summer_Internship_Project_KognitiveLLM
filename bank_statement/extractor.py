"""
====================================================================
           BANK STATEMENT EXTRACTION MODULE
====================================================================

Description
-----------
This module extracts transaction data from bank statement PDF files
using pdfplumber. It automatically identifies important columns such
as Date, Description, Debit, Credit, and Balance, converts the
extracted data into a Pandas DataFrame, and categorizes transactions
using keyword-based classification.

Main Features
-------------
• Extracts transaction tables from PDF bank statements.
• Detects standard banking columns automatically.
• Converts transaction records into a structured DataFrame.
• Classifies transactions into predefined spending categories.
• Cleans and converts debit and credit amounts into numeric values.
• Provides processed data for financial analysis and visualization.

Technologies Used
-----------------
Python • pdfplumber • Pandas

====================================================================
"""
import pdfplumber
import pandas as pd
from bank_statement.category import get_category


def normalize(text):
    if text is None:
        return ""
    return str(text).strip().lower()


def find_column(header):

    columns = {}

    for i, col in enumerate(header):

        col = normalize(col)

        # Date
        if any(x in col for x in [
            "date",
            "txn date",
            "transaction date"
        ]):
            columns["Date"] = i

        # Description
        elif any(x in col for x in [
            "description",
            "particular",
            "narration",
            "remarks",
            "transaction details",
            "details"
        ]):
            columns["Description"] = i

        # Debit
        elif any(x in col for x in [
            "debit",
            "withdrawal",
            "withdraw",
            "dr"
        ]):
            columns["Debit"] = i

        # Credit
        elif any(x in col for x in [
            "credit",
            "deposit",
            "cr"
        ]):
            columns["Credit"] = i

        # Balance
        elif any(x in col for x in [
            "balance",
            "current balance",
            "closing balance",
            "available balance"
        ]):
            columns["Balance"] = i

    return columns


def extract_bank_statement(pdf_path):

    records = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:

                if len(table) < 2:
                    continue

                header = table[0]

                cols = find_column(header)

                if "Description" not in cols:
                    continue

                for row in table[1:]:

                    if row is None:
                        continue

                    item = {}

                    for key, index in cols.items():

                        if index < len(row):

                            item[key] = row[index]

                        else:

                            item[key] = ""

                    records.append(item)

    return pd.DataFrame(records)



def extract_bank_statement(pdf_path):

    records = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:

                if len(table) < 2:
                    continue

                header = table[0]

                cols = find_column(header)

                if "Description" not in cols:
                    continue

                for row in table[1:]:

                    if row is None:
                        continue

                    item = {}

                    for key, index in cols.items():

                        if index < len(row):
                            item[key] = row[index]
                        else:
                            item[key] = ""

                    records.append(item)

    # Create DataFrame
    df = pd.DataFrame(records)

    # If Description column exists, classify transactions
    if "Description" in df.columns:
        df["Category"] = df["Description"].fillna("").apply(get_category)

    # Convert Debit and Credit to numeric
    if "Debit" in df.columns:
        df["Debit"] = (
            df["Debit"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["Debit"] = pd.to_numeric(df["Debit"], errors="coerce").fillna(0)

    if "Credit" in df.columns:
        df["Credit"] = (
            df["Credit"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["Credit"] = pd.to_numeric(df["Credit"], errors="coerce").fillna(0)

    return df
