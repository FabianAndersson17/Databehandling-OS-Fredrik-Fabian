#Setup
import pandas as pd
import plotly_express as px


#Reads in the file
athlete_events = pd.read_csv("Data/athlete_events.csv")

#Sorting and structuring the data for the plot-A.
russia_sovjet_merged_all = athlete_events[athlete_events["NOC"].isin(["RUS", "URS"])].reset_index()
russia_sovjet_merged_all = russia_sovjet_merged_all.drop_duplicates(subset=["Event", "Games", "Medal"])
rus_sov_grouped_per_event = russia_sovjet_merged_all.groupby(["Event"]).count().reset_index()
sorted_per_medal = rus_sov_grouped_per_event.sort_values("Medal",ascending=False)
sorted_per_medal = sorted_per_medal.head(10)

#Plotting the bar-graph.
figA = px.bar(sorted_per_medal, title = "Russia & Sovjet top events in the Olympic Games (counted in nr of medal)",
             y = "Medal" ,x = "Event", color = "Medal", range_y=(10,25))
figA.show()


#Sorting and structuring the data for the plot-B.
athlete_events_drop = athlete_events.drop_duplicates(subset=["Event", "Games", "Medal"])
athlete_events_per_year = athlete_events_drop.groupby(["NOC","Year"]).count()
athlete_events_per_year =  athlete_events_per_year.reset_index()

#merging Russia and Sovjet and sorting the values from first Olympic Games to last.
russia_sovjet_merge = athlete_events_per_year[athlete_events_per_year["NOC"].isin(["RUS", "URS"])].reset_index()
russia_sovjet_merge = russia_sovjet_merge.sort_values("Year")

#Plotting the line-graph.
figB = px.line(title = "Medals per Olympic Game for Russia / Sovjet")
rus_sov_line = figB.add_scatter(name = "Russia / Sovjet" , y = russia_sovjet_merge["Medal"], x = russia_sovjet_merge["Year"], mode='lines+markers')
figB.show()
