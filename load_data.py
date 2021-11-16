import re
import pandas as pd
import plotly_express as px

athlete_path = "Data/athlete_events.csv"
regions_path = "Data/noc_regions.csv"

athlete_data = pd.read_csv(athlete_path)
athlete_data = athlete_data.drop_duplicates(subset=["Event", "Games", "Medal"])
russia_data = athlete_data[athlete_data["Team"].isin(["Russia", "Soviet Union"])].reset_index(drop=True)

seasons_list = ["Summer", "Winter"]

def data_locator(sport):
    sport_data = athlete_data[athlete_data["Sport"].isin([sport])].reset_index(drop=True)

    gold_dist = sport_data[sport_data["Medal"].isin(["Gold"])]
    silver_dist = sport_data[sport_data["Medal"].isin(["Silver"])]
    bronze_dist = sport_data[sport_data["Medal"].isin(["Bronze"])]
    gold_dist = gold_dist["NOC"].value_counts().reset_index().rename({"NOC": "gold count", "index": "NOC1"}, axis="columns")
    silver_dist = silver_dist["NOC"].value_counts().reset_index().rename({"NOC": "silver count", "index": "NOC2"}, axis="columns")
    bronze_dist = bronze_dist["NOC"].value_counts().reset_index().rename({"NOC": "bronze count", "index": "NOC3"}, axis="columns")
    medal_dist = pd.concat([gold_dist, silver_dist, bronze_dist], axis=1, join="outer")
    medal_dist = medal_dist.drop(["NOC1", "NOC3"], axis="columns")

    sport_ages = sport_data["Age"].unique().tolist()
    sport_ages.sort()
    sport_age_dist = sport_data[sport_data["Age"].isin(sport_ages)]
    sport_age_dist = sport_age_dist["Age"].value_counts().reset_index().rename({"Age": "Age count", "index": "Age"}, axis="columns")
    sport_age_dist = sport_age_dist.sort_values(by="Age").reset_index(drop=True)
    total_all2 = sport_age_dist['Age count'].sum()
    sport_age_dist["Total participants"] = total_all2
    sport_age_dist["Age in percentage"] = sport_age_dist["Age count"] / sport_age_dist["Total participants"]

    all_data_age = athlete_data.groupby(["Age"]).count().reset_index()
    total_all = all_data_age['ID'].sum()
    all_data_age["Total participants"] = total_all
    all_data_age["Age in percentage"] = all_data_age["ID"] / all_data_age["Total participants"]

    fig_medal = px.bar(medal_dist, x="NOC2", y=["gold count", "silver count", "bronze count"], title=f"Number of medals in {sport} per country",
            labels={"value": "Medal count", "NOC2": "Countries"}, template="plotly_dark")
    fig_medal.update_layout(barmode="group")

    fig_age = px.bar(sport_age_dist, x="Age", y="Age in percentage", title=f"Ages distrubution in {sport}", barmode = 'group', template="plotly_dark")
    fig_age.add_bar(name = "Age histogram all sports", x= all_data_age["Age"], y = all_data_age["Age in percentage"])
    
    return fig_medal, fig_age

