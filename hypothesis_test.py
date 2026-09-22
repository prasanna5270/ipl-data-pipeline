import sqlite3
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

conn = sqlite3.connect("data/ipl.db")

df = pd.read_sql("SELECT toss_match_winner_same FROM matches", conn)

successes = df["toss_match_winner_same"].sum()   # matches where toss winner = match winner
total = len(df)

# H0: toss winning does not affect match winning (true proportion = 0.5)
# H1: toss winning does affect match winning (proportion != 0.5)
stat, p_value = proportions_ztest(count=successes, nobs=total, value=0.5)

print(f"Toss winner also won match: {successes} out of {total} ({successes/total:.2%})")
print(f"Z-statistic: {stat:.4f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("Result: Statistically significant — toss winning DOES affect match outcome.")
else:
    print("Result: NOT statistically significant — toss winning has no real effect on match outcome.")