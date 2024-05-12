import pandas as pd
import numpy as np
import datetime
from baseball_scraper import statcast
from baseball_scraper import playerid_lookup # Might be worthwhile to use ID's instead of names to filter by pitcher...
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle

playerName = 'Skenes, Paul'
selected_pitch = '4-Seam Fastball'
hitter = 'R'

def scrape_data():
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')
    prev_day = today - datetime.timedelta(days=1)
    prev_day = prev_day.strftime('%Y-%m-%d')
    data = statcast(start_dt = prev_day, end_dt = today_str)

    return data

def clean_data(df):
    df = df[['pitcher', 'player_name', 'pitch_type', 'pitch_name', 'plate_x', 'plate_z', 'stand']]
    df.dropna(inplace=True)
    return df

def filter_data(df, player_name, pitch_name, stand):
    return df[(df['player_name'] == player_name) & (df['pitch_name'] == pitch_name) & (df['stand'] == stand)]


def plot_heatmap(df, pitch_type, stand):
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')
    prev_day = today - datetime.timedelta(days=1)
    prev_day = prev_day.strftime('%Y-%m-%d')

    max_abs_x = np.max(np.abs(df['plate_x']))
    max_abs_z = np.max(np.abs(df['plate_z']))
    plot_range_z = max(max_abs_z, 5)

    hitter_tag = 'RHH' if stand == 'R' else 'LHH'

    fig, ax = plt.subplots(figsize=(6, 6))
    sns.kdeplot(data=df, x='plate_x', y='plate_z', fill=True, thresh=0, levels=100, cmap="coolwarm")

    strike_zone = Rectangle((-0.71, 1.5), 1.42, 2.0, fill=False, color='black', linewidth=2)
    ax.add_patch(strike_zone)

    ax.set_title(f"Heatmap of {pitch_type} locations for {playerName} against {hitter_tag}, Date: {prev_day} (Catcher's Perspective)")
    ax.set_xlabel('Horizontal Location (feet)')
    ax.set_ylabel('Vertical Location (feet)')

    ax.set_xlim(-max_abs_x, max_abs_x)
    ax.set_ylim(0, plot_range_z)
    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor('#3D50C3')
    ax.patch.set_facecolor('#3D50C3')
    plt.tight_layout()
    plt.show()



def main():
    data = clean_data(scrape_data())
    filtered_data = filter_data(data, playerName, selected_pitch, hitter)
    plot_heatmap(filtered_data, selected_pitch, hitter)

if __name__== "__main__":
    main()