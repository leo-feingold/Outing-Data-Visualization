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





plot_heatmap(clean_data(scrape_data()), selected_pitch, hitter)