# CODSOFT DATA ANALYTICS INTERNSHIP
# TASK 3: DATA VISUALIZATION DASHBOARD
# Project: Retail Sales Analysis

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --------------------------------------------------
# 1. SET UP PROJECT PATHS
# --------------------------------------------------

base_path = Path(__file__).parent
file_path = base_path / "retail_sales_dataset.csv"

charts_folder = base_path / "charts"
charts_folder.mkdir(exist_ok=True)

# --------------------------------------------------
# 2. LOAD THE DATASET
# --------------------------------------------------

print("=" * 60)
print("RETAIL SALES - DATA VISUALIZATION DASHBOARD")
print("=" * 60)

df = pd.read_csv(file_path)

print("\nDataset loaded successfully!")
print("\nDataset shape:", df.shape)
print("\nAvailable columns:")
print(df.columns.tolist())

# --------------------------------------------------
# 3. CHECK REQUIRED COLUMNS
# --------------------------------------------------

required_columns = [
    "Date",
    "Product Category",
    "Total Amount",
    "Quantity"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns not found: {missing_columns}. "
        f"Available columns: {df.columns.tolist()}"
    )

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove records with missing values needed for charts
df = df.dropna(
    subset=["Date", "Product Category", "Total Amount", "Quantity"]
)

sns.set_theme(style="whitegrid", palette="deep")

# --------------------------------------------------
# 4. PREPARE DATA FOR VISUALIZATION
# --------------------------------------------------

category_sales = (
    df.groupby("Product Category")["Total Amount"]
    .sum()
    .sort_values(ascending=False)
)

monthly_sales = (
    df.groupby(df["Date"].dt.to_period("M"))["Total Amount"]
    .sum()
)

category_quantity = (
    df.groupby("Product Category")["Quantity"]
    .sum()
)

# --------------------------------------------------
# 5. BAR CHART
# --------------------------------------------------

plt.figure(figsize=(9, 5))

sns.barplot(
    x=category_sales.index,
    y=category_sales.values
)

plt.title("Total Sales by Product Category",
          fontsize=15, fontweight="bold")
plt.xlabel("Product Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=25)
plt.tight_layout()

plt.savefig(charts_folder / "bar_chart.png", dpi=300)
plt.close()

print("\nBar chart created successfully!")

# --------------------------------------------------
# 6. LINE CHART
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker="o",
    linewidth=2
)

plt.title("Monthly Retail Sales Trend",
          fontsize=15, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(charts_folder / "line_chart.png", dpi=300)
plt.close()

print("Line chart created successfully!")

# --------------------------------------------------
# 7. PIE CHART
# --------------------------------------------------

plt.figure(figsize=(8, 6))

plt.pie(
    category_sales.values,
    labels=category_sales.index,
    autopct="%1.1f%%",
    startangle=90,
    shadow=False
)

plt.title("Sales Distribution by Product Category",
          fontsize=15, fontweight="bold")

plt.tight_layout()
plt.savefig(charts_folder / "pie_chart.png", dpi=300)
plt.close()

print("Pie chart created successfully!")

# --------------------------------------------------
# 8. HISTOGRAM
# --------------------------------------------------

plt.figure(figsize=(9, 5))

sns.histplot(
    data=df,
    x="Total Amount",
    bins=20,
    kde=True
)

plt.title("Distribution of Retail Transaction Amounts",
          fontsize=15, fontweight="bold")
plt.xlabel("Transaction Amount")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig(charts_folder / "histogram.png", dpi=300)
plt.close()

print("Histogram created successfully!")

# --------------------------------------------------
# 9. SCATTER PLOT
# --------------------------------------------------

plt.figure(figsize=(9, 5))

sns.scatterplot(
    data=df,
    x="Quantity",
    y="Total Amount",
    hue="Product Category",
    s=80
)

plt.title("Relationship Between Quantity and Sales",
          fontsize=15, fontweight="bold")
plt.xlabel("Quantity Purchased")
plt.ylabel("Total Amount")
plt.legend(title="Product Category")
plt.tight_layout()

plt.savefig(charts_folder / "scatter_plot.png", dpi=300)
plt.close()

print("Scatter plot created successfully!")

# --------------------------------------------------
# 10. CREATE COMBINED DASHBOARD
# --------------------------------------------------

fig, axes = plt.subplots(2, 3, figsize=(18, 11))

fig.suptitle(
    "RETAIL SALES ANALYSIS DASHBOARD",
    fontsize=20,
    fontweight="bold"
)

# Bar chart
sns.barplot(
    x=category_sales.index,
    y=category_sales.values,
    ax=axes[0, 0]
)
axes[0, 0].set_title("Sales by Category")
axes[0, 0].set_xlabel("Category")
axes[0, 0].set_ylabel("Total Sales")
axes[0, 0].tick_params(axis="x", rotation=25)

# Line chart
axes[0, 1].plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker="o"
)
axes[0, 1].set_title("Monthly Sales Trend")
axes[0, 1].set_xlabel("Month")
axes[0, 1].set_ylabel("Total Sales")
axes[0, 1].tick_params(axis="x", rotation=45)

