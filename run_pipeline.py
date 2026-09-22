import logging
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()],
)

DB_URL = "sqlite:///data/ipl.db"


def extract():
    matches = pd.read_csv("data/raw/matches.csv")
    deliveries = pd.read_csv("data/raw/deliveries.csv")
    logging.info("Extracted matches: %d rows, deliveries: %d rows", len(matches), len(deliveries))
    return matches, deliveries


def transform_matches(df):
    # Fix date type
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
        # Standardize renamed teams
    name_fixes = {
        "Delhi Daredevils": "Delhi Capitals",
        "Kings XI Punjab": "Punjab Kings",
        "Deccan Chargers": "Sunrisers Hyderabad",
        "Rising Pune Supergiant": "Rising Pune Supergiants",
        "Royal Challengers Bengaluru": "Royal Challengers Bangalore",
    }
    for col in ["team1", "team2", "toss_winner", "winner"]:
        df[col] = df[col].replace(name_fixes)
    # Fill missing categorical values instead of dropping rows
    df["city"] = df["city"].fillna("Unknown")
    df["method"] = df["method"].fillna("Normal")

    # Drop rows with no result at all (abandoned matches) - only 5 rows
    df = df.dropna(subset=["winner"])

    # New column: did the toss winner also win the match?
    df["toss_match_winner_same"] = df["toss_winner"] == df["winner"]

    # New column: season as a clean year label
    df["season"] = df["season"].astype(str).str.slice(0, 4)

    logging.info("Transformed matches: %d clean rows", len(df))
    return df


def transform_deliveries(df):
    # New column: was this ball a boundary (4 or 6)?
    df["is_boundary"] = df["batsman_runs"].isin([4, 6])
    name_fixes = {
        "Delhi Daredevils": "Delhi Capitals",
        "Kings XI Punjab": "Punjab Kings",
        "Deccan Chargers": "Sunrisers Hyderabad",
        "Rising Pune Supergiant": "Rising Pune Supergiants",
        "Royal Challengers Bengaluru": "Royal Challengers Bangalore",
    }
    for col in ["batting_team", "bowling_team"]:
        df[col] = df[col].replace(name_fixes)
    # New column: match phase based on over number
    def phase(over):
        if over < 6:
            return "Powerplay"
        elif over < 16:
            return "Middle"
        else:
            return "Death"
    df["phase"] = df["over"].apply(phase)

    logging.info("Transformed deliveries: %d rows", len(df))
    return df


def load(matches, deliveries):
    matches.to_csv("data/processed/matches_clean.csv", index=False)
    deliveries.to_csv("data/processed/deliveries_clean.csv", index=False)

    engine = create_engine(DB_URL)
    matches.to_sql("matches", engine, if_exists="replace", index=False)
    deliveries.to_sql("deliveries", engine, if_exists="replace", index=False)
    logging.info("Loaded both tables into SQLite and CSV")


def run():
    try:
        logging.info("Pipeline started")
        matches, deliveries = extract()
        matches = transform_matches(matches)
        deliveries = transform_deliveries(deliveries)
        load(matches, deliveries)
        logging.info("Pipeline finished successfully")
    except Exception as e:
        logging.error("Pipeline failed: %s", e)
        raise


if __name__ == "__main__":
    run()