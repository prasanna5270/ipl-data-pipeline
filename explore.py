import pandas as pd

for name in ["matches", "deliveries"]:
    df = pd.read_csv(f"data/raw/{name}.csv")
    print(f"\n===== {name.upper()} =====")
    print("Shape:", df.shape)
    print(df.head())
    print(df.dtypes)
    print("\nMissing values:\n", df.isnull().sum())
    print("Duplicates:", df.duplicated().sum())