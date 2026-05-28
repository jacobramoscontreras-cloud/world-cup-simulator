import streamlit as st
import pandas as pd
import plotly.express as px
from world_cup import *

st.set_page_config(
    page_title="World Cup Simulator",
    page_icon="🏆",
    layout="wide"
)

def addFlagsToMatch(match):
    for team, flag in teamFlags.items():
        match = match.replace(team, flag + " " + team)
    return match

st.markdown("""
<div style="
    background-color:#0057B8;
    padding:18px 30px;
    border-radius:0px;
    color:white;
    display:flex;
    justify-content:space-between;
    align-items:center;
">
    <div style="font-size:28px; font-weight:bold;">FIFA WORLD CUP 2026™</div>
</div>

<div style="
    background:linear-gradient(90deg,#315BFF,#003BDB);
    padding:35px;
    margin-top:20px;
    border-radius:18px;
    color:white;
">
    <h1 style="font-size:46px; margin-bottom:5px;">🏆 FIFA World Cup 2026™</h1>
    <p style="font-size:20px;">11 June - 19 July 2026</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Controls")

    page = st.radio(
        "Navigate",
        ["🏆 Simulator", "📊 Probabilities", "⚽ Teams", "📋 Groups"]
    )

    simulationCount = st.slider(
        "Number of simulations",
        100,
        10000,
        1000
    )

    runSimulation = st.button("🏆 Run Simulator")
    resetApp = st.button("🔄 Reset Simulator")

if resetApp:
    st.session_state.clear()
    st.rerun()

if runSimulation:
    with st.spinner("Simulating tournament..."):
        resetUpsets()

    roundOf32, groupStandings = createRoundOf32()

    roundOf16, round32Matches = playKnockoutRound(roundOf32, "Round of 32")
    quarterFinals, round16Matches = playKnockoutRound(roundOf16, "Round of 16")
    semiFinals, quarterFinalMatches = playKnockoutRound(quarterFinals, "Quarterfinals")
    finalTeams, semiFinalMatches = playKnockoutRound(semiFinals, "Semifinals")
    championList, finalMatch = playKnockoutRound(finalTeams, "Final")

    st.session_state.groupStandings = groupStandings
    st.session_state.round32Matches = round32Matches
    st.session_state.round16Matches = round16Matches
    st.session_state.quarterFinalMatches = quarterFinalMatches
    st.session_state.semiFinalMatches = semiFinalMatches
    st.session_state.finalMatch = finalMatch
    st.session_state.champion = championList[0]

if page == "🏆 Simulator":
    st.header("🧩 Tournament Bracket")

    if "champion" not in st.session_state:
        st.info("Click **Run Simulator** in the sidebar first.")
    else:
        champion = st.session_state.champion
        st.success("🏆 Champion: " + teamFlags[champion] + " " + champion)

        col1, col2, col3, col4, col5 = st.columns(5)

        rounds = [
            ("Round of 32", st.session_state.round32Matches, col1),
            ("Round of 16", st.session_state.round16Matches, col2),
            ("Quarterfinals", st.session_state.quarterFinalMatches, col3),
            ("Semifinals", st.session_state.semiFinalMatches, col4),
            ("Final", st.session_state.finalMatch, col5),
        ]

        for roundName, matches, col in rounds:
            with col:
                st.subheader(roundName)

                for match in matches:
                    st.markdown(
                        f"""
                        <div style="
                            background-color:#1E222A;
                            padding:10px;
                            border-radius:10px;
                            margin-bottom:10px;
                            color:white;
                        ">
                            {addFlagsToMatch(match)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

elif page == "📊 Probabilities":
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

    mostLikelyTeam = sortedTeams[0][0]
    mostLikelyWins = sortedTeams[0][1]
    mostLikelyPercent = (mostLikelyWins / simulationCount) * 100

    st.metric(
        "Most Likely Champion",
        teamFlags[mostLikelyTeam] + " " + mostLikelyTeam,
        str(round(mostLikelyPercent, 2)) + "%"
    )

    chartData = pd.DataFrame({
        "Team": [teamFlags[team] + " " + team for team, wins in sortedTeams],
        "Championship Chance (%)": [
            (wins / simulationCount) * 100 for team, wins in sortedTeams
        ]
    })

    fig = px.bar(
        chartData,
        x="Team",
        y="Championship Chance (%)",
        text="Championship Chance (%)",
        color="Championship Chance (%)",
        title="World Cup Championship Probabilities"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header("Team Progression Probabilities")

    progressionCounts = {}

    rounds = [
        "Group Stage",
        "Round of 32",
        "Round of 16",
        "Quarterfinals",
        "Semifinals",
        "Final",
        "Champion"
    ]

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
        row = {"Team": teamFlags[team] + " " + team}

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

    fig2 = px.bar(
        chartProgression,
        x="Team",
        y=selectedRound,
        text=selectedRound,
        color=selectedRound,
        title=selectedRound + " Probability"
    )

    fig2.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(progressionDF, use_container_width=True, hide_index=True)

elif page == "⚽ Teams":
    st.header("⚽ Team Ratings")

    selectedTeam = st.selectbox("Select a team", list(teamStats.keys()))

    st.subheader(teamFlags[selectedTeam] + " " + selectedTeam)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Attack", teamStats[selectedTeam]["attack"])

    with col2:
        st.metric("Defense", teamStats[selectedTeam]["defense"])

    with col3:
        st.metric("Strength", getTeamStrength(selectedTeam))

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

        st.write(teamFlags[teamA], teamA, "win chance:", round((teamAWins / 1000) * 100, 2), "%")
        st.write(teamFlags[teamB], teamB, "win chance:", round((teamBWins / 1000) * 100, 2), "%")
        st.write("Draw chance:", round((draws / 1000) * 100, 2), "%")

    st.header("Team Comparison")

    compareTeam1 = st.selectbox("Compare Team 1", list(teamStats.keys()))
    compareTeam2 = st.selectbox("Compare Team 2", list(teamStats.keys()))

    comparisonData = pd.DataFrame({
        "Category": ["Attack", "Defense", "Strength"],
        teamFlags[compareTeam1] + " " + compareTeam1: [
            teamStats[compareTeam1]["attack"],
            teamStats[compareTeam1]["defense"],
            getTeamStrength(compareTeam1)
        ],
        teamFlags[compareTeam2] + " " + compareTeam2: [
            teamStats[compareTeam2]["attack"],
            teamStats[compareTeam2]["defense"],
            getTeamStrength(compareTeam2)
        ]
    })

    st.dataframe(comparisonData, use_container_width=True, hide_index=True)

elif page == "📋 Groups":
    st.header("📋 Group Stage Tables")

    if "groupStandings" not in st.session_state:
        st.info("Click **Run Simulator** in the sidebar first.")
    else:
        for groupName, standings in st.session_state.groupStandings.items():
            st.markdown(
                f"""
                <div style="
                    background-color:#061A5F;
                    color:white;
                    padding:14px;
                    border-radius:12px 12px 0px 0px;
                    font-size:22px;
                    font-weight:bold;
                    margin-top:25px;
                ">
                    {groupName}
                </div>
                """,
                unsafe_allow_html=True
            )

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