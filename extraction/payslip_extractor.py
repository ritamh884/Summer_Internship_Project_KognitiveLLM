"""
====================================================================
             PAYSLIP SALARY EXTRACTION MODULE
====================================================================

Description
-----------
This module extracts salary components from OCR-generated payslip
text using Regular Expressions (Regex). It identifies key salary
fields and returns them in a structured format for loan eligibility
assessment and salary visualization.

Main Features
-------------
• Searches OCR text for predefined salary components.
• Extracts numerical values using Regular Expressions.
• Identifies Basic Pay, HRA, Medical, Conveyance, Other,
  Gross Salary, and Net Salary.
• Returns salary details as a Python dictionary for further analysis.

Technologies Used
-----------------
Python • Regular Expressions (re)

====================================================================
"""
import re

def find_amount(keyword, text):
    """
    Finds the first number that appears after a keyword.
    """

    pattern = rf"{keyword}.*?([\d]+(?:\.\d+)?)"

    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    if match:
        try:
            return float(match.group(1))
        except:
            return 0

    return 0


def extract_salary(text):

    salary = {

        "Basic": find_amount("Basic", text),

        "HRA": find_amount("House Rent", text),

        "Medical": find_amount("Medical", text),

        "Conveyance": find_amount("Conveyance", text),

        "Other": find_amount("Other", text),

        "Gross": find_amount("Gross", text),

        "Net": find_amount("Net", text)

    }

    return salary