import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
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
    background-color:#0057B8;
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
        ["🏆 Simulator", "📊 Probabilities", "⚽ Teams", "📋 Groups", "Your Predictions"]
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

    roundOf16, roundOf32Losers, round32Matches = playKnockoutRound(roundOf32, "Round of 32")
    quarterFinals, round16Losers, round16Matches = playKnockoutRound(roundOf16, "Round of 16")
    semiFinals, quarterFinalLosers, quarterFinalMatches = playKnockoutRound(quarterFinals, "Quarterfinals")
    finalTeams, semiFinalLosers, semiFinalMatches = playKnockoutRound(semiFinals, "Semifinals")

    thirdPlaceList, thirdPlaceLosers, thirdPlaceMatch = playKnockoutRound(semiFinalLosers, "Third Place Match")

    championList, finalLosers, finalMatch = playKnockoutRound(finalTeams, "Final")

    st.session_state.groupStandings = groupStandings
    st.session_state.round32Matches = round32Matches
    st.session_state.round16Matches = round16Matches
    st.session_state.quarterFinalMatches = quarterFinalMatches
    st.session_state.semiFinalMatches = semiFinalMatches
    st.session_state.finalMatch = finalMatch

    st.session_state.thirdPlaceMatch = thirdPlaceMatch
    st.session_state.thirdPlaceWinner = thirdPlaceList[0]

    st.session_state.champion = championList[0]

if page == "🏆 Simulator":
    st.header("🧩 Tournament Bracket")

    if "champion" not in st.session_state:
        st.info("Click **Run Simulator** in the sidebar first.")
    else:
        champion = st.session_state.champion
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#D4AF37,#D4AF37);
            padding:28px;
            border-radius:22px;
            text-align:center;
            color:#111827;
            font-weight:bold;
            font-size:34px;
            box-shadow:0 8px 25px rgba(0,0,0,.30);
            margin-bottom:35px;
        ">
            WORLD CUP CHAMPION<br>
            <span style="font-size:42px;">
                {teamFlags[champion]} {champion}
            </span>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Teams", "48")

        with col2:
            st.metric("Knockout Matches", "32")

        with col3:
            st.metric("Champion", teamFlags[champion] + " " + champion)

        with col4:
            st.metric("Simulations", simulationCount)

        def matchCard(match):
            return f"""
            <div style="
                background:#061A5F;
                color:white;
                width:250px;
                min-height:55px;
                padding:14px;
                border-radius:14px;
                margin-bottom:22px;
                box-shadow:0px 4px 12px rgba(0,0,0,0.35);
                border-left:7px solid #ff7a00;
                font-family:Arial;
                font-size:15px;
                line-height:1.5;
                height:88px;
            ">
                {addFlagsToMatch(match)}
            </div>
            """

        def bracketColumn(title, matches, marginTop):
            cards = ""

            for match in matches:
                cards += matchCard(match)

            return f"""
            <div style="
                min-width:270px;
                margin-top:{marginTop}px;
            ">
                <h2 style="
                    color:white;
                    text-align:center;
                    font-family:Arial;
                    margin-bottom:20px;
                ">
                    {title}
                </h2>
                {cards}
            </div>
            """
        
        def connectorLines():
            lines = ""

            cardHeight = 88
            cardGap = 22
            columnGap = 55
            cardWidth = 270

            startX = 35 + cardWidth
            startY = 95

            roundSizes = [16, 8, 4, 2]
            marginTops = [0, 65, 145, 245]

            for roundIndex in range(len(roundSizes)):
                games = roundSizes[roundIndex]

                x1 = startX + roundIndex * (cardWidth + columnGap)
                x2 = x1 + columnGap

                yOffset = marginTops[roundIndex]

                for i in range(0, games, 2):
                    y1 = startY + yOffset + i * (cardHeight + cardGap) + cardHeight / 2
                    y2 = startY + yOffset + (i + 1) * (cardHeight + cardGap) + cardHeight / 2
                    middleY = (y1 + y2) / 2

                    lines += f"""
                    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y1}" stroke="white" stroke-width="3"/>
                    <line x1="{x1}" y1="{y2}" x2="{x2}" y2="{y2}" stroke="white" stroke-width="3"/>
                    <line x1="{x2}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="white" stroke-width="3"/>
                    <line x1="{x2}" y1="{middleY}" x2="{x2 + 55}" y2="{middleY}" stroke="white" stroke-width="3"/>
                    """

                return lines

        bracketHTML = f"""
        <div style="
            position:relative;
            background:linear-gradient(135deg,#003BDB,#315BFF);
            padding:35px;
            border-radius:24px;
            overflow-x:auto;
            min-height:850px;
            min-width:1600px;
        ">
            <div style="
                display:flex;
                gap:90px;
                align-items:flex-start;
            ">
                {bracketColumn("R32", st.session_state.round32Matches, 0)}  
                {bracketColumn("R16", st.session_state.round16Matches, 65)}
                {bracketColumn("QF", st.session_state.quarterFinalMatches, 180)}
                {bracketColumn("SF", st.session_state.semiFinalMatches, 320)}
                {bracketColumn("3RD PLACE", st.session_state.thirdPlaceMatch, 480)}
                {bracketColumn("FINAL", st.session_state.finalMatch, 560)}
            </div>
        </div>
        """

        components.html(bracketHTML, height=950, scrolling=True)


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

