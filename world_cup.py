import random

groups = {
    "Group A": ["Mexico", "South Korea", "South Africa", "Czechia"],
    "Group B": ["Canada", "Switzerland", "Qatar", "Bosnia and Herzegovina"],
    "Group C": ["Brazil", "Morocco", "Scotland", "Haiti"],
    "Group D": ["United States", "Australia", "Paraguay", "Turkey"],
    "Group E": ["Germany", "Ecuador", "Ivory Coast", "Curacao"],
    "Group F": ["Netherlands", "Japan", "Tunisia", "Sweden"],
    "Group G": ["Belgium", "Iran", "Egypt", "New Zealand"],
    "Group H": ["Spain", "Uruguay", "Saudi Arabia", "Cape Verde"],
    "Group I": ["France", "Senegal", "Norway", "Iraq"],
    "Group J": ["Argentina", "Austria", "Algeria", "Jordan"],
    "Group K": ["Portugal", "Colombia", "Uzbekistan", "DR Congo"],
    "Group L": ["England", "Croatia", "Panama", "Ghana"]
}

teamStats = {
    "Mexico": {"attack": 81, "defense": 81},
    "South Korea": {"attack": 80, "defense": 81},
    "South Africa": {"attack": 69, "defense": 71},
    "Czechia": {"attack": 76, "defense": 78},

    "Canada": {"attack": 80, "defense": 76},
    "Switzerland": {"attack": 80, "defense": 85},
    "Qatar": {"attack": 69, "defense": 68},
    "Bosnia and Herzegovina": {"attack": 73, "defense": 73},

    "Brazil": {"attack": 95, "defense": 86},
    "Morocco": {"attack": 81, "defense": 89},
    "Scotland": {"attack": 76, "defense": 78},
    "Haiti": {"attack": 64, "defense": 65},

    "United States": {"attack": 82, "defense": 80},
    "Australia": {"attack": 75, "defense": 77},
    "Paraguay": {"attack": 77, "defense": 79},
    "Turkey": {"attack": 83, "defense": 79},

    "Germany": {"attack": 88, "defense": 90},
    "Ecuador": {"attack": 79, "defense": 83},
    "Ivory Coast": {"attack": 79, "defense": 77},
    "Curacao": {"attack": 66, "defense": 65},

    "Netherlands": {"attack": 87, "defense": 89},
    "Japan": {"attack": 83, "defense": 84},
    "Tunisia": {"attack": 74, "defense": 76},
    "Sweden": {"attack": 78, "defense": 80},

    "Belgium": {"attack": 85, "defense": 82},
    "Iran": {"attack": 76, "defense": 80},
    "Egypt": {"attack": 80, "defense": 77},
    "New Zealand": {"attack": 67, "defense": 69},

    "Spain": {"attack": 92, "defense": 93},
    "Uruguay": {"attack": 84, "defense": 88},
    "Saudi Arabia": {"attack": 72, "defense": 73},
    "Cape Verde": {"attack": 70, "defense": 72},

    "France": {"attack": 94, "defense": 90},
    "Senegal": {"attack": 81, "defense": 83},
    "Norway": {"attack": 84, "defense": 80},
    "Iraq": {"attack": 66, "defense": 68},

    "Argentina": {"attack": 91, "defense": 90},
    "Austria": {"attack": 82, "defense": 83},
    "Algeria": {"attack": 77, "defense": 76},
    "Jordan": {"attack": 66, "defense": 67},

    "Portugal": {"attack": 90, "defense": 86},
    "Colombia": {"attack": 85, "defense": 86},
    "Uzbekistan": {"attack": 70, "defense": 72},
    "DR Congo": {"attack": 70, "defense": 71},

    "England": {"attack": 90, "defense": 89},
    "Croatia": {"attack": 84, "defense": 86},
    "Panama": {"attack": 70, "defense": 71},
    "Ghana": {"attack": 77, "defense": 76}
}

hostTeams = ["United States", "Mexico", "Canada"]

upsetWins = {}


def getTeamStrength(team):
    return teamStats[team]["attack"] + teamStats[team]["defense"]


def playMatch(team1, team2):
    team1Attack = teamStats[team1]["attack"]
    team1Defense = teamStats[team1]["defense"]

    team2Attack = teamStats[team2]["attack"]
    team2Defense = teamStats[team2]["defense"]

    if team1 in hostTeams:
        team1Attack += 2
        team1Defense += 1

    if team2 in hostTeams:
        team2Attack += 2
        team2Defense += 1

    team1Goals = 0
    team2Goals = 0

    team1Chance = 0.15 + ((team1Attack - team2Defense) * 0.01)
    team2Chance = 0.15 + ((team2Attack - team1Defense) * 0.01)

    team1Chance = max(0.05, min(team1Chance, 0.50))
    team2Chance = max(0.05, min(team2Chance, 0.50))

    team1Attacks = int(team1Attack / 12)
    team2Attacks = int(team2Attack / 12)

    for i in range(team1Attacks):
        if random.random() < team1Chance:
            team1Goals += 1

    for i in range(team2Attacks):
        if random.random() < team2Chance:
            team2Goals += 1

    return team1Goals, team2Goals