def russia_graphs(grafPicker):
        if grafPicker == "medalGraph":
                for i, item in enumerate(seasons_list):
                        russia_medals = russia_data[russia_data["Season"].isin([item])].reset_index(drop=True)
                        russia_gold = russia_medals[(russia_medals["Medal"] == "Gold")].reset_index(drop=True)
                        russia_silver = russia_medals[(russia_medals["Medal"] == "Silver")].reset_index(drop=True)
                        russia_bronze = russia_medals[(russia_medals["Medal"] == "Bronze")].reset_index(drop=True)
                        russia_seasonal_data = pd.concat([russia_gold, russia_silver, russia_bronze])
                        russia_seasonal_medals = russia_seasonal_data["Year"].value_counts().reset_index().rename({"Year": f"{item} medal count", "index": "Year"}, axis="columns")
                        russia_seasonal_medals = russia_seasonal_medals.sort_values(by="Year", ascending=True).reset_index(drop=True)
                        russia_seasonal_medals["Season"] = seasons_list[i]
        
                        if item == "Summer":
                                summer_rus_medals = russia_seasonal_medals
                        elif item == "Winter":
                                winter_rus_medals = russia_seasonal_medals

                for i, item in enumerate(seasons_list):
                        total_medals = athlete_data[athlete_data["Season"].isin([item])].reset_index(drop=True)
                        total_gold = total_medals[(total_medals["Medal"] == "Gold")].reset_index(drop=True)
                        total_silver = total_medals[(total_medals["Medal"] == "Silver")].reset_index(drop=True)
                        totla_bronze = total_medals[(total_medals["Medal"] == "Bronze")].reset_index(drop=True)
                        total_seasonal_data = pd.concat([total_gold, total_silver, totla_bronze])
                        total_seasonal_medals = total_seasonal_data["Year"].value_counts().reset_index().rename({"Year": f"{item} medal count", "index": "Year"}, axis="columns")
                        total_seasonal_medals = total_seasonal_medals.sort_values(by="Year", ascending=True).reset_index(drop=True)
                        total_seasonal_medals["Season"] = seasons_list[i]
        
                        if item == "Summer":
                                summer_total_medals = total_seasonal_medals
                        elif item == "Winter":
                                winter_total_medals = total_seasonal_medals


                winter_rus_medals["Procent winter medals"] = winter_rus_medals["Winter medal count"]/winter_total_medals["Winter medal count"]
                summer_rus_medals["Procent summer medals"] = summer_rus_medals["Summer medal count"]/summer_total_medals["Summer medal count"]
                seasonal_medals_RUS = pd.concat([winter_rus_medals, summer_rus_medals])

                seasonal_medals_RUS.sort_values(by="Year", ascending=True)

                fig_procent_medals = px.bar(seasonal_medals_RUS, x="Year", y=["Procent winter medals", "Procent summer medals"], title="Procent of medals taken by russia per year", template="plotly_dark")
                fig_procent_medals.update_layout(barmode="group")
                return fig_procent_medals

        if grafPicker == "medianGraph":
                median_data_russia = russia_data.groupby(["Year"]).median().reset_index()
                all_countries = athlete_data.groupby(["Year"]).median().reset_index()
                fig_median_age = px.line(title = "Median age for Russia / Soviet per Olympic Game")
                rus_sov_line = fig_median_age.add_scatter(name = "Russia / Sovjet" , y = median_data_russia["Age"], x = median_data_russia["Year"], mode='lines+markers')
                all_countires = fig_median_age.add_scatter(name = "Average for all countries" , y = all_countries["Age"], x = all_countries["Year"], mode='lines+markers')

                median_data_height_russia = russia_data.groupby(["Event"]).median().reset_index()
                top5_tallest_events = median_data_russia.sort_values("Height",ascending=False).head(5)
                top5_shortest_events = median_data_russia.sort_values("Height",ascending=True).head(5)
                fig_median_height = px.bar(title = "Median height for Russia / Soviet per Olympic Game",)
                tallest= fig_median_height.add_bar(name = "Top5 tallest sports" , y = top5_tallest_events ["Height"], x = top5_tallest_events ["Event"])
                shortest = fig_median_height.add_bar(name = "Top5 shortest sports",y=  top5_shortest_events ["Height"], x = top5_shortest_events["Event"])

                return fig_median_age, fig_median_height

        if grafPicker == "genderGraph":
                russia_female_data = russia_data[russia_data["Sex"].isin(["F"])].reset_index(drop=True) ## Takes out all females in the dataframe
                russia_male_data = russia_data[russia_data["Sex"].isin(["M"])].reset_index(drop=True) ## Takes out all the makes in the dataframe
                russia_female_sports = russia_female_data["Sport"].value_counts().reset_index().rename({"Sport": "Female count", "index": "Sport"}, axis="columns") ## Calulates the number of genders in each sport
                russia_male_sports = russia_male_data["Sport"].value_counts().reset_index().rename({"Sport": "Male count", "index": "Sport"}, axis="columns")
                russia_male_sports = russia_male_sports.sort_values(by="Sport", ascending=True).reset_index(drop=True) ## Sorts the numbers 
                russia_female_sports = russia_female_sports.sort_values(by="Sport", ascending=True)
                russia_sports_genders = russia_male_sports
                russia_sports_genders = russia_sports_genders.merge(russia_female_sports, how="right") ## Merges the female dataframe into the genders dataframe
                russia_sports_genders = russia_sports_genders.fillna(0) ## Fills missing values with 0
                russia_sports_genders = russia_sports_genders.sort_values(by="Male count", ascending=False) ## Sorts the genders dataframe
                fig_gender_in_sports = px.bar(russia_sports_genders, x="Sport", y=["Male count", "Female count"]) 
                fig_gender_in_sports.update_layout(barmode="group")
                
                return fig_gender_in_sports
