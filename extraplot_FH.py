#Setup
import pandas as pd
from _plotly_utils.basevalidators import type_str
import plotly_express as px

#Reads in the file
athlete_events = pd.read_csv("Data/athlete_events.csv")

athlete_events_drop = athlete_events.drop_duplicates(subset=["Event", "Games", "Medal"])
athlete_events_per_year = athlete_events_drop.groupby(["NOC","Year"]).count()
athlete_events_per_year =  athlete_events_per_year.reset_index()
athlete_events_per_year["Medal"] = athlete_events_per_year["Medal"].cumsum()
athlete_events_per_year = athlete_events_per_year.dropna()


fig = px.scatter(athlete_events_per_year, x = "Medal", y = "Medal", 
    size = "Medal", color = "NOC", size_max = 70,
    log_x = True, animation_frame = "Year", title="Gapminder",
    range_x = [0, 5000], range_y = [1890,2020])
fig.show()