def playGroup(groupName, teams):
    table = {}

    for team in teams:
        table[team] = {
            "points": 0,
            "goalsFor": 0,
            "goalsAgainst": 0,
            "goalDifference": 0
        }

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            team1 = teams[i]
            team2 = teams[j]

            team1Goals, team2Goals = playMatch(team1, team2)

            table[team1]["goalsFor"] += team1Goals
            table[team1]["goalsAgainst"] += team2Goals

            table[team2]["goalsFor"] += team2Goals
            table[team2]["goalsAgainst"] += team1Goals

            if team1Goals > team2Goals:
                table[team1]["points"] += 3
            elif team2Goals > team1Goals:
                table[team2]["points"] += 3
            else:
                table[team1]["points"] += 1
                table[team2]["points"] += 1

    for team in teams:
        table[team]["goalDifference"] = (
            table[team]["goalsFor"] - table[team]["goalsAgainst"]
        )

    standings = sorted(
        table.items(),
        key=lambda item: (
            item[1]["points"],
            item[1]["goalDifference"],
            item[1]["goalsFor"]
        ),
        reverse=True
    )

    return standings


def createRoundOf32():
    firstPlaceTeams = []
    otherQualifiedTeams = []
    thirdPlaceTeams = []
    groupStandings = {}

    for groupName, teams in groups.items():
        standings = playGroup(groupName, teams)

        groupStandings[groupName] = standings

        firstPlace = standings[0]
        secondPlace = standings[1]
        thirdPlace = standings[2]

        firstPlaceTeams.append(firstPlace[0])
        otherQualifiedTeams.append(secondPlace[0])
        thirdPlaceTeams.append(thirdPlace)

    thirdPlaceTeams = sorted(
        thirdPlaceTeams,
        key=lambda item: (
            item[1]["points"],
            item[1]["goalDifference"],
            item[1]["goalsFor"]
        ),
        reverse=True
    )

    bestThirdPlaceTeams = thirdPlaceTeams[:8]

    for team, stats in bestThirdPlaceTeams:
        otherQualifiedTeams.append(team)

    random.shuffle(firstPlaceTeams)
    random.shuffle(otherQualifiedTeams)

    roundOf32 = []

    for i in range(12):
        roundOf32.append(firstPlaceTeams[i])
        roundOf32.append(otherQualifiedTeams[i])

    remainingTeams = otherQualifiedTeams[12:]

    for i in range(0, len(remainingTeams), 2):
        roundOf32.append(remainingTeams[i])
        roundOf32.append(remainingTeams[i + 1])

    return roundOf32, groupStandings


def playKnockoutRound(teams, roundName):
    winners = []
    matchResults = []

    for i in range(0, len(teams), 2):
        team1 = teams[i]
        team2 = teams[i + 1]

        team1Goals, team2Goals = playMatch(team1, team2)

        if team1Goals == team2Goals:
            penaltyWinner = random.choice([team1, team2])
            winner = penaltyWinner

            matchResults.append(
                team1 + " vs " + team2 +
                " : " + str(team1Goals) + " - " + str(team2Goals) +
                " (" + penaltyWinner + " won on penalties)"
            )

        else:
            if team1Goals > team2Goals:
                winner = team1
            else:
                winner = team2

            matchResults.append(
                team1 + " " + str(team1Goals) +
                " - " +
                str(team2Goals) + " " + team2
            )

        winners.append(winner)

    return winners, matchResults

def resetUpsets():
    global upsetWins
    upsetWins = {}

def simulateTournamentProgression():
    global upsetWins
    upsetWins = {}

    progression = {}

    for team in teamStats.keys():
        progression[team] = "Group Stage"

    roundOf32, _ = createRoundOf32()

    for team in roundOf32:
        progression[team] = "Round of 32"

    roundOf16, round32Matches = playKnockoutRound(roundOf32, "Round of 32")
    for team in roundOf16:
        progression[team] = "Round of 16"

    quarterFinals, round16Matches = playKnockoutRound(roundOf16, "Round of 16")
    for team in quarterFinals:
        progression[team] = "Quarterfinals"

    semiFinals, quarterFinalMatches = playKnockoutRound(quarterFinals, "Quarterfinals")
    for team in semiFinals:
        progression[team] = "Semifinals"

    finalTeams, semiFinalMatches = playKnockoutRound(semiFinals, "Semifinals")
    for team in finalTeams:
        progression[team] = "Final"

    championList, finalMatch = playKnockoutRound(finalTeams, "Final")
    champion = championList[0]

    progression[champion] = "Champion"

    return progression

def simulateTournament():
    global upsetWins
    upsetWins = {}

    roundOf32, _ = createRoundOf32()

    roundOf16, round32Matches = playKnockoutRound(roundOf32, "Round of 32")
    quarterFinals, round16Matches = playKnockoutRound(roundOf16, "Round of 16")
    semiFinals, quarterFinalMatches = playKnockoutRound(quarterFinals, "Quarterfinals")
    finalTeams, semiFinalMatches = playKnockoutRound(semiFinals, "Semifinals")
    championList, finalMatch = playKnockoutRound(finalTeams, "Final")

    return championList[0]