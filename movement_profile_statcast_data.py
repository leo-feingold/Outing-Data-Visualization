import pandas as pd
import numpy as np
import datetime
from baseball_scraper import statcast
from baseball_scraper import playerid_lookup # Might be worthwhile to use ID's instead of names to filter by pitcher...
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# fix time delta, currently set for 2 days ago!
playerName = 'Ragans, Cole'
pitcherPerspectiveMode = False

def scrape_data():
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    prev_day = today - datetime.timedelta(days=2)
    prev_day = prev_day.strftime('%Y-%m-%d')
    data = statcast(start_dt = prev_day, end_dt = today_str)
    return data

def clean_data(df):
    df = scrape_data()
    df = df[['pitcher', 'player_name', 'pitch_type', 'release_speed', 'pfx_x', 'pfx_z', 'release_spin_rate', 'spin_axis', 'release_extension', 'pitch_name', 'description', 'events', 'bb_type', 'type', 'estimated_woba_using_speedangle', 'p_throws']]
    
    # Pitcher Perspective Visualization Mode
    if pitcherPerspectiveMode:
        df['pfx_x'] = df['pfx_x'] * -12
    # + is Arm Side, - is Glove Side, for data processing mode
    else:
        df['pfx_x'] = np.where(df['p_throws'] == 'R', df['pfx_x'] * -12, df['pfx_x'] * 12)
    
    df['pfx_z'] = df['pfx_z'] * 12
    return df

def plot_data(df):
    myStr = ""
    if pitcherPerspectiveMode:
        myStr = "Pitcher's Perspective"
    else:
        myStr = "Arm Side +, Glove Side -"

    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    prev_day = today - datetime.timedelta(days=2)
    prev_day = prev_day.strftime('%Y-%m-%d')

    df = clean_data(scrape_data())
    pitcher_data = df[df['player_name'] == playerName]
    pitcher_data = pitcher_data.dropna(subset=['pfx_x', 'pfx_z', 'release_speed', 'release_spin_rate', 'spin_axis', 'release_extension', 'pitch_type', 'description', 'estimated_woba_using_speedangle'])

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='pfx_x', y='pfx_z', data=pitcher_data, hue='pitch_type', style='pitch_type', s=100, palette='deep')
    plt.title(f"Pitch Movement Profile for {playerName}, Date: {prev_day} ({myStr})")
    plt.xlabel('Horizontal Movement (pfx_x)')
    plt.ylabel('Vertical Movement (pfx_z)')
    plt.legend(title='Pitch Type')
    plt.grid(True)
    plt.show()

def plot_data_interactive(df):
    myStr = ""
    if pitcherPerspectiveMode:
        myStr = "Pitcher's Perspective"
    else:
        myStr = "Arm Side +, Glove Side -"
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')
    prev_day = today - datetime.timedelta(days=2)
    prev_day = prev_day.strftime('%Y-%m-%d')

    df = clean_data(df)
    pitcher_data = df[df['player_name'] == playerName]
    pitcher_data = pitcher_data.dropna(subset=['pfx_x', 'pfx_z', 'release_speed', 'release_spin_rate', 'spin_axis'])
    bip_condition = pitcher_data['description'] == 'hit_into_play'
    pitcher_data.loc[bip_condition, 'description'] += " || xwOBA: " + pitcher_data.loc[bip_condition,'estimated_woba_using_speedangle'].astype(str)

    fig = px.scatter(pitcher_data, x='pfx_x', y='pfx_z', color='pitch_name',
                     hover_data=['release_speed', 'release_spin_rate', 'spin_axis', 'release_extension', 'description'],
                     labels={
                         'pfx_x': 'Horizontal Movement (inches)',
                         'pfx_z': 'Vertical Movement (inches)',
                         'pitch_name': 'Pitch Type'
                     },
                     title=f"Pitch Movement Profile for {playerName} ({pitcher_data.p_throws.iloc[0]}HP), Date: {prev_day} ({myStr})")
    fig.show()



def main():
    data = clean_data(scrape_data())
    plot_data_interactive(data)

 
if __name__ == "__main__":
    main()

