# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# Each tab is drawn by one script
from scripts.timeseries import time_series_tab
# from scripts.density import density_tab

# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

# Read data into dataframes
topics = pd.read_csv(join(dirname(__file__), 'data', 'Rosbag_Content.csv'), 
	                                          index_col=0).dropna()

# Create each of the tabs
tab1 = time_series_tab(topics)
# tab2 = density_tab(flights)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab])
# tabs = Tabs(tabs = [tab1, tab2, tab3, tab4, tab5])

# Put the tabs in the current document for display
curdoc().add_root(tabs)


