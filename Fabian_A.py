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
            labels={"value": "Medal count", "NOC2": "Countries"}, template="seaborn")
    fig_medal.update_layout(barmode="group")

    fig_age = px.bar(sport_age_dist, x="Age", y="Age in percentage", title=f"Ages distrubution in {sport}", barmode = 'group', template="plotly_dark")
    fig_age.add_bar(name = "Age histogram all sports", x= all_data_age["Age"], y = all_data_age["Age in percentage"])
    
    return fig_medal, fig_age

def medals_taken():
        
        for i, item in enumerate([summer_medals_RUS, winter_medals_RUS]):
                item[i] = russia_data[russia_data["Season"].isin(seasons_list[i])].reset_index(drop=True)
                russia_winter_gold = russia_winter_data[(russia_winter_data["Medal"] == "Gold")].reset_index(drop=True)
                russia_winter_silver = russia_winter_data[(russia_winter_data["Medal"] == "Silver")].reset_index(drop=True)
                russia_winter_bronze = russia_winter_data[(russia_winter_data["Medal"] == "Bronze")].reset_index(drop=True)
                russia_winter_data = pd.concat([russia_winter_gold, russia_winter_silver, russia_winter_bronze])
                russia_winter_medals = russia_winter_data["Year"].value_counts().reset_index().rename({"Year": "Medal count", "index": "Year"}, axis="columns")
                russia_winter_medals = russia_winter_medals.sort_values(by="Year", ascending=True).reset_index(drop=True)
                russia_winter_medals["Season"] = seasons_list[i]
