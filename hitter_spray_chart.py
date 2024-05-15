import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import io

# Function to get the player lookup table
def get_lookup_table():
    print('Gathering player lookup table. This may take a moment.')
    url = "https://raw.githubusercontent.com/chadwickbureau/register/master/data/people.csv"
    s = requests.get(url).content
    table = pd.read_csv(io.StringIO(s.decode('utf-8')), dtype={'key_sr_nfl': object, 'key_sr_nba': object, 'key_sr_nhl': object})
    # Subset columns
    cols_to_keep = ['name_last', 'name_first', 'key_mlbam', 'key_retro', 'key_bbref', 'key_fangraphs', 'mlb_played_first', 'mlb_played_last']
    table = table[cols_to_keep]
    # Make these lowercase to avoid capitalization mistakes when searching
    table['name_last'] = table['name_last'].str.lower()
    table['name_first'] = table['name_first'].str.lower()
    # Replace NaNs with -1, then convert columns to integers
    table[['key_mlbam', 'key_fangraphs']] = table[['key1_mlbam', 'key_fangraphs']].fillna(-1)
    table[['key_mlbam', 'key_fangraphs']] = table[['key_mlbam', 'key_fangraphs']].astype(int)  # originally returned as floats which is wrong
    return table

# Function to look up player ID by last and first name
def playerid_lookup(last, first=None):
    last = last.lower()
    if first:
        first = first.lower()
    table = get_lookup_table()
    if first is None:
        results = table.loc[table['name_last'] == last]
    else:
        results = table.loc[(table['name_last'] == last) & (table['name_first'] == first)]
    results = results.reset_index().drop('index', 1)
    return results

# Load your CSV data
df = pd.read_csv("/Users/leofeingold/Desktop/Outing Data Visualization/test.csv")

# Look up Aaron Judge's player ID
judge_data = playerid_lookup('judge', 'aaron')
if not judge_data.empty:
    judge_ID = judge_data['key_mlbam'].values[0]
    # Filter your DataFrame using the player ID
    aaron_judge_data = df[df['batter'] == judge_ID]
    print(aaron_judge_data.head())
else:
    print("Aaron Judge not found in the lookup table.")