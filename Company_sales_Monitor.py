import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set visual style
sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"


#BUSINESS DATA SECTION.


# 1. CREATING MOCK BUSINESS DATA
np.random.seed(42)
n_rows = 1000

dates = pd.date_range(start="2024-01-01", end="2024-12-31", periods=n_rows)
regions = np.random.choice(
    ["North America", "Europe", "Asia-Pacific", "Latin America"], size=n_rows
)
categories = ["Electronics", "Furniture", "Office Supplies", "Apparel"]
products_map = {
    "Electronics": ["Laptops", "Smartphones", "Headphones"],
    "Furniture": ["Office Chairs", "Desks", "Bookshelves"],
    "Office Supplies": ["Paper", "Pens", "Binders"],
    "Apparel": ["Jackets", "Sneakers", "Shirts"],
}

cat_list = np.random.choice(categories, size=n_rows, p=[0.35, 0.25, 0.20, 0.20])
prod_list = [np.random.choice(products_map[c]) for c in cat_list]
units = np.random.randint(1, 15, size=n_rows)
unit_price = np.random.uniform(10, 500, size=n_rows)

df = pd.DataFrame(
    {
        "Date": dates,
        "Region": regions,
        "Category": cat_list,
        "Product": prod_list,
        "Units_Sold": units,
        "Unit_Price": unit_price,
    }
)


#            KIP CALCULATION





# Introduce KPI Calculations
df["Revenue"] = df["Units_Sold"] * df["Unit_Price"]
df["Month"] = df["Date"].dt.to_period("M")

# 2. KEY METRICS SUMMARY
total_revenue = df["Revenue"].sum()
total_units = df["Units_Sold"].sum()
avg_order_val = df["Revenue"].mean()

print(f"--- EXECUTIVE SUMMARY METRICS ---")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Units Sold: {total_units:,}")
print(f"Average Order Value: ${avg_order_val:,.2f}\n")

# 3. VISUALIZATION GENERATION
fig, axes = plt.subplots(2, 2, figsize=(16, 10))



# REVENUE SECTION


#  1: Revenue Trends Over Time
monthly_rev = df.groupby(df["Date"].dt.to_period("M"))["Revenue"].sum()
monthly_rev.plot(kind="line", marker="o", color="#2b5c8f", ax=axes[0, 0])
axes[0, 0].set_title("1. Monthly Revenue Trend (2024)", fontsize=12, fontweight="bold")
axes[0, 0].set_ylabel("Revenue ($)")
axes[0, 0].set_xlabel("Month")

#  2: High-Value Categories
cat_rev = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
sns.barplot(
    x=cat_rev.values, y=cat_rev.index, ax=axes[0, 1], palette="Blues_r"
)
axes[0, 1].set_title(
    "2. Revenue by Category (High-Value)", fontsize=12, fontweight="bold"
)
axes[0, 1].set_xlabel("Revenue ($)")

#  3: Top-Selling Products
top_prod = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
sns.barplot(
    x=top_prod.values, y=top_prod.index, ax=axes[1, 0], palette="Greens_r"
)
axes[1, 0].set_title(
    "3. Top 5 Products by Revenue", fontsize=12, fontweight="bold"
)
axes[1, 0].set_xlabel("Revenue ($)")



#       REGIONAL PERFORMANCE 



# 4: Regional Performance
reg_rev = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
sns.barplot(
    x=reg_rev.index, y=reg_rev.values, ax=axes[1, 1], palette="Oranges_r"
)
axes[1, 1].set_title(
    "4. Regional Sales Performance", fontsize=12, fontweight="bold"
)
axes[1, 1].set_ylabel("Revenue ($)")

plt.tight_layout()
plt.show()