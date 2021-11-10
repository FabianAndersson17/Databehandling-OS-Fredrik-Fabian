#Setup
import pandas as pd
import plotly_express as px


#Reads in the file
athlete_events = pd.read_csv("Data/athlete_events.csv")

#Sorting and structuring the data for the plot-A.
russia_sovjet_merged_all = athlete_events[athlete_events["NOC"].isin(["RUS", "URS"])].reset_index()
russia_sovjet_merged_dropped = russia_sovjet_merged_all.drop_duplicates(subset=["Event", "Games", "Medal"])
rus_sov_grouped_per_event = russia_sovjet_merged_dropped.groupby(["Event"]).count().reset_index()
sorted_per_medal = rus_sov_grouped_per_event.sort_values("Medal",ascending=False)
sorted_per_medal = sorted_per_medal.head(10)

#Plotting the bar-graph.
figA = px.bar(sorted_per_medal, title = "Russia & Sovjet top events in the Olympic Games (counted in nr of medal)",
             y = "Medal" ,x = "Event", color = "Medal", range_y=(10,25))
#figA.show()


#Sorting and structuring the data for the plot-B.
athlete_events_per_year = russia_sovjet_merged_dropped.groupby(["NOC","Year"]).count()
athlete_events_per_year =  athlete_events_per_year.reset_index()
athlete_events_per_year = athlete_events_per_year.sort_values("Year")

#Plotting the line-graph.
figB = px.line(title = "Medals per Olympic Game for Russia / Sovjet")
rus_sov_line = figB.add_scatter(name = "Russia / Sovjet" , y = athlete_events_per_year["Medal"], x = athlete_events_per_year["Year"], mode='lines+markers')
#figB.show()


#Sorting and structuring the data for the plot-C.
rus_sov = russia_sovjet_merged_all.groupby(["Year"]).median().reset_index()
all_count = athlete_events.groupby(["Year"]).median().reset_index()


figC = px.line(title = "Median age for Russia / Sovjet per Olympic Game")
rus_sov_line = figB.add_scatter(name = "Russia / Sovjet" , y = rus_sov["Age"], x = rus_sov["Year"], mode='lines+markers')
all_countires = figB.add_scatter(name = "Average for all countries" , y = all_count["Age"], x = all_count["Year"], mode='lines+markers')
figC.show()

