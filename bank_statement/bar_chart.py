"""
====================================================================
           BANK STATEMENT VISUALIZATION MODULE
====================================================================

Description
-----------
This module generates graphical representations of bank statement
transactions using Matplotlib. It processes debit and credit amounts
to create informative bar charts that help analyze income, expenses,
and overall transaction patterns.

Main Features
-------------
• Cleans and validates debit and credit amounts.
• Generates transaction-wise bar charts.
• Differentiates debit and credit transactions using distinct colors.
• Highlights the highest-value transactions.
• Automatically saves charts for display in the Flask dashboard.

Technologies Used
-----------------
Python • Pandas • Matplotlib • Flask

====================================================================
"""
import matplotlib

# Required for Flask
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os


def clean_amount(value):

    if value is None:
        return 0

    value = str(value).replace(",", "").replace("₹", "").strip()

    if value == "" or value == "-":
        return 0

    try:
        return float(value)
    except:
        return 0


def create_bar_chart(df):

    descriptions = []
    amounts = []
    colors = []
    labels = []

    for _, row in df.iterrows():

        description = str(row.get("Description", ""))

        debit = clean_amount(row.get("Debit", 0))
        credit = clean_amount(row.get("Credit", 0))

        # Short description
        if len(description) > 22:
            description = description[:22] + "..."

        if credit > 0:

            descriptions.append(description)
            amounts.append(credit)
            colors.append("#2ecc71")      # Bright Green
            labels.append(f"{credit:,.2f}\n(CR)")

        elif debit > 0:

            descriptions.append(description)
            amounts.append(debit)
            colors.append("#e74c3c")      # Bright Red
            labels.append(f"{debit:,.2f}\n(DB)")

    if len(amounts) == 0:
        return None

    os.makedirs("static/charts", exist_ok=True)

    path = "static/charts/barplot.png"

    plt.figure(figsize=(14,7))

    bars = plt.bar(
        descriptions,
        amounts,
        color=colors,
        edgecolor="black",
        linewidth=1.2
    )

    plt.title(
        "Bank Transaction Analysis",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel(
        "Transaction Description",
        fontsize=12
    )

    plt.ylabel(
        "Amount (₹)",
        fontsize=12
    )

    plt.xticks(
        rotation=35,
        ha="right",
        fontsize=10
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    # Show CR / DB on every bar
    for bar, label in zip(bars, labels):

        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width()/2,
            height,
            label,
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold"
        )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close()

    return path
def create_bar(df):

    df["Amount"] = df["Debit"].fillna(0)

    df.loc[df["Amount"] == 0, "Amount"] = df["Credit"]

    top = df.sort_values(
        "Amount",
        ascending=False
    ).head(7)

    labels = top["Category"]

    values = top["Amount"]

    colors = []

    for _, row in top.iterrows():

        if row["Credit"] > 0:
            colors.append("green")
        else:
            colors.append("red")

    plt.figure(figsize=(12,6))

    bars = plt.bar(
        labels,
        values,
        color=colors
    )

    for i, row in top.iterrows():

        txt = "CR" if row["Credit"] > 0 else "DB"

        plt.text(
            row["Category"],
            row["Amount"]+50,
            txt,
            ha="center",
            fontweight="bold"
        )

    plt.title("Top 7 Transactions")

    plt.ylabel("Amount (₹)")

    plt.tight_layout()

    os.makedirs("static/charts",exist_ok=True)

    plt.savefig("static/charts/bar.png")

    plt.close()