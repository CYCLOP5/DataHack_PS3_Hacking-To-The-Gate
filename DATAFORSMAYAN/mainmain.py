import streamlit as st
import pandas as pd
import altair as alt

# Load data
df = pd.read_csv("./Modded_Datasheet.csv")

# Create bar chart with swapped axis
bar_chart1 = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="puStart_Time",
        y="Pushups_Repetitions",
    )
    .interactive()
)

# Display bar chart
st.write(bar_chart1)


# Create bar chart with swapped axis
bar_chart2 = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="bcStart_Time",
        y="BicepCurls_Repetitions",
    )
    .interactive()
)

# Display bar chart
st.write(bar_chart2)

bar_chart2 = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="sStart_Time",
        y="Squats_Repetitions",
    )
    .interactive()
)

# Display bar chart
st.write(bar_chart2)


# Create a new dataframe with the sum of sets for each exercise
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

# Create pie chart
pie_chart = (
    alt.Chart(sets_df)
    .mark_arc()
    .encode(
        theta="Sets", color="Exercise", tooltip=["Exercise", "Sets"], y=alt.value(1)
    )
    .properties(width=500, height=500)
)

# Display pie chart
st.write(pie_chart)
