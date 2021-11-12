import pandas as pd
import plotly_express as px

athlete_path = "Data/athlete_events.csv"
regions_path = "Data/noc_regions.csv"

athlete_data = pd.read_csv(athlete_path)
athlete_data = athlete_data.drop_duplicates(subset=["Event", "Games", "Medal"])

taekwondo_data = athlete_data[athlete_data["Sport"].isin(["Taekwondo"])].reset_index(drop=True)
gold_dist_taekwondo = taekwondo_data[taekwondo_data["Medal"].isin(["Gold"])]
silver_dist_taekwondo = taekwondo_data[taekwondo_data["Medal"].isin(["Silver"])]
bronze_dist_taekwondo = taekwondo_data[taekwondo_data["Medal"].isin(["Bronze"])]
gold_dist_taekwondo = gold_dist_taekwondo["NOC"].value_counts().reset_index().rename({"NOC": "gold count", "index": "NOC1"}, axis="columns")
silver_dist_taekwondo = silver_dist_taekwondo["NOC"].value_counts().reset_index().rename({"NOC": "silver count", "index": "NOC2"}, axis="columns")
bronze_dist_taekwondo = bronze_dist_taekwondo["NOC"].value_counts().reset_index().rename({"NOC": "bronze count", "index": "NOC3"}, axis="columns")
taekwondo_medal_dist = gold_dist_taekwondo
taekwondo_medal_dist = pd.concat([gold_dist_taekwondo, silver_dist_taekwondo, bronze_dist_taekwondo], axis=1, join="outer")
taekwondo_medal_dist = taekwondo_medal_dist.drop(["NOC1", "NOC3"], axis="columns")
fig = px.bar(taekwondo_medal_dist, x="NOC2", y=["gold count", "silver count", "bronze count"], title="Number of medals in taekwondo per country",
            labels={"value": "Medal count", "NOC2": "Countries"})
fig.update_layout(barmode="group")
fig.show()