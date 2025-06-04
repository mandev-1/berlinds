import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CONNECT_TO_DB import setup_connection
import matplotlib.pyplot as plt
import psycopg2

def visualize_pie_chart(param):
    # Create 'generated' directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), '../generated')
    os.makedirs(output_dir, exist_ok=True)

    # Connect to the database
    conn = setup_connection()
    cursor = conn.cursor()

    # Query to get the number of customers by country
    cursor.execute(f"SELECT {param}, COUNT(*) FROM customers GROUP BY {param};")
    data = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Prepare data for pie chart
    labels = [row[0] for row in data]
    counts = [row[1] for row in data]

    # Helper to format numbers with spaces as thousand separators
    def format_number(n):
        return f"{n:,}".replace(",", " ")

    # Create pie chart
    plt.figure(figsize=(10, 6))
    wedges, texts, autotexts = plt.pie(
        counts, labels=None, autopct='%1.1f%%', startangle=140
    )
    plt.title(f'Distribution of records by "{param}"')
    plt.setp(autotexts, size=10, weight="bold", color="white")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Build legend labels with nicely formatted counts
    legend_labels = [f"{label} ({format_number(count)})" for label, count in zip(labels, counts)]
    plt.legend(wedges, legend_labels, title=param, loc="center left", bbox_to_anchor=(1, 0.5))

    # Save the pie chart as a PNG in 'generated'
    plt.savefig(os.path.join(output_dir, "pie_chart.png"), bbox_inches='tight')
    # plt.show()

visualize_pie_chart("event_type")