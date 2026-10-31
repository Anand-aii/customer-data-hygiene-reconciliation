import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

OUT = Path("portfolio")
OUT.mkdir(exist_ok=True)

BG = "#F3F6FB"
NAVY = "#142B4A"
BLUE = "#2878D0"
GREEN = "#21966B"
ORANGE = "#E69A35"
RED = "#D95757"
GREY = "#64748B"
LIGHT = "#E3EAF3"

def base(title, subtitle):
    fig = plt.figure(figsize=(10, 7.5), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.06, 0.93, title, fontsize=20,
            fontweight="bold", color=NAVY)
    ax.text(0.06, 0.885, subtitle,
            fontsize=8.5, color=GREY)
    ax.text(0.94, 0.93, "PORTFOLIO DEMO",
            fontsize=8, color=BLUE,
            ha="right", fontweight="bold")
    return fig, ax

def card(ax, x, y, w, h, label, value, color):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.008,rounding_size=0.015",
        facecolor="white",
        edgecolor="#E1E8F0",
        linewidth=0.8
    ))

    # Separate label and number positions
    ax.text(x+w/2, y+h*0.72, label,
            fontsize=7.5, color=GREY,
            ha="center", va="center")

    ax.text(x+w/2, y+h*0.30, str(value),
            fontsize=19, fontweight="bold",
            color=color, ha="center", va="center")

def metric_cards(ax, metrics):
    start_x = 0.06
    width = 0.205
    gap = 0.023

    for i, (label, value, color) in enumerate(metrics):
        card(ax, start_x+i*(width+gap),
             0.70, width, 0.13,
             label, value, color)

def aligned_row(ax, y, label, value, maximum, color):
    # Column 1: Fixed label position
    ax.text(0.075, y, label,
            fontsize=9, color=NAVY,
            ha="left", va="center")

    # Column 2: Fixed progress bar position
    bar_x = 0.39
    bar_width = 0.42
    bar_height = 0.023

    ax.add_patch(FancyBboxPatch(
        (bar_x, y-bar_height/2),
        bar_width, bar_height,
        boxstyle="round,pad=0.002,rounding_size=0.008",
        facecolor=LIGHT, edgecolor="none"
    ))

    progress = bar_width * value / maximum

    if progress > 0:
        ax.add_patch(FancyBboxPatch(
            (bar_x, y-bar_height/2),
            progress, bar_height,
            boxstyle="round,pad=0.002,rounding_size=0.008",
            facecolor=color, edgecolor="none"
        ))

    # Column 3: Fixed right-aligned number
    ax.text(0.92, y, str(value),
            fontsize=10, fontweight="bold",
            color=NAVY, ha="right", va="center")

def section_title(ax, text, y):
    ax.text(0.07, y, text,
            fontsize=11, fontweight="bold",
            color=NAVY, va="center")

def footer(ax, text):
    ax.text(0.5, 0.025, text,
            fontsize=7.2, color=GREY,
            ha="center", va="center")

# ==========================================
# DASHBOARD 1: CUSTOMER DATA HYGIENE
# ==========================================

fig, ax = base(
    "CUSTOMER DATA HYGIENE",
    "Data cleaning | Quality checks | Segmentation | Suppression audit"
)

metric_cards(ax, [
    ("MASTER RECORDS", 515, BLUE),
    ("DUPLICATES FLAGGED", 15, ORANGE),
    ("PASSED CLEANING", 467, GREEN),
    ("NEEDS REVIEW", 48, RED)
])

section_title(ax, "SEGMENT EXPORT RESULTS", 0.625)

segments = [
    ("Lapsed", 121),
    ("Proposal Abandoned", 111),
    ("Web Engagers", 126),
    ("Product Expiration", 147)
]

for i, (label, value) in enumerate(segments):
    aligned_row(
        ax,
        0.55-i*0.075,
        label,
        value,
        147,
        BLUE
    )

section_title(ax, "EXPORT SUMMARY", 0.235)

summary = [
    ("TOTAL EXPORTED", 505, GREEN),
    ("SUPPRESSED", 10, ORANGE),
    ("SUPPRESSED IN EXPORTS", 0, GREEN)
]

for i, (label, value, color) in enumerate(summary):
    card(ax, 0.06+i*0.30, 0.085,
         0.27, 0.105, label, value, color)

footer(
    ax,
    "Synthetic fictional data | Demonstration project | Not real client data"
)

fig.savefig(
    OUT / "customer_data_hygiene_dashboard.png",
    dpi=100, facecolor=BG
)
plt.close(fig)

# ==========================================
# DASHBOARD 2: CUSTOMER RECONCILIATION
# ==========================================

fig, ax = base(
    "CUSTOMER RECONCILIATION",
    "Record matching | Exception handling | Manual review"
)

metric_cards(ax, [
    ("SOURCE RECORDS", 30, BLUE),
    ("EMAIL MATCHES", 10, GREEN),
    ("PHONE MATCHES", 10, BLUE),
    ("FUZZY SUGGESTIONS", 5, ORANGE)
])

section_title(ax, "RECONCILIATION CLASSIFICATIONS", 0.625)

classifications = [
    ("Exact email matches", 10, GREEN),
    ("Exact phone matches", 10, BLUE),
    ("Possible fuzzy matches", 5, ORANGE),
    ("Unmatched records", 5, RED)
]

for i, (label, value, color) in enumerate(classifications):
    aligned_row(
        ax,
        0.55-i*0.075,
        label,
        value,
        10,
        color
    )

section_title(ax, "REVIEW SUMMARY", 0.235)

card(
    ax, 0.15, 0.085, 0.30, 0.105,
    "MANUAL REVIEW REQUIRED", 10, ORANGE
)

card(
    ax, 0.55, 0.085, 0.30, 0.105,
    "TOTAL CLASSIFIED", 30, GREEN
)

footer(
    ax,
    "Fuzzy matches require human verification | Synthetic demo data"
)

fig.savefig(
    OUT / "customer_reconciliation_dashboard.png",
    dpi=100, facecolor=BG
)
plt.close(fig)

print("\nSUCCESS: Both dashboards generated!")
print("-------------------------------------")
print("1. portfolio/customer_data_hygiene_dashboard.png")
print("2. portfolio/customer_reconciliation_dashboard.png")
print("\nImage dimensions: 1000 x 750 pixels")
print("All row labels, bars and numbers use fixed columns.")
