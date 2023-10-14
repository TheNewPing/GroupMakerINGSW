from itertools import combinations
import argparse
import pandas as pd

def total_points(team_member, team, df):
    all_offers = df.loc[team_member]        
    group_offers = all_offers[[t for t in team if t != team_member]]
    return group_offers.sum()

# argument parsing
parser = argparse.ArgumentParser(description="Read a CSV file.")
parser.add_argument('filepath', type=str, help="The path to the CSV file.")
args = parser.parse_args()

# read csv table
df = pd.read_csv(args.filepath, index_col=0)

# get team options and size
candidates = list(df.columns)
team_size = len(candidates) // 2
all_teams = [list(c) for c in combinations(candidates, team_size)]

# find the best teams
best_score = 0
for team in all_teams:
    # calculate the other team members and size
    other_team = [c for c in candidates if c not in team]
    other_team_size = len(other_team)

    # calculate average point for the 2 teams
    avg_points_team = sum([total_points(team_member, team, df) for team_member in team]) / team_size
    avg_points_other_team = sum([total_points(other_team_member, other_team, df) for other_team_member in other_team]) / other_team_size
    score = (avg_points_team + avg_points_other_team) / 2

    if score > best_score:
        best_score = score
        best_team = team.copy()

other_best_team = [c for c in candidates if c not in best_team]
print(f"team 1: {best_team}")
print(f"team 2: {other_best_team}")
    