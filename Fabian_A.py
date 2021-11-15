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
    fig = px.bar(medal_dist, x="NOC2", y=["gold count", "silver count", "bronze count"], title=f"Number of medals in {sport} per country",
            labels={"value": "Medal count", "NOC2": "Countries"})
    fig.update_layout(barmode="group")
    return fig