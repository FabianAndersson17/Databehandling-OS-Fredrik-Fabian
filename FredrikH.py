#Setup
import pandas as pd
import plotly_express as px



#Reads in the file
athlete_events = pd.read_csv("Data/athlete_events.csv")
def testfunc(sport):
    #Sorting and structuring the data for the plot-A.
    russia_sovjet_merged_all = athlete_events[athlete_events["NOC"].isin(["RUS", "URS"])].reset_index()
    #Dropping all duplicates of medals in the same event (for example, fotball only counts as 1 medal instead of 22 
    # because it's 22 players in a team)
    russia_sovjet_merged_dropped = russia_sovjet_merged_all.drop_duplicates(subset=["Event", "Games", "Medal"])
    rus_sov_grouped_per_event = russia_sovjet_merged_dropped.groupby(["Event"]).count().reset_index()
    sorted_per_medal = rus_sov_grouped_per_event.sort_values("Medal",ascending=False)
    sorted_per_medal = sorted_per_medal.head(10)

    #Plotting the bar-graph.
    figA = px.bar(sorted_per_medal, title = "Russia & Sovjet top events in the Olympic Games (counted in nr of medal)",
                y = "Medal" ,x = "Event", color = "Medal", range_y=(10,25))
    figA.show()


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

    #Plotting the line-graph.
    figC = px.line(title = "Median age for Russia / Sovjet per Olympic Game")
    rus_sov_line = figC.add_scatter(name = "Russia / Sovjet" , y = rus_sov["Age"], x = rus_sov["Year"], mode='lines+markers')
    all_countires = figC.add_scatter(name = "Average for all countries" , y = all_count["Age"], x = all_count["Year"], mode='lines+markers')
    figC.show()

    #Sorting and structuring the data for the plot-D.
    rus_sov_D = russia_sovjet_merged_all.groupby(["Event"]).median().reset_index()
    top5_tallest_events = rus_sov_D.sort_values("Height",ascending=False).head(5)
    top5_shortest_events = rus_sov_D.sort_values("Height",ascending=True).head(5)

    #Plotting the bar-graph.
    figD = px.bar(title = "Median height for Russia / Sovjet per Olympic Game",)
    tallest= figD.add_bar(name = "Top5 tallest sports" , y = top5_tallest_events ["Height"], x = top5_tallest_events ["Event"])
    shortest = figD.add_bar(name = "Top5 shortest sports",y=  top5_shortest_events ["Height"], x = top5_shortest_events["Event"])
    figD.show()

    #Exercise 2: Choosed sport = Football

    football_data = athlete_events[athlete_events["Sport"].isin(["Football"])].reset_index()
    football_data = football_data.drop_duplicates(subset=["Event", "Games", "Medal"])
    football_data = football_data.groupby(["Team"]).count().reset_index()
    football_data = football_data.sort_values("Medal",ascending=False).head(42)

    #Plotting the bar-graph.
    figE = px.bar(football_data, title = "Fussball", y = "Medal", x = "Team", color= "Team")
    #figE.show()

    #Exercise 2: Choosed sport 2 = Tennis

    tennis_data = athlete_events[athlete_events["Sport"].isin([sport])].reset_index()
    tennis_data = tennis_data.drop_duplicates(subset=["Event", "Games", "Medal"])
    tennis_data = tennis_data.groupby(["Team"]).count().reset_index()
    tennis_data = tennis_data.sort_values("Medal",ascending=False)

    #Plotting the bar-graph.
    figF = px.bar(tennis_data, title = sport, y = "Medal", x = "Team", color= "Team")
    #figF.show()
    return figF

