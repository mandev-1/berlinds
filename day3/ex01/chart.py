import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CONNECT_TO_DB import setup_connection
import matplotlib.pyplot as plt
from collections import defaultdict
import logging
from datetime import datetime

# Set global matplotlib style to match target aesthetic
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'axes.titlesize': 0,
    'figure.figsize': (8, 5),
    'axes.grid': True,  # Enable grid
    'axes.facecolor': '#f5f5f8',  # Light purple-gray background
    'figure.facecolor': 'white',
    'axes.edgecolor': '#e0e0e0',  # Light gray edges
    'axes.linewidth': 0.5,
    'font.family': 'sans-serif',
    'grid.color': '#ffffff',      # White grid lines
    'grid.linewidth': 1,
    'grid.alpha': 0.8
})

def ensure_output_dir():
    output_dir = os.path.join(os.path.dirname(__file__), '../generated')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def visualize_customer_flow():
    output_dir = ensure_output_dir()
    conn = setup_connection()
    cur = conn.cursor()
    cur.execute("SELECT event_time, user_id FROM customers WHERE event_time IS NOT NULL;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    day_users = defaultdict(set)
    for event_time, user_id in rows:
        day = event_time.date()
        day_users[day].add(user_id)
    days = sorted(day_users.keys())
    counts = [len(day_users[day]) for day in days]
    fig, ax = plt.subplots()
    ax.fill_between(days, counts, alpha=0.6, color='#9db4d1', linewidth=1, edgecolor='#7a9cc6')
    ax.set_xlabel('month', color='#666666')
    ax.set_ylabel('number of customers', color='#666666')
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e0e0e0')
    ax.spines['bottom'].set_color('#e0e0e0')
    ax.tick_params(colors='#666666', length=0)
    ax.grid(True, which='major', axis='both', color='white', linewidth=1, alpha=0.8)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'customer_flow.png'), dpi=150, bbox_inches='tight')
    plt.close()

def visualize_sales_monthly():
    output_dir = ensure_output_dir()
    conn = setup_connection()
    cur = conn.cursor()
    cur.execute("SELECT event_time, price FROM customers WHERE event_time IS NOT NULL;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    month_sales = defaultdict(float)
    for event_time, price in rows:
        month = event_time.strftime('%b')
        month_sales[month] += float(price)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    months = [m for m in month_order if m in month_sales]
    sales = [month_sales[m] for m in months]
    fig, ax = plt.subplots()
    bars = ax.bar(months, sales, color='#a8bdd1', alpha=0.8, edgecolor='#8fa8c0', linewidth=0.5)
    ax.set_xlabel('month', color='#666666')
    ax.set_ylabel('total sales in million of £', color='#666666')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e0e0e0')
    ax.spines['bottom'].set_color('#e0e0e0')
    ax.tick_params(colors='#666666', length=0)
    ax.grid(True, which='major', axis='both', color='white', linewidth=1, alpha=0.8)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sales_monthly.png'), dpi=150, bbox_inches='tight')
    plt.close()

def visualize_average_spend_customer_monthly():
    output_dir = ensure_output_dir()
    conn = setup_connection()
    cur = conn.cursor()
    cur.execute("SELECT event_time, price, user_id FROM customers WHERE event_time IS NOT NULL;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    day_price = defaultdict(float)
    day_users = defaultdict(set)
    for event_time, price, user_id in rows:
        day = event_time.date()
        day_price[day] += float(price)
        day_users[day].add(user_id)
    days = sorted(day_price.keys())
    avg_spend = [day_price[day] / len(day_users[day]) if day_users[day] else 0 for day in days]
    fig, ax = plt.subplots()
    ax.fill_between(days, avg_spend, alpha=0.6, color='#9db4d1', linewidth=1, edgecolor='#7a9cc6')
    ax.set_xlabel('month', color='#666666')
    ax.set_ylabel('average spend/customers in £', color='#666666')
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e0e0e0')
    ax.spines['bottom'].set_color('#e0e0e0')
    ax.tick_params(colors='#666666', length=0)
    ax.grid(True, which='major', axis='both', color='white', linewidth=1, alpha=0.8)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'avg_spend_monthly.png'), dpi=150, bbox_inches='tight')
    plt.close()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_and_run(func, description):
    logging.info(f"Started generating {description}...")
    start_time = datetime.now()
    func()
    end_time = datetime.now()
    logging.info(f"Finished generating {description} in {(end_time - start_time).total_seconds():.2f} seconds.")

if __name__ == "__main__":
    print("Generating charts...\n\n\nNote: This may take a few minutes, please be patient.")
    log_and_run(visualize_customer_flow, "customer flow chart")
    log_and_run(visualize_sales_monthly, "monthly sales chart")
    log_and_run(visualize_average_spend_customer_monthly, "average spend per customer chart")