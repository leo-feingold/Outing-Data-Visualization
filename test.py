import pandas as pd
import numpy as np
import datetime
from baseball_scraper import statcast
from baseball_scraper import playerid_lookup # Might be worthwhile to use ID's instead of names to filter by pitcher...
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from matplotlib.patches import Rectangle

playerName = 'Skenes, Paul'
selected_pitch = 'Slider'
hitter = 'R'

def scrape_data():
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')
    prev_day = today - datetime.timedelta(days=1)
    prev_day = prev_day.strftime('%Y-%m-%d')
    data = statcast(start_dt = prev_day, end_dt = today_str)
    
    #print(data.columns)
    #print(data.stand)
    #location of pitch stored in plate_x and plate_z, stand is RHH vs LHH

    return data

def clean_data(df):
    df = df[['pitcher', 'player_name', 'pitch_type', 'pitch_name', 'plate_x', 'plate_z', 'stand']]
    df.dropna(inplace=True)
    return df

def plot_heatmap(df, pitch_type, stand):
    df = df[df['player_name'] == playerName]
    df = df[df['stand'] == stand]
    df = df[df['pitch_name'] == pitch_type] 

    hitter_tag = 'RHH' if stand == 'R' else 'LHH'

    strike_zone = Rectangle((-0.71, 1.5), 1.42, 2.0, fill=False, color='red', linewidth=2)
    ax.add_patch(strike_zone)

    fig, ax = plt.subplots(figsize=(6, 6))
    sns.kdeplot(data=df, x='plate_x', y='plate_z', fill=True, thresh=0, levels=100, cmap="viridis")
    ax.set_title(f'Heatmap of {pitch_type} locations for {playerName} against {hitter_tag}')
    ax.set_xlabel('Horizontal Location (feet)')
    ax.set_ylabel('Vertical Location (feet)')
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 5)
    plt.show()



plot_heatmap(clean_data(scrape_data()), selected_pitch, hitter)