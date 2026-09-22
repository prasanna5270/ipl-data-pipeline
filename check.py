import sqlite3
import pandas as pd

conn = sqlite3.connect("data/ipl.db")

# Q1: Which teams have won the most matches?
q1 = """
SELECT winner, COUNT(*) AS wins
FROM matches
GROUP BY winner
ORDER BY wins DESC
LIMIT 10
"""
print("Top 10 winning teams:\n", pd.read_sql(q1, conn), "\n")

# Q2: Does winning the toss help win the match?
q2 = """
SELECT toss_match_winner_same, COUNT(*) AS matches
FROM matches
GROUP BY toss_match_winner_same
"""
print("Toss winner = Match winner?\n", pd.read_sql(q2, conn), "\n")

# Q3: Runs scored per phase (Powerplay/Middle/Death)
q3 = """
SELECT phase, SUM(total_runs) AS total_runs, COUNT(*) AS balls
FROM deliveries
GROUP BY phase
"""
print("Runs by phase:\n", pd.read_sql(q3, conn))
# Q4: Bat first vs chase - which wins more?
q4 = """
SELECT
  CASE WHEN toss_decision = 'bat' THEN 'Batted First' ELSE 'Chased' END AS toss_choice,
  COUNT(*) AS times_chosen,
  SUM(CASE WHEN toss_match_winner_same = 1 THEN 1 ELSE 0 END) AS also_won
FROM matches
GROUP BY toss_decision
"""
print("Bat vs Chase after toss:\n", pd.read_sql(q4, conn), "\n")

# Q5: Top run scorers
q5 = """
SELECT batter, SUM(batsman_runs) AS total_runs
FROM deliveries
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10
"""
print("Top 10 run scorers:\n", pd.read_sql(q5, conn), "\n")

# Q6: Top wicket takers
q6 = """
SELECT bowler, COUNT(*) AS wickets
FROM deliveries
WHERE is_wicket = 1 AND dismissal_kind NOT IN ('run out', 'retired hurt', 'obstructing the field')
GROUP BY bowler
ORDER BY wickets DESC
LIMIT 10
"""
print("Top 10 wicket takers:\n", pd.read_sql(q6, conn), "\n")

# Q7: Most sixes by team
q7 = """
SELECT batting_team, COUNT(*) AS sixes
FROM deliveries
WHERE batsman_runs = 6
GROUP BY batting_team
ORDER BY sixes DESC
LIMIT 10
"""
print("Most sixes by team:\n", pd.read_sql(q7, conn))