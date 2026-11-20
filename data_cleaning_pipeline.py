import pandas as pd
from pathlib import Path

def load(path):
    df = pd.read_csv("messy_sales.csv")
    print("==BEFORE CLEANING==")
    print("Shape:", df.shape)
    print("Missing values:")
    print(df.isnull().sum())
    print("Data types:")
    print(df.dtypes)

    return df

def clean_county(df):
    # Step 1: lowercase everything to remove case differences
    df["county"] = df["county"].str.lower().str.strip()

    # Step 2: fix known abbreviations
    county_fixes = {
        "nrb": "nairobi",
        "nkr": "nakuru",
        "msa": "mombasa",
        "ksm": "kisumu",
        "eldoret": "uasin gishu"
    }
    df["county"] = df["county"].replace(county_fixes)

    # Step 3: proper case for display
    df["county"] = df["county"].str.title()
    return df


def clean_customer(df):
    df["customer"] = df["customer"].str.strip()
    return df

  
def clean_amount(df):
      # Keep only digits and decimal point, then convert to float
    df["amount_kes"] = (
        df["amount"]
        .str.replace(r"[^\d.]", "", regex=True)
        .replace("", None)
        .astype(float)  # float handles NaN; int does not
    )
    df = df.drop(columns=["amount"])
    return df

def handle_missing_data(df):
    df["county"] = df["county"].fillna("Unknown")
    df["customer"] = df["customer"].fillna("Walk-in Customer")
    df = df.dropna(subset=["amount_kes"])
    return df

def remove_duplicates(df):
    df = df.drop_duplicates()  # or subset=[..., "date"/"invoice_id"]
    return df

def run_pipeline(path_in, path_out):
    df = load(path_in)
    rows_start = len(df)
    df = clean_county(df)
    df = clean_customer(df)
    df = clean_amount(df)
    df = handle_missing_data(df)
    df = remove_duplicates(df)
    print()
    print("==AFTER CLEANING==")
    print("Shape:", df.shape)
    print("Missing values:")
    print(df.isnull().sum())
    print("Data types:")
    print(df.dtypes)
    df.to_csv(path_out, index=False)
    print(f"{rows_start} rows in, {len(df)} rows out")

if __name__ == "__main__":
    run_pipeline("messy_sales.csv", "clean_sales.csv")