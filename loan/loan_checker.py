"""
====================================================================
              LOAN ELIGIBILITY ASSESSMENT MODULE
====================================================================

Description
-----------
This module evaluates an applicant's loan eligibility based on the
salary information extracted from a payslip. It compares the Net
Salary and Gross Salary, determines the effective monthly income,
and checks whether it meets the predefined loan eligibility criteria.

Main Features
-------------
• Extracts Net Salary and Gross Salary from salary data.
• Determines the effective monthly income.
• Evaluates loan eligibility based on the income threshold.
• Returns the eligibility status, display color, and calculated income.
• Supports integration with the Flask dashboard and result page.

Technologies Used
-----------------
Python

====================================================================
"""
def check_loan_eligibility(salary):

    # Try to find Net Salary
    net_salary = 0

    for key, value in salary.items():

        if "net" in key.lower():

            try:
                net_salary = float(value)
            except:
                pass

    # Try to find Gross/Total Salary
    gross_salary = 0

    for key, value in salary.items():

        if ("gross" in key.lower()) or ("total" in key.lower()):

            try:
                gross_salary = float(value)
            except:
                pass

    # Use the higher value
    income = max(net_salary, gross_salary)

    if income >= 20000:

        return (
            "Eligible for Loan",
            "#16A34A",
            income
        )

    else:

        return (
            "Not Eligible for Loan",
            "#DC2626",
            income
        )