import re
import pprint

TEAMS = [
    "Aviators",
    "Bears",
    "Blizzard",
    "Bulls",
    "Comets",
    "Demolition",
    "Dodgers",
    "Ducks",
    "Elite",
    "Flames",
    "Foxes",
    "Hawks",
    "Hurricanes",
    "Jets",
    "Lightning",
    "Pandas",
    "Pirates",
    "Puffins",
    "Rhinos",
    "Sharks",
    "Spartans",
    "Tigers",
    "Warriors",
    "Wolves"
]

NUM_WEEKS = 10
NUM_GAMES = 5
STATS_REGEX = r"(^.*?),\d*,\d*,(\d+),(\d+),(\d+),(\d+),(\d+),\d*,,"
CSV_PREFIX = "csv/MLD_Season_5 - "

def get_score(score_line):
    """ get_score(score_line)
    Extracts the score from a line in CSV format using the format in the spreadsheet.
    """
    m = re.search(STATS_REGEX, score_line)
    if m == None:
        return 0
    score = int(m.group(2))
    return score

def get_scores_for_week(week):
    """ get_scores_for_week(week)
    Extracts the points each team had for/against them in their game that week.
    Returns a dictionary where the keys are team names and the corresponding value is a tuple containing the
    number of points they scored and the number of points scored against them in their match that week.
    {
        "team1": (points_for, points_against),
        "team2": (points_for, points_against),
        etc...
    }
    """
    game_one_scores = {}
    for team in TEAMS:
        with open(CSV_PREFIX + team + ".csv", 'r') as f:
            lines = f.readlines()
        start_line = 31*(week - 1) + 1
        end_line = start_line + 3
        player_score_lines = lines[start_line:end_line]
        opponent_score_line = lines[end_line]
        team_score_for = 0
        for score_line in player_score_lines:
            team_score_for += get_score(score_line)
        team_score_against = get_score(opponent_score_line)
        game_one_scores[team] = (team_score_for, team_score_against)
    return game_one_scores

def is_team_in_schedule(schedule, team):
    """ is_team_in_schedule(schedule, team)
    Returns true if the specified team is already in the schedule (list of tuples containing matchups). This is used
    just to make sure matchups aren't duplicated.
    """
    for matchup in schedule:
        teamA = matchup[0]
        teamB = matchup[1]
        if team == teamA or team == teamB:
            return True
    return False

def find_schedule_for_week(week):
    """ find_schedule_for_week(week)
    Looks through each team's spreadsheet and finds the corresponding opponent team for each match based on their score and their
    opponent's score (in a given week).
    Returns a list of tuples containing the matchups for that week.
    [
        (team1, team2),
        (team3, team4),
        etc...
    ]
    """
    schedule = []
    scores = get_scores_for_week(week)
    for teamA in TEAMS:
        teamA_for = scores[teamA][0]
        teamA_against = scores[teamA][1]
        for teamB in TEAMS:
            teamB_for = scores[teamB][0]
            teamB_against = scores[teamB][1]
            if teamA_for == teamB_against and teamB_for == teamA_against and not is_team_in_schedule(schedule, teamB):
                schedule.append((teamA, teamB))
                break
    return schedule

def find_schedule():
    """ find_Schedule()
    Finds the schedule for each week and places them in a list.
    [
        [Week 1 Schedule],
        [Week 2 Schedule],
        etc...
    ]
    """
    schedule = []
    for week in range(1, NUM_WEEKS + 1):
        schedule.append(find_schedule_for_week(week))
    return schedule

def get_player_stats(stats_line):
    """ get_player_stats(stats_line)
    Extracts the player's name, score, goals, assists, saves, and shots from a line from the spreadsheet.
    Returns a list containing the stats: [name, score, goals, assists, saves, shots]
    """
    m = re.search(STATS_REGEX, stats_line)
    if m == None:
        return None
    stats = []
    for i in range(1, 6 + 1):
        stats.append(m.group(i))
    return stats

def get_player_stats_for_game(team, week, game):
    """ get_player_stats_for_game(team, week, game)
    Extracts a player's stats on a specific team during a specific game in a specific week.
    Returns a list containing their stats: [name, score, goals, assists, saves, shots]
    """
    with open(CSV_PREFIX + team + ".csv", 'r') as f:
        lines = f.readlines()
    start_line = 31*(week - 1) + 5*(game - 1) + 1
    end_line = start_line + 3
    player_lines = lines[start_line:end_line]
    game_stats = []
    for line in player_lines:
        stats = get_player_stats(line)
        if stats != None:
            game_stats.append(stats)
    return game_stats

