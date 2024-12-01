# chart_utils.py

import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from matplotlib import rcParams

def create_bar_chart(items, title, output_path, max_items):
    """
    Creates a bar chart for the given items and saves it to the specified path.
    Ensures that all charts have the same height by using max_items.
    """
    # Reverse the items for right-to-left display
    labels = list(items.keys())[::-1]
    grades = list(items.values())[::-1]

    # Use get_display to handle RTL text
    labels = [get_display(label) for label in labels]
    title = get_display(title)

    # Set font to Arial (or another font that supports Hebrew)
    rcParams['font.family'] = 'Arial'

    # Calculate figure height based on max_items to keep consistent height
    figure_height = max_items * 0.5 + 1  # Adjust the multiplier as needed

    plt.figure(figsize=(8, figure_height))
    bars = plt.barh(labels, grades, color='skyblue', height=0.4)
    plt.xlabel(get_display("ציון"), fontsize=14)
    plt.title(title, fontsize=16)
    plt.xlim(0, 10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    # Add grade labels next to the bars
    for bar, grade in zip(bars, grades):
        plt.text(grade + 0.1, bar.get_y() + bar.get_height()/2, f'{grade}', va='center', fontsize=12)
    plt.savefig(output_path)
    plt.close()

def create_final_grade_chart(grades_data, output_path, max_items):
    """
    Creates a bar chart for the final grades of each part.
    Ensures consistent chart size using max_items.
    """
    parts = [part for part in grades_data if part != 'final_grade']
    averages = [grades_data[part]['average'] for part in parts]

    # Reverse the parts and averages for right-to-left display
    parts = parts[::-1]
    averages = averages[::-1]

    # Use get_display to handle RTL text
    parts = [get_display(part) for part in parts]
    title = get_display('ציון ממוצע לכל חלק')

    # Set font to Arial (or another font that supports Hebrew)
    rcParams['font.family'] = 'Arial'

    # Calculate figure height based on max_items
    figure_height = max_items * 0.5 + 1  # Adjust the multiplier as needed

    plt.figure(figsize=(8, figure_height))
    bars = plt.barh(parts, averages, color='lightgreen', height=0.4)
    plt.xlabel(get_display("ציון ממוצע"), fontsize=14)
    plt.title(title, fontsize=16)
    plt.xlim(0, 10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    # Add average labels next to the bars
    for bar, avg in zip(bars, averages):
        plt.text(avg + 0.1, bar.get_y() + bar.get_height()/2, f'{avg}', va='center', fontsize=12)
    plt.savefig(output_path)
    plt.close()
