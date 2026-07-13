"""
====================================================================
           TRANSACTION VISUALIZATION MODULE
====================================================================

Description
-----------
This module generates graphical representations of categorized bank
transactions using Matplotlib. It summarizes transaction amounts by
category and creates professional bar charts and pie charts to help
users understand their spending patterns and financial activities.

Main Features
-------------
• Calculates transaction amounts from debit and credit values.
• Excludes uncategorized ("Others") transactions from analysis.
• Groups transactions by category and computes total spending.
• Generates a bar chart for the top transaction categories.
• Creates a pie chart showing category-wise expense distribution.
• Automatically saves charts for display in the Flask dashboard.

Technologies Used
-----------------
Python • Pandas • Matplotlib • Flask

====================================================================
"""
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os


def create_bar(df):

    df["Amount"] = df["Debit"].fillna(0)
    df.loc[df["Amount"] == 0, "Amount"] = df["Credit"]

    # Remove Others
    df = df[df["Category"] != "Others"]

    # Sum by category
    summary = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(7)
    )

    labels = summary.index.tolist()
    values = summary.values.tolist()

    colors = [
        "#FF6B6B",
        "#4ECDC4",
        "#FFD93D",
        "#6C5CE7",
        "#00B894",
        "#0984E3",
        "#E17055"
    ]

    plt.figure(figsize=(10,6))

    bars = plt.bar(
        labels,
        values,
        color=colors[:len(labels)],
        width=0.55
    )

    for bar, value in zip(bars, values):

        plt.text(
            bar.get_x() + bar.get_width()/2,
            value + value*0.02,
            f"₹{value:,.0f}",
            ha="center",
            fontsize=10,
            fontweight="bold"
        )

    plt.title(
        "Top 7 Transaction Categories",
        fontsize=16,
        fontweight="bold"
    )

    plt.ylabel("Amount (₹)", fontsize=12)

    plt.xticks(fontsize=10)

    plt.grid(axis="y", linestyle="--", alpha=0.35)

    plt.tight_layout()

    os.makedirs("static/charts", exist_ok=True)

    plt.savefig(
        "static/charts/bar.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()
def create_pie(df):

    df["Amount"] = df["Debit"].fillna(0)
    df.loc[df["Amount"] == 0, "Amount"] = df["Credit"]

    # Remove Others
    df = df[df["Category"] != "Others"]

    pie = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(7)
    )

    colors = [
        "#FF6B6B",
        "#4ECDC4",
        "#FFD93D",
        "#6C5CE7",
        "#00B894",
        "#0984E3",
        "#E17055"
    ]

    plt.figure(figsize=(8,8))

    wedges, _, autotexts = plt.pie(

        pie.values,

        labels=None,

        colors=colors[:len(pie)],

        autopct="%1.1f%%",

        startangle=90,

        pctdistance=0.75,

        textprops={
            "fontsize":10,
            "fontweight":"bold",
            "color":"white"
        }

    )

    plt.title(
        "Top 7 Transaction Categories",
        fontsize=15,
        fontweight="bold"
    )

    legend_labels = [
        f"{cat} (₹{amt:,.0f})"
        for cat, amt in zip(pie.index, pie.values)
    ]

    plt.legend(

        wedges,

        legend_labels,

        title="Categories",

        loc="lower center",

        bbox_to_anchor=(0.5, -0.18),

        ncol=2,

        fontsize=10,

        frameon=False

    )

    plt.axis("equal")

    plt.tight_layout()

    os.makedirs("static/charts", exist_ok=True)

    plt.savefig(
        "static/charts/pie.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()
