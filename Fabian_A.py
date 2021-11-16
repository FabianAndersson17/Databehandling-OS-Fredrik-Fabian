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

        if grafPicker == "genderGraph":
                pass

