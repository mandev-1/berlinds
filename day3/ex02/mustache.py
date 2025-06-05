import sys
import os
import math
from decimal import Decimal
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CONNECT_TO_DB import setup_connection

def percentile(sorted_list, percent):
    k = (len(sorted_list) - 1) * float(percent)
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return sorted_list[int(k)]
    return sorted_list[f] * Decimal(str(c - k)) + sorted_list[c] * Decimal(str(k - f))

def print_price_statistics():
    logging.info("Starting price statistics computation.")
    try:
        conn = setup_connection()
        cur = conn.cursor()
        cur.execute("SELECT price FROM customers WHERE price IS NOT NULL;")
        prices = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Database error: {e}")
        return

    if not prices:
        logging.warning("No prices found.")
        print("No prices found.")
        return

    prices.sort()
    n = len(prices)
    mean = sum(prices) / n
    std = math.sqrt(sum((x - mean) ** 2 for x in prices) / n)
    stats = [
        ("count", n),
        ("mean", mean),
        ("std", std),
        ("min", prices[0]),
        ("25%", percentile(prices, 0.25)),
        ("50%", percentile(prices, 0.5)),
        ("75%", percentile(prices, 0.75)),
        ("max", prices[-1])
    ]
    for label, value in stats:
        print(f"{label} {value:.6f}")
    logging.info("Finished price statistics computation.")

def ensure_output_dir():
    output_dir = os.path.join(os.path.dirname(__file__), '../generated')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def boxplot_item_prices():
    """Generate horizontal boxplot for item prices - matches your first image"""
    logging.info("Generating boxplot for item prices.")
    try:
        conn = setup_connection()
        cur = conn.cursor()
        cur.execute("SELECT price FROM customers WHERE price IS NOT NULL;")
        prices = [float(row[0]) for row in cur.fetchall()]
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Database error: {e}")
        return

    if not prices:
        logging.warning("No prices found.")
        print("No prices found.")
        return

    output_dir = ensure_output_dir()
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#f0f0f0')
    ax.set_facecolor('#f0f0f0')
    sns.boxplot(x=prices, orient='h', color='white', linewidth=1, fliersize=3, ax=ax)
    ax.set_xlabel('price', fontsize=12)
    ax.set_ylabel('')
    ax.set_title('')
    ax.grid(True, alpha=0.3, color='gray')
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('black')
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'boxplot_item_prices.png')
    plt.savefig(output_path, dpi=150, facecolor='#f0f0f0', bbox_inches='tight')
    plt.close()
    logging.info(f"Boxplot saved to {output_path}")

def boxplot_item_prices_vertical_green():
    """Generate vertical green boxplot for item prices - matches your second image"""
    logging.info("Generating vertical green boxplot for item prices.")
    try:
        conn = setup_connection()
        cur = conn.cursor()
        cur.execute("SELECT price FROM customers WHERE price IS NOT NULL;")
        prices = [float(row[0]) for row in cur.fetchall()]
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Database error: {e}")
        return

    if not prices:
        logging.warning("No prices found.")
        print("No prices found.")
        return

    output_dir = ensure_output_dir()
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#f0f0f0')
    ax.set_facecolor('#f0f0f0')
    sns.boxplot(y=prices, color='#90c695', linewidth=1, fliersize=3, ax=ax)
    ax.set_ylabel('price', fontsize=12)
    ax.set_xlabel('')
    ax.set_title('')
    ax.grid(True, alpha=0.3, color='gray')
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_color('black')
    plt.tight_layout()
    # Save as boxplot_item_prices-2.png to match Makefile
    output_path = os.path.join(output_dir, 'boxplot_item_prices-2.png')
    plt.savefig(output_path, dpi=150, facecolor='#f0f0f0', bbox_inches='tight')
    plt.close()
    logging.info(f"Green boxplot saved to {output_path}")


# Z H E    B A S K E T U    S E S S I O N U 


def calculate_basket_average():
    # PLAN:
    # 1. Connect to the database and fetch everything from the customers table, and order by user_session. Exclude the "corrupted" session:
    # SELECT * 
    # FROM customers 
    # WHERE user_session != '00000000-0000-0000-0000-000000000000' 
    # ORDER BY user_session 
    # 2. For each user session, calculate the total price of items in that session at the end of the session. This means, add price of record if the event_type is "cart" and remove the price if the event_type is "remove_from_cart".
    # SELECT user_session, 
    #     MIN(event_time) as first_event,
    #     MAX(event_time) as last_event,
    #     COUNT(*) as event_count,
    #     SUM(CASE WHEN event_type != 'view' THEN price ELSE 0 END) as price_total,
    #     SUM(CASE WHEN event_type = 'remove_from_cart' THEN price ELSE 0 END) as price_subtract,
    #     SUM(CASE WHEN event_type != 'view' THEN price ELSE 0 END) - SUM(CASE WHEN event_type = 'remove_from_cart' THEN price ELSE 0 END) as basket_session
    # FROM customers 
    # WHERE user_session != '00000000-0000-0000-0000-000000000000' 
    # GROUP BY user_session
    # HAVING SUM(CASE WHEN event_type != 'view' THEN price ELSE 0 END) - SUM(CASE WHEN event_type = 'remove_from_cart' THEN price ELSE 0 END) != 0
    # ORDER BY MIN(event_time);
    # 
    # Plot using the resulting query above.

    # T O D O 
    pass    


def boxplot_avg_basket_per_user():
    """Generate horizontal blue boxplot for average basket per user - matches your third image with swapped axes"""
    logging.info("Generating boxplot for average basket per user (horizontal).")
    try:
        conn = setup_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, price FROM customers WHERE price IS NOT NULL;")
        user_baskets = defaultdict(list)
        for user_id, price in cur.fetchall():
            user_baskets[user_id].append(float(price))
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Database error: {e}")
        return

    if not user_baskets:
        logging.warning("No user baskets found.")
        print("No user baskets found.")
        return

    total_basket_per_user = [sum(prices) for prices in user_baskets.values() if prices]
    
    output_dir = ensure_output_dir()
    
    # Set style and create figure
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#f0f0f0')
    ax.set_facecolor('#f0f0f0')
    
    # Create horizontal boxplot with blue color and outliers
    sns.boxplot(x=total_basket_per_user,
                color='#7bb3d9',  # Light blue color
                linewidth=1,
                fliersize=4,  # Slightly larger outlier points
                ax=ax)
    
    # Customize appearance to match your third image, but horizontal
    ax.set_xlabel('price', fontsize=12)
    ax.set_ylabel('')
    ax.set_title('')
    ax.grid(True, alpha=0.3, color='gray')
    ax.set_yticks([])  # Remove y-axis ticks for cleaner look
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('black')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'boxplot_avg_basket_per_user.png')
    plt.savefig(output_path, dpi=150, facecolor='#f0f0f0', bbox_inches='tight')
    plt.close()
    logging.info(f"Boxplot for average basket per user saved to {output_path}")

if __name__ == "__main__":
    logging.info("Script started.")
    print_price_statistics()
    boxplot_item_prices()  # Horizontal white boxplot
    boxplot_item_prices_vertical_green()  # Vertical green boxplot (now saves as -2)
    boxplot_avg_basket_per_user()  # Vertical blue boxplot with outliers
    logging.info("Script finished.")