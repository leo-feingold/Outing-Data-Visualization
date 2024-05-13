import pandas as pd
import numpy as np
import datetime
from baseball_scraper import statcast
from baseball_scraper import playerid_lookup # Might be worthwhile to use ID's instead of names to filter by pitcher...
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

playerName = 'Skenes, Paul'

def scrape_data():
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    prev_day = today - datetime.timedelta(days=1)
    prev_day = prev_day.strftime('%Y-%m-%d')
    data = statcast(start_dt = prev_day, end_dt = today_str)
    print(data.columns)
    return data

scrape_data()