elif page == "Your Predictions":
    st.header("Build your own World Cup Bracket")

    def pickGroupStage():
        groupStandings = {}
        firstPlaceTeams = []
        secondPlaceTeams = []
        thirdPlaceTeams = []

        for groupName, groupTeams in groups.items():
            st.subheader(groupName)

            first = st.selectbox(
                groupName + " - 1st Place",
                groupTeams,
                key=groupName + "_first"
            )

            secondOptions = [team for team in groupTeams if team != first]

            second = st.selectbox(
                groupName + " - 2nd Place",
                secondOptions,
                key=groupName + "_second"
            )

            thirdOptions = [
                team for team in groupTeams
                if team != first and team != second
            ]

            third = st.selectbox(
                groupName + " - 3rd Place",
                thirdOptions,
                key=groupName + "_third"
            )

            firstPlaceTeams.append(first)
            secondPlaceTeams.append(second)

            thirdPlaceTeams.append({
                "team": third,
                "group": groupName
            })

            groupStandings[groupName] = [first, second, third]

        return firstPlaceTeams, secondPlaceTeams, thirdPlaceTeams, groupStandings
    
    firstPlaceTeams, secondPlaceTeams, thirdPlaceTeams, userGroupStandings = pickGroupStage()

    st.header("Best 8 Third Placed Teams")

    thirdPlaceTeams = [item["team"] for item in thirdPlaceTeams]

    selectedThirdPlaceTeams = st.multiselect(
        "Select the 8 best third placed teams to advance to the knockout stage",
        thirdPlaceTeams,
        default=thirdPlaceTeams[:8]
    )

    if len(selectedThirdPlaceTeams) != 8:
        st.warning("Please select exactly 8 third placed teams.")
    else:
        predictionRoundOf32 = []

        otherQualifiedTeams = secondPlaceTeams + selectedThirdPlaceTeams

        random.shuffle(firstPlaceTeams)
        random.shuffle(otherQualifiedTeams)

        for i in range(12):
            predictionRoundOf32.append(firstPlaceTeams[i])
            predictionRoundOf32.append(otherQualifiedTeams[i])

        remainingTeams = otherQualifiedTeams[12:]

        for i in range(0, len(remainingTeams), 2):
            predictionRoundOf32.append(remainingTeams[i])
            predictionRoundOf32.append(remainingTeams[i + 1])

        def userPickRound(teams, roundName):
            st.subheader(roundName)

            winners = []

            for i in range(0, len(teams), 2):
                team1 = teams[i]
                team2 = teams[i + 1]

                winner = st.radio(
                    teamFlags[team1] + " " + team1 + " vs " + teamFlags[team2] + " " + team2,
                    [team1, team2],
                    key=roundName + team1 + team2
                )

                winners.append(winner)

            return winners
        
        roundOf16 = userPickRound(predictionRoundOf32, "Round of 32")
        quarterFinals = userPickRound(roundOf16, "Round of 16")
        semiFinals = userPickRound(quarterFinals, "Quarterfinals")
        finalTeams = userPickRound(semiFinals, "Semifinals")
        championList = userPickRound(finalTeams, "Final")

        champion = championList[0]

        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#D4AF37,#D4AF37);
            padding:28px;
            border-radius:22px;
            text-align:center;
            color:#111827;
            font-weight:bold;
            font-size:34px;
            box-shadow:0 8px 25px rgba(0,0,0,.30);
            margin-top:30px;
        ">
            YOUR PREDICTED CHAMPION<br>
            <span style="font-size:42px;">
                {teamFlags[champion]} {champion}
            </span>
        </div>
        """, unsafe_allow_html=True)