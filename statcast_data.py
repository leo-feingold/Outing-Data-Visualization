import pandas as pd
import numpy as np
import datetime
from baseball_scraper import statcast
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

today = datetime.date.today()
today_str = today.strftime('%Y-%m-%d')

prev_day = today - datetime.timedelta(days=1)
prev_day = prev_day.strftime('%Y-%m-%d')

def scrape_data():
    data = statcast(start_dt = prev_day, end_dt = today_str)
    return data

def clean_data(df):
    df = scrape_data()
    df = df[['pitcher', 'player_name', 'pitch_type', 'release_speed', 'pfx_x', 'pfx_z', 'release_spin_rate', 'spin_axis', 'release_extension', 'pitch_name']]
    df['pfx_x'] = df['pfx_x'] * -12
    df['pfx_z'] = df['pfx_z'] * 12
    return df

def plot_data(df):
    playerName = 'Schmidt, Clarke'
    df = clean_data(scrape_data())
    pitcher_data = df[df['player_name'] == playerName]
    pitcher_data = pitcher_data.dropna(subset=['pfx_x', 'pfx_z', 'release_speed', 'release_spin_rate', 'spin_axis', 'release_extension', 'pitch_type'])


    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='pfx_x', y='pfx_z', data=pitcher_data, hue='pitch_type', style='pitch_type', s=100, palette='deep')
    plt.title(f"Pitch Movement Profile for {playerName}, Date: {prev_day} (Pitcher's Perspective)")
    plt.xlabel('Horizontal Movement (pfx_x)')
    plt.ylabel('Vertical Movement (pfx_z)')
    plt.legend(title='Pitch Type')
    plt.grid(True)
    plt.show()

def plot_data_interactive(df):
    playerName = 'Schmidt, Clarke'
    df = clean_data(df)  # Assuming df is already cleaned and passed here
    pitcher_data = df[df['player_name'] == playerName]
    pitcher_data = pitcher_data.dropna(subset=['pfx_x', 'pfx_z', 'release_speed', 'release_spin_rate', 'spin_axis'])

    # Create an interactive scatter plot
    fig = px.scatter(pitcher_data, x='pfx_x', y='pfx_z', color='pitch_type',
                     hover_data=['release_speed', 'release_spin_rate', 'spin_axis', 'release_extension'],
                     labels={
                         'pfx_x': 'Horizontal Movement (inches)',
                         'pfx_z': 'Vertical Movement (inches)',
                         'pitch_type': 'Pitch Type'
                     },
                     title=f"Pitch Movement Profile for {playerName}, Date: {prev_day} (Pitcher's Perspective)")
    fig.show()



def main():
    data = clean_data(scrape_data())
    plot_data_interactive(data)

 
if __name__ == "__main__":
    main()

