# CODSOFT DATA ANALYTICS INTERNSHIP
# TASK 2: EXPLORATORY DATA ANALYSIS (EDA)
# Project: Retail Sales Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

# --------------------------------------------------
# 1. LOAD THE DATASET
# --------------------------------------------------

print("=" * 60)
print("RETAIL SALES - EXPLORATORY DATA ANALYSIS")
print("=" * 60)

file_path = Path(__file__).parent / "retail_sales_dataset.csv"

df = pd.read_csv(file_path)

print("\nDataset loaded successfully!")

# --------------------------------------------------
# 2. UNDERSTANDING THE DATASET
# --------------------------------------------------

print("\n1. FIRST FIVE RECORDS")
print(df.head())

print("\n2. LAST FIVE RECORDS")
print(df.tail())

print("\n3. DATASET SHAPE")
print("Rows and Columns:", df.shape)

print("\n4. COLUMN NAMES")
print(df.columns.tolist())

print("\n5. DATASET INFORMATION")
df.info()

print("\n6. DESCRIPTIVE STATISTICS")
print(df.describe(include="all"))

# --------------------------------------------------
# 3. DATA QUALITY CHECK
# --------------------------------------------------

print("\n7. MISSING VALUES")
print(df.isnull().sum())

print("\n8. DUPLICATE RECORDS")
print("Number of duplicates:", df.duplicated().sum())

# --------------------------------------------------
# 4. DATA PREPROCESSING FOR ANALYSIS
# --------------------------------------------------

df.columns = df.columns.str.strip()

# Convert date column if available
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove duplicate records
df = df.drop_duplicates()

# --------------------------------------------------
# 5. STATISTICAL ANALYSIS
# --------------------------------------------------

print("\n9. NUMERICAL COLUMN ANALYSIS")

numeric_columns = df.select_dtypes(include=np.number).columns

print(df[numeric_columns].describe())

print("\n10. CORRELATION MATRIX")
print(df[numeric_columns].corr())

# --------------------------------------------------
# 6. CATEGORY-WISE ANALYSIS
# --------------------------------------------------

print("\n11. PRODUCT CATEGORY ANALYSIS")

if "Product Category" in df.columns:
    if "Total Amount" in df.columns:
        category_sales = df.groupby("Product Category")["Total Amount"].sum()
        print("\nTotal sales by category:")
        print(category_sales)

        print("\nHighest selling category:")
        print(category_sales.idxmax())

        print("\nLowest selling category:")
        print(category_sales.idxmin())

    if "Quantity" in df.columns:
        print("\nQuantity sold by category:")
        print(df.groupby("Product Category")["Quantity"].sum())

# --------------------------------------------------
# 7. CUSTOMER ANALYSIS
# --------------------------------------------------

print("\n12. CUSTOMER ANALYSIS")

if "Gender" in df.columns and "Total Amount" in df.columns:
    print("\nSales by gender:")
    print(df.groupby("Gender")["Total Amount"].sum())

if "Age" in df.columns:
    print("\nAverage customer age:")
    print(df["Age"].mean())

    print("\nCustomer age statistics:")
    print(df["Age"].describe())

# --------------------------------------------------
# 8. OUTLIER DETECTION USING IQR
# --------------------------------------------------

print("\n13. OUTLIER DETECTION")

outlier_results = {}

for column in numeric_columns:
    values = df[column].dropna()

    if len(values) == 0:
        continue

    Q1 = values.quantile(0.25)
    Q3 = values.quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = values[
        (values < lower_limit) | (values > upper_limit)
    ]

    outlier_results[column] = len(outliers)

    print(f"\n{column}: {len(outliers)} outliers")
    print("Lower limit:", lower_limit)
    print("Upper limit:", upper_limit)

# --------------------------------------------------
# 9. MONTHLY SALES TREND
# --------------------------------------------------

print("\n14. MONTHLY SALES ANALYSIS")

if "Date" in df.columns and "Total Amount" in df.columns:

    monthly_sales = (
        df.dropna(subset=["Date"])
        .groupby(df.dropna(subset=["Date"])["Date"].dt.to_period("M"))["Total Amount"]
        .sum()
    )

    print(monthly_sales)

# --------------------------------------------------
# 10. VISUAL EXPLORATION
# --------------------------------------------------

sns.set_theme(style="whitegrid")

# Distribution of numerical columns
for column in numeric_columns:
    plt.figure(figsize=(8, 5))
    sns.histplot(df[column].dropna(), kde=True)
    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"eda_distribution_{column.replace(' ', '_')}.png")
    plt.close()

# Category-wise sales
if "Product Category" in df.columns and "Total Amount" in df.columns:

    plt.figure(figsize=(9, 5))

    sns.barplot(
        data=df,
        x="Product Category",
        y="Total Amount",
        estimator=sum,
        errorbar=None
    )

    plt.title("Total Sales by Product Category")
    plt.xlabel("Product Category")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("eda_category_sales.png")
    plt.close()

# Correlation heatmap
if len(numeric_columns) >= 2:

    plt.figure(figsize=(9, 6))

    sns.heatmap(
        df[numeric_columns].corr(),
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("eda_correlation_heatmap.png")
    plt.close()

# --------------------------------------------------
# 11. SAVE ANALYSIS REPORT
# --------------------------------------------------

report_path = Path(__file__).parent / "task2_report.txt"

with open(report_path, "w", encoding="utf-8") as report:

    report.write("RETAIL SALES - EXPLORATORY DATA ANALYSIS\n")
    report.write("=" * 50 + "\n\n")

    report.write(f"Total Records: {len(df)}\n")
    report.write(f"Total Columns: {len(df.columns)}\n\n")

    report.write("COLUMN INFORMATION:\n")
    report.write(str(df.dtypes) + "\n\n")

    report.write("DESCRIPTIVE STATISTICS:\n")
    report.write(df.describe(include="all").to_string() + "\n\n")

    report.write("MISSING VALUES:\n")
    report.write(df.isnull().sum().to_string() + "\n\n")

    report.write("DUPLICATE RECORDS REMOVED:\n")
    report.write(f"{df.duplicated().sum()}\n\n")

    report.write("OUTLIER COUNTS:\n")
    report.write(str(outlier_results) + "\n\n")

    if "Product Category" in df.columns and "Total Amount" in df.columns:
        report.write("SALES BY PRODUCT CATEGORY:\n")
        report.write(
            df.groupby("Product Category")["Total Amount"]
            .sum().to_string()
        )
        report.write("\n\n")

    if "Gender" in df.columns and "Total Amount" in df.columns:
        report.write("SALES BY GENDER:\n")
        report.write(
            df.groupby("Gender")["Total Amount"]
            .sum().to_string()
        )
        report.write("\n\n")

    report.write("CORRELATION MATRIX:\n")
    report.write(df[numeric_columns].corr().to_string())

print("\n" + "=" * 60)
print("EXPLORATORY DATA ANALYSIS COMPLETED SUCCESSFULLY!")
print("Analysis report saved as task2_report.txt")
print("Exploratory charts have been saved.")
print("=" * 60)