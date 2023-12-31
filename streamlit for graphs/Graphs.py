import streamlit as st
import pandas as pd
import altair as alt
import matplotlib as plt

st.set_page_config(layout="wide")
df = pd.read_csv("./Modded_Datasheet.csv")

df["puStart_Time"] = pd.to_datetime(df["puStart_Time"])
df["puEnd_Time"] = pd.to_datetime(df["puEnd_Time"])
df["bcStart_Time"] = pd.to_datetime(df["bcStart_Time"])
df["bcEnd_Time"] = pd.to_datetime(df["bcEnd_Time"])
df["sStart_Time"] = pd.to_datetime(df["sStart_Time"])
df["sEnd_Time"] = pd.to_datetime(df["sEnd_Time"])

sets_df = pd.DataFrame(
    {
        "Exercise": ["Squats", "Pushups", "BicepCurls"],
        "Sets": [
            df["Squats_Sets"].sum(),
            df["Pushups_Sets"].sum(),
            df["BicepCurls_Sets"].sum(),
        ],
    }
)

pie_chart = (
    alt.Chart(sets_df)
    .mark_arc()
    .encode(
        theta="Sets",
        color=alt.Color(
            "Exercise", scale=alt.Scale(range=["#1f77b4", "#ff7f0e", "#2ca02c"])
        ),
        tooltip=["Exercise", "Sets"],
        y=alt.value(1),
    )
    .properties(width=500, height=500)
)

st.write(pie_chart)


bar_chart1 = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("puStart_Time", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("Pushups_Repetitions", axis=alt.Axis(title="Repetitions")),
    )
    .properties(width=1200, height=400)
)

st.write(bar_chart1)

bar_chart2 = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("bcStart_Time", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("BicepCurls_Repetitions", axis=alt.Axis(title="Repetitions")),
    )
    .properties(width=1200, height=400)
)

st.write(bar_chart2)

bar_chart3 = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("sStart_Time", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("Squats_Repetitions", axis=alt.Axis(title="Repetitions")),
    )
    .properties(width=1200, height=400)
)

st.write(bar_chart3)


time_series_chart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x=alt.X("puStart_Time", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("Total_Sets", axis=alt.Axis(title="Total Sets")),
        tooltip=["Total_Sets"],
    )
    .properties(width=1200, height=400)
)

st.write(time_series_chart)
st.write(
    "\n## The threshold values are the multiplication of the number of sets x number of individual reps divided by time taken for each set. "
)

st.write(
    "### This value give us a constant number for each set and after analying the data for all the sets we can aquare a median and around the median we can decided if the user is nearing exhaustion or has more energy left after the set."
)
df2 = pd.read_csv("./meow.csv")
df2 = df2.drop(["Unnamed: 0", "Unnamed: 5"], axis=1)
st.write(df2)
