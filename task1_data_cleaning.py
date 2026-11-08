import pandas as pd

# 1. Load the dataset
df = pd.read_csv("codsoft_task1_messy_dataset.csv")

# 2. Inspect the dataset
print("\nORIGINAL DATASET")
print(df)

print("\nDATASET INFORMATION")
df.info()

print("\nDATASET DESCRIPTION")
print(df.describe(include="all"))

# 3. Identify missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# 4. Identify duplicate records
print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

# 5. Handle missing values
df["Age"] = df["Age"].fillna(df["Age"].median())

df["PurchaseAmount"] = df["PurchaseAmount"].fillna(
    df["PurchaseAmount"].median()
)

# 6. Remove duplicate records
df = df.drop_duplicates()

# 7. Correct inconsistent entries
df["Gender"] = df["Gender"].replace({
    "F": "Female",
    "f": "Female",
    "M": "Male"
})

df["City"] = df["City"].replace({
    "BANGALORE": "Bengaluru",
    "Bangalore": "Bengaluru",
    "Mysore": "Mysuru",
    "Belgaum": "Belagavi"
})

# 8. Correct data types
df["Age"] = df["Age"].astype(int)

df["JoinDate"] = pd.to_datetime(
    df["JoinDate"], dayfirst=True, format="mixed"
)

# 9. Display cleaned dataset
print("\nCLEANED DATASET")
print(df)

print("\nMISSING VALUES AFTER CLEANING")
print(df.isnull().sum())

print("\nDUPLICATES AFTER CLEANING")
print(df.duplicated().sum())

# 10. Save cleaned dataset
df.to_csv("cleaned_dataset.csv", index=False)

print("\nCleaned dataset saved successfully!")