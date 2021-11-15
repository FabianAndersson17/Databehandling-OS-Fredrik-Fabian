import pandas as pd
import plotly_express as px

athlete_path = "Data/athlete_events.csv"
regions_path = "Data/noc_regions.csv"

athlete_data = pd.read_csv(athlete_path)
athlete_data = athlete_data.drop_duplicates(subset=["Event", "Games", "Medal"])

taekwondo_medal_list = []

# for i in []
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
    sport_ages = sport_ages.sort()
    sport_age_dist = sport_data[sport_data["Age"].isin([sport_ages])]
    sport_age_dist = sport_age_dist["Age"].value_counts().reset_index().rename({"Age": "Age count", "index": "Age"}, axis="columns")
    sport_age_dist = sport_age_dist.sort_values(by="Age").reset_index(drop=True)

    fig_medal = px.bar(medal_dist, x="NOC2", y=["gold count", "silver count", "bronze count"], title=f"Number of medals in {sport} per country",
            labels={"value": "Medal count", "NOC2": "Countries"})
    fig_medal.update_layout(barmode="group")
    fig_age = px.bar(sport_age_dist, x="Age", y="Age count", title=f"Ages distrubution in {sport}")
    return [fig_medal, fig_age]