# Pie chart
axes[0, 2].pie(
    category_sales.values,
    labels=category_sales.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[0, 2].set_title("Category Sales Distribution")

# Histogram
sns.histplot(
    data=df,
    x="Total Amount",
    bins=20,
    kde=True,
    ax=axes[1, 0]
)
axes[1, 0].set_title("Transaction Amount Distribution")

# Scatter plot
sns.scatterplot(
    data=df,
    x="Quantity",
    y="Total Amount",
    hue="Product Category",
    ax=axes[1, 1]
)
axes[1, 1].set_title("Quantity vs Total Amount")
axes[1, 1].legend(title="Category")

# Summary panel
axes[1, 2].axis("off")

summary = (
    f"TOTAL TRANSACTIONS\n{len(df):,}\n\n"
    f"TOTAL SALES\n{df['Total Amount'].sum():,.2f}\n\n"
    f"TOTAL QUANTITY SOLD\n{df['Quantity'].sum():,}\n\n"
    f"PRODUCT CATEGORIES\n{df['Product Category'].nunique()}"
)

axes[1, 2].text(
    0.5, 0.5,
    summary,
    ha="center",
    va="center",
    fontsize=14,
    bbox=dict(boxstyle="round,pad=1", alpha=0.15)
)

plt.tight_layout(rect=[0, 0, 1, 0.95])

plt.savefig(
    charts_folder / "sales_dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# 11. COMPLETION MESSAGE
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA VISUALIZATION COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nAll five individual charts have been saved.")
print("Combined dashboard has been saved.")
print("\nCharts folder:", charts_folder)

print("\nGenerated files:")
for chart in charts_folder.iterdir():
    if chart.is_file():
        print("-", chart.name)

print("\nTASK 3 COMPLETED SUCCESSFULLY!")# CODSOFT DATA ANALYTICS INTERNSHIP
# TASK 3: DATA VISUALIZATION DASHBOARD
# Project: Retail Sales Analysis

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --------------------------------------------------
# 1. SET UP PROJECT PATHS
# --------------------------------------------------

base_path = Path(__file__).parent
file_path = base_path / "retail_sales_dataset.csv"

charts_folder = base_path / "charts"
charts_folder.mkdir(exist_ok=True)

# --------------------------------------------------
# 2. LOAD THE DATASET
# --------------------------------------------------

print("=" * 60)
print("RETAIL SALES - DATA VISUALIZATION DASHBOARD")
print("=" * 60)

df = pd.read_csv(file_path)

print("\nDataset loaded successfully!")
print("\nDataset shape:", df.shape)
print("\nAvailable columns:")
print(df.columns.tolist())

# --------------------------------------------------
# 3. CHECK REQUIRED COLUMNS
# --------------------------------------------------

required_columns = [
    "Date",
    "Product Category",
    "Total Amount",
    "Quantity"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns not found: {missing_columns}. "
        f"Available columns: {df.columns.tolist()}"
    )

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove records with missing values needed for charts
df = df.dropna(
    subset=["Date", "Product Category", "Total Amount", "Quantity"]
)

sns.set_theme(style="whitegrid", palette="deep")

# --------------------------------------------------
# 4. PREPARE DATA FOR VISUALIZATION
# --------------------------------------------------

category_sales = (
    df.groupby("Product Category")["Total Amount"]
    .sum()
    .sort_values(ascending=False)
)

monthly_sales = (
    df.groupby(df["Date"].dt.to_period("M"))["Total Amount"]
    .sum()
)

category_quantity = (
    df.groupby("Product Category")["Quantity"]
    .sum()
)

# --------------------------------------------------
# 5. BAR CHART
# --------------------------------------------------

plt.figure(figsize=(9, 5))

sns.barplot(
    x=category_sales.index,
    y=category_sales.values
)

plt.title("Total Sales by Product Category",
          fontsize=15, fontweight="bold")
plt.xlabel("Product Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=25)
plt.tight_layout()

plt.savefig(charts_folder / "bar_chart.png", dpi=300)
plt.close()

print("\nBar chart created successfully!")

# --------------------------------------------------
# 6. LINE CHART
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker="o",
    linewidth=2
)

plt.title("Monthly Retail Sales Trend",
          fontsize=15, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(charts_folder / "line_chart.png", dpi=300)
plt.close()

print("Line chart created successfully!")

# --------------------------------------------------
# 7. PIE CHART
# --------------------------------------------------

plt.figure(figsize=(8, 6))

plt.pie(
    category_sales.values,
    labels=category_sales.index,
    autopct="%1.1f%%",
    startangle=90,
    shadow=False
)

plt.title("Sales Distribution by Product Category",
          fontsize=15, fontweight="bold")

plt.tight_layout()
plt.savefig(charts_folder / "pie_chart.png", dpi=300)
plt.close()

print("Pie chart created successfully!")

# --------------------------------------------------
# 8. HISTOGRAM
# --------------------------------------------------

plt.figure(figsize=(9, 5))

sns.histplot(
    data=df,
    x="Total Amount",
    bins=20,
    kde=True
)

plt.title("Distribution of Retail Transaction Amounts",
          fontsize=15, fontweight="bold")
plt.xlabel("Transaction Amount")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig(charts_folder / "histogram.png", dpi=300)
plt.close()

print("Histogram created successfully!")

# --------------------------------------------------
# 9. SCATTER PLOT
# --------------------------------------------------

plt.figure(figsize=(9, 5))

sns.scatterplot(
    data=df,
    x="Quantity",
    y="Total Amount",
    hue="Product Category",
    s=80
)

plt.title("Relationship Between Quantity and Sales",
          fontsize=15, fontweight="bold")
plt.xlabel("Quantity Purchased")
plt.ylabel("Total Amount")
plt.legend(title="Product Category")
plt.tight_layout()

plt.savefig(charts_folder / "scatter_plot.png", dpi=300)
plt.close()

print("Scatter plot created successfully!")

# --------------------------------------------------
# 10. CREATE COMBINED DASHBOARD
# --------------------------------------------------

fig, axes = plt.subplots(2, 3, figsize=(18, 11))

fig.suptitle(
    "RETAIL SALES ANALYSIS DASHBOARD",
    fontsize=20,
    fontweight="bold"
)

# Bar chart
sns.barplot(
    x=category_sales.index,
    y=category_sales.values,
    ax=axes[0, 0]
)
axes[0, 0].set_title("Sales by Category")
axes[0, 0].set_xlabel("Category")
axes[0, 0].set_ylabel("Total Sales")
axes[0, 0].tick_params(axis="x", rotation=25)

# Line chart
axes[0, 1].plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker="o"
)
axes[0, 1].set_title("Monthly Sales Trend")
axes[0, 1].set_xlabel("Month")
axes[0, 1].set_ylabel("Total Sales")
axes[0, 1].tick_params(axis="x", rotation=45)

# Pie chart
axes[0, 2].pie(
    category_sales.values,
    labels=category_sales.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[0, 2].set_title("Category Sales Distribution")

# Histogram
sns.histplot(
    data=df,
    x="Total Amount",
    bins=20,
    kde=True,
    ax=axes[1, 0]
)
axes[1, 0].set_title("Transaction Amount Distribution")

# Scatter plot
sns.scatterplot(
    data=df,
    x="Quantity",
    y="Total Amount",
    hue="Product Category",
    ax=axes[1, 1]
)
axes[1, 1].set_title("Quantity vs Total Amount")
axes[1, 1].legend(title="Category")

# Summary panel
axes[1, 2].axis("off")

summary = (
    f"TOTAL TRANSACTIONS\n{len(df):,}\n\n"
    f"TOTAL SALES\n{df['Total Amount'].sum():,.2f}\n\n"
    f"TOTAL QUANTITY SOLD\n{df['Quantity'].sum():,}\n\n"
    f"PRODUCT CATEGORIES\n{df['Product Category'].nunique()}"
)

axes[1, 2].text(
    0.5, 0.5,
    summary,
    ha="center",
    va="center",
    fontsize=14,
    bbox=dict(boxstyle="round,pad=1", alpha=0.15)
)

plt.tight_layout(rect=[0, 0, 1, 0.95])

plt.savefig(
    charts_folder / "sales_dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# 11. COMPLETION MESSAGE
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA VISUALIZATION COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nAll five individual charts have been saved.")
print("Combined dashboard has been saved.")
print("\nCharts folder:", charts_folder)

print("\nGenerated files:")
for chart in charts_folder.iterdir():
    if chart.is_file():
        print("-", chart.name)

print("\nTASK 3 COMPLETED SUCCESSFULLY!")