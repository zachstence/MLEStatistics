import CSVExtractUtils as csv

NCP_WINNER_STATS = [150, 1, 1, 1, 1]
NCP_LOSER_STATS = [50, 0, 0, 0, 1]

def is_ncp(game_stats):
    playerA1Stats = game_stats["teamA"][0][1:]
    playerA2Stats = game_stats["teamA"][1][1:]
    playerB1Stats = game_stats["teamB"][0][1:]
    playerB2Stats = game_stats["teamB"][1][1:]
    if playerA1Stats == NCP_WINNER_STATS and playerA2Stats == NCP_WINNER_STATS and \
        playerB1Stats == NCP_LOSER_STATS and playerB2Stats == NCP_LOSER_STATS:
        return True
    elif playerB1Stats == NCP_WINNER_STATS and playerB2Stats == NCP_WINNER_STATS and \
        playerA1Stats == NCP_LOSER_STATS and playerA2Stats == NCP_LOSER_STATS:
        return True
    else:
        return False

# {
#   week: 1,
#   game: 1,
#   match_id: 1,
#   matchup: (Aviators, Jets),
#   is_ncp: True/False
#   teamA: [
#       [player1 stats],
#       [player2 stats]
#   ],
#   teamB: [
#       [player1 stats],
#       [player2 stats]
#   ]
# }
def get_game_stats_from_lines(lines):
    week = csv.get_week(lines[0])
    game = csv.get_game(lines[0])
    match_id = csv.get_match_id(lines[0])
    teamA = csv.get_team(lines[0])
    teamB = csv.get_opponent(lines[0])

    # get first team's stats
    teamAStats = []
    for line in lines[:2]:
        teamAStats.append([
            csv.get_player(line),
            csv.get_score(line),
            csv.get_goals(line),
            csv.get_assists(line),
            csv.get_saves(line),
            csv.get_shots(line)
        ])
    # get second team's stats
    teamBStats = []
    for line in lines[2:]:
        teamBStats.append([
            csv.get_player(line),
            csv.get_score(line),
            csv.get_goals(line),
            csv.get_assists(line),
            csv.get_saves(line),
            csv.get_shots(line)
        ])
    
    game_stats = {
        "week": week,
        "game": game,
        "match_id": match_id,
        "matchup": (teamA, teamB),
        "teamA": teamAStats,
        "teamB": teamBStats
    }
    game_stats["is_ncp"] = is_ncp(game_stats)
    return game_stats  

def get_games_from_csv(csv_filepath):
    games = []
    with open(csv_filepath, 'r') as csv:
        lines = csv.readlines()
    for start in range(2, len(lines), 4):
        stop = start + 4
        game_lines = lines[start:stop]
        game_stats = get_game_stats_from_lines(game_lines)
        games.append(game_stats)
    return games
