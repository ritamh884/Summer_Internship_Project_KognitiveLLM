import matplotlib

# Non-GUI backend for Flask
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os


def create_pie_chart(salary):

    labels = []
    values = []

    # Modern vibrant color palette
    palette = [
        "#00C853",   # Bright Green
        "#2979FF",   # Bright Blue
        "#FF6D00",   # Bright Orange
        "#AA00FF",   # Purple
        "#FF1744",   # Red
        "#00B8D4",   # Cyan
        "#FFD600",   # Yellow
        "#1DE9B6",   # Aqua
        "#FF4081",   # Pink
        "#651FFF"    # Indigo
    ]

    color_index = 0
    colors = []

    for key, value in salary.items():

        try:
            value = float(value)
        except:
            continue

        if value <= 0:
            continue

        labels.append(f"{key}   ₹{value:,.2f}")
        values.append(value)

        colors.append(palette[color_index % len(palette)])
        color_index += 1

    if len(values) == 0:
        return None

    os.makedirs("static/charts", exist_ok=True)

    chart_path = "static/charts/piechart.png"

    plt.rcParams["font.family"] = "DejaVu Sans"

    fig, ax = plt.subplots(
        figsize=(8,8),
        dpi=600,
        facecolor="white"
    )

    wedges, texts, autotexts = ax.pie(

        values,

        labels=None,

        colors=colors,

        startangle=90,

        counterclock=False,

        autopct=lambda p: f"{p:.1f}%",

        pctdistance=0.72,

        shadow=False,

        wedgeprops={
            "linewidth":0,      # No white separators
            "antialiased":True
        }

    )

    # Percentage style
    for txt in autotexts:

        txt.set_fontsize(12)

        txt.set_fontweight("bold")

        txt.set_color("white")

    ax.set_title(

        "Salary Components Distribution",

        fontsize=18,

        fontweight="bold",

        color="#1A237E",

        pad=18

    )

    ax.axis("equal")

    ax.legend(

        wedges,

        labels,

        title="Detected Salary Components",

        loc="upper center",

        bbox_to_anchor=(0.5,-0.08),

        ncol=2,

        fontsize=10,

        title_fontsize=12,

        frameon=False

    )

    plt.tight_layout()

    plt.savefig(

        chart_path,

        dpi=600,

        facecolor="white",

        bbox_inches="tight"

    )

    plt.close(fig)

    return chart_path