# {
#   week: 1,
#   game: 1,
#   match_id: 1,
#   matchup: (Aviators, Jets),
#   teamA: [
#       [player1 stats],
#       [player2 stats]
#   ],
#   teamB: [
#       [player1 stats],
#       [player2 stats]
#   ]
# }
def get_game_stats(matchup, week, game, match_id):
    """ get_game_stats(matchup, week, game, match_id)
    Gets the stats for players that played a game.
    Returns a dictionary containing various fields used for creating a spreadsheet with the stats of all games:
    {
        week: 1,
        game: 1,
        match_id: 1,
        matchup: (Aviators, Jets),
        teamA: [
            [player1 stats],
            [player2 stats]
        ],
        teamB: [
            [player1 stats],
            [player2 stats]
        ]
    }
    """
    teamA = matchup[0]
    teamB = matchup[1]
    teamAStats = get_player_stats_for_game(teamA, week, game)
    teamBStats = get_player_stats_for_game(teamB, week, game)
    return {
        'week': week,
        'game': game,
        'match_id': match_id,
        'matchup': matchup,
        'teamA': teamAStats,
        'teamB': teamBStats
    }

def get_match_stats(matchup, week, match_id):
    """ get_match_stats(mathup, week, match_id)
    Gets the game stats for all games in a match and returns them in a list.
    [
        {game 1 stats},
        {game 2 stats},
        {game 3 stats},
        {game 4 stats},
        {game 5 stats}
    ]
    """
    stats = []
    for game in range(1, 5 + 1):
        game_stats = get_game_stats(matchup, week, game, match_id)
        stats.append(game_stats)
    return stats

def match_stats_to_csv_string(match_stats):
    """ match_stats_to_csv_string(match_status)
    Converts a match stats into a string to write to a CSV file.
    """
    out = ""
    for game_stats in match_stats:
        out += "{},{},{},{},{},{},{},{},{},{},{}\n".format(
            game_stats['week'],
            game_stats['game'],
            game_stats['match_id'],
            game_stats['matchup'][0],
            game_stats['matchup'][1],
            game_stats['teamA'][0][0],
            game_stats['teamA'][0][1],
            game_stats['teamA'][0][2],
            game_stats['teamA'][0][3],
            game_stats['teamA'][0][4],
            game_stats['teamA'][0][5],
        )
        out += "{},{},{},{},{},{},{},{},{},{},{}\n".format(
            game_stats['week'],
            game_stats['game'],
            game_stats['match_id'],
            game_stats['matchup'][0],
            game_stats['matchup'][1],
            game_stats['teamA'][1][0],
            game_stats['teamA'][1][1],
            game_stats['teamA'][1][2],
            game_stats['teamA'][1][3],
            game_stats['teamA'][1][4],
            game_stats['teamA'][1][5],
        )
        out += "{},{},{},{},{},{},{},{},{},{},{}\n".format(
            game_stats['week'],
            game_stats['game'],
            game_stats['match_id'],
            game_stats['matchup'][1],
            game_stats['matchup'][0],
            game_stats['teamB'][0][0],
            game_stats['teamB'][0][1],
            game_stats['teamB'][0][2],
            game_stats['teamB'][0][3],
            game_stats['teamB'][0][4],
            game_stats['teamB'][0][5],
        )
        out += "{},{},{},{},{},{},{},{},{},{},{}\n".format(
            game_stats['week'],
            game_stats['game'],
            game_stats['match_id'],
            game_stats['matchup'][1],
            game_stats['matchup'][0],
            game_stats['teamB'][1][0],
            game_stats['teamB'][1][1],
            game_stats['teamB'][1][2],
            game_stats['teamB'][1][3],
            game_stats['teamB'][1][4],
            game_stats['teamB'][1][5],
        )
    return out

if __name__ == "__main__":
    matchups = find_schedule()
    match_id = 1
    with open('stats.csv', 'w+') as out:
        for week, week_matchups in enumerate(matchups):
            for matchup in week_matchups:
                stats = get_match_stats(matchup, week + 1, match_id)
                s = match_stats_to_csv_string(stats)
                out.write(s)
                match_id += 1
