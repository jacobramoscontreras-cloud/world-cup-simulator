import streamlit as st
import pandas as pd
import plotly.express as px
from world_cup import *
st.set_page_config(
    page_title="World Cup Simulator",
    page_icon="🏆",
    layout="wide"
)
st.markdown("""
<style>
.main {
    background-color: #f7f9cd;
}

h1 {
    text-align: center;
    font-size: 48px;
}

.metric-card {
    background-color: black;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

if "simulationDone" not in st.session_state:
    st.session_state.simulationDone = False

st.title("🏆 World Cup Simulator")

selectedTeam = st.selectbox("Select a team", list(teamStats.keys()))

st.subheader(teamFlags[selectedTeam] + " " + selectedTeam)
#st.write("Attack:", teamStats[selectedTeam]["attack"])
#st.write("Defense:", teamStats[selectedTeam]["defense"])
#st.write("Strength:", getTeamStrength(selectedTeam))
st.header("⚽ Team Ratings")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Attack", teamStats[selectedTeam]["attack"])

with col2:
    st.metric("Defense", teamStats[selectedTeam]["defense"])

with col3:
    st.metric("Strength", getTeamStrength(selectedTeam))

simulationCount = st.slider("Number of simulations", 100, 10000, 1000)

st.header("Match Predictor")

teamA = st.selectbox("Select Team A", list(teamStats.keys()))
teamB = st.selectbox("Select Team B", list(teamStats.keys()))

if st.button("Predict Match"):
    teamAWins = 0
    teamBWins = 0
    draws = 0

    for i in range(1000):
        goalsA, goalsB = playMatch(teamA, teamB)

        if goalsA > goalsB:
            teamAWins += 1
        elif goalsB > goalsA:
            teamBWins += 1
        else:
            draws += 1

    st.write(teamA, "win chance:", round((teamAWins / 1000) * 100, 2), "%")
    st.write(teamB, "win chance:", round((teamBWins / 1000) * 100, 2), "%")
    st.write("Draw chance:", round((draws / 1000) * 100, 2), "%")

if st.button("Run Simulator"):
    st.session_state.simulationDone = True

if st.session_state.simulationDone:
    resetUpsets()

    roundOf32, groupStandings = createRoundOf32()

    roundOf16, round32Matches = playKnockoutRound(roundOf32, "Round of 32")
    quarterFinals, round16Matches = playKnockoutRound(roundOf16, "Round of 16")
    semiFinals, quarterFinalMatches = playKnockoutRound(quarterFinals, "Quarterfinals")
    finalTeams, semiFinalMatches = playKnockoutRound(semiFinals, "Semifinals")
    championList, finalMatch = playKnockoutRound(finalTeams, "Final")

    champion = championList[0]

    st.success("🏆 Champion: " + teamFlags[champion] + " " + champion)
    
    st.header("🧩 Tournament Bracket")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.subheader("Round of 32")
        for match in round32Matches:
            st.markdown(
                f"""
                <div style="
                    background-color: #D3D3D3;
                    padding: 10px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                ">
                    {match}
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with col2:
        st.subheader("Round of 16")
        for match in round16Matches:
            st.markdown(
                f"""
                <div style="
                    background-color: #D3D3D3;
                    padding: 10px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                ">
                    {match}
                </div>
                """,
                unsafe_allow_html=True
            )

    with col3:
        st.subheader("Quarterfinals")
        for match in quarterFinalMatches:
            st.markdown(
                f"""
                <div style="
                    background-color: #D3D3D3;
                    padding: 10px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                ">
                    {match}
                </div>
                """,
                unsafe_allow_html=True
            )

    with col4:
        st.subheader("Semifinals")
        for match in semiFinalMatches:
            st.markdown(
                f"""
                <div style="
                    background-color: #D3D3D3;
                    padding: 10px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                ">
                    {match}
                </div>
                """,
                unsafe_allow_html=True
            )

    with col5:
        st.subheader("Final")
        for match in finalMatch:
            st.markdown(
                f"""
                <div style="
                    background-color: #FFD700;
                    padding: 10px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                ">
                    {match}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.success("🏆 Champion: " + teamFlags[champion] + " " + champion)

    st.header("Group Stage Tables")
    for groupName, standings in groupStandings.items():
        st.subheader(groupName)
        
        rows = []

        for team, stats in standings:
            rows.append({
                "Team": teamFlags[team] + " " + team,
                "Pts": stats["points"],
                "GF": stats["goalsFor"],
                "GA": stats["goalsAgainst"],
                "GD": stats["goalDifference"]
            })

        groupDF = pd.DataFrame(rows)

        st.dataframe(groupDF, use_container_width=True, hide_index=True)

    st.header("📊 Championship Probabilities")

    championships = {}

    for i in range(simulationCount):
        winner = simulateTournament()
        championships[winner] = championships.get(winner, 0) + 1

    sortedTeams = sorted(
        championships.items(),
        key=lambda item: item[1],
        reverse=True
    )

    chartTeams = []
    chartPercents = []

    for team, wins in sortedTeams:
        percent = (wins / simulationCount) * 100
        chartTeams.append(team)
        chartPercents.append(percent)

    chartData = pd.DataFrame({
        "Team": chartTeams,
        "Championship Chance (%)": chartPercents
    })

    fig = px.bar(
    chartData,
    x="Team",
    y="Championship Chance (%)",
    text="Championship Chance (%)",
    color="Championship Chance (%)"
    )

    fig.update_traces(
    texttemplate='%{text:.2f}%',
    textposition='outside'
    )

    fig.update_layout(
    title="World Cup Championship Probabilities",
    xaxis_title="Team",
    yaxis_title="Chance to Win (%)",
    height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    for team, wins in sortedTeams:
        percent = (wins / simulationCount) * 100
        st.write(teamFlags[team], team, "-", round(percent, 2), "%")

    st.header("Team Progression Probabilities")

    progressionCounts = {}

    rounds = ["Group Stage","Round of 32", "Round of 16", "Quarterfinals", "Semifinals", "Final", "Champion"]

    for team in teamStats.keys():
        progressionCounts[team] = {}

        for roundName in rounds:
            progressionCounts[team][roundName] = 0

    for i in range(simulationCount):
        progression = simulateTournamentProgression()

        for team, finish in progression.items():
            for roundName in rounds:
                if rounds.index(finish) >= rounds.index(roundName):
                    progressionCounts[team][roundName] += 1
            
    rows = []

    for team, results in progressionCounts.items():
        row = {"Team": team}

        for roundName in rounds:
            row[roundName] = round((results[roundName] / simulationCount) * 100, 2)

        rows.append(row)

    progressionDF = pd.DataFrame(rows)

    selectedRound = st.selectbox(
        "Choose round to chart",
        ["Round of 32", "Round of 16", "Quarterfinals", "Semifinals", "Final", "Champion"]
    )

    chartProgression = progressionDF.sort_values(
        by=selectedRound,
        ascending=False
    ).head(20)

    fig = px.bar(
        chartProgression,
        x="Team",
        y=selectedRound,
        text=selectedRound,
        color=selectedRound,
        title=selectedRound + " Probability"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(progressionDF, use_container_width=True, hide_index=True)