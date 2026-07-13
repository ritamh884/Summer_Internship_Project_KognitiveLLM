"""
====================================================================
           TRANSACTION CATEGORIZATION MODULE
====================================================================

Description
-----------
This module classifies bank transaction descriptions into predefined
expense and income categories using keyword-based matching. It serves
as a lightweight categorization approach for organizing transactions
before visualization and financial analysis.

Main Features
-------------
• Converts transaction descriptions to lowercase for uniform matching.
• Identifies common spending and income categories using keywords.
• Supports categories such as Food, Shopping, Transport, Medical,
  Recharge, Salary, Cash Withdrawal, and Cab.
• Assigns uncategorized transactions to the "Others" category.
• Provides categorized data for charts, reports, and dashboard
  visualization.

Technologies Used
-----------------
Python

====================================================================
"""
def get_category(description):

    text = description.lower()

    # Food
    if any(x in text for x in [
        "swiggy",
        "zomato",
        "faasos",
        "ovenstory",
        "dominos",
        "pizza",
        "restaurant",
        "food"
    ]):
        return "Food"

    # ATM

    elif "atm" in text or "atm wdl" in text:
        return "Cash Withdrawal"

    # Metro

    elif "metro" in text:
        return "Transport"

    # Ola Uber

    elif "ola" in text or "uber" in text:
        return "Cab"

    # Recharge

    elif any(x in text for x in [
        "jio",
        "airtel",
        "vodafone",
        "recharge",
        "billdesk"
    ]):
        return "Recharge"

    # Shopping

    elif any(x in text for x in [
        "amazon",
        "amzn",
        "flipkart",
        "myntra"
    ]):
        return "Shopping"

    # Medical

    elif any(x in text for x in [
        "medical",
        "pharmacy",
        "medicine"
    ]):
        return "Medical"

    # Salary

    elif any(x in text for x in [
        "salary",
        "huey tech",
        "company",
        "credit interest"
    ]):
        return "Salary"

    else:
        return "Others"