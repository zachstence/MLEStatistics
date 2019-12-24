import pprint
import GenUtils

def get_goals_per_player(csv_filepath, exclude_ncp):
    goals_per_player = {}
    games = GenUtils.get_games_from_csv(csv_filepath)
    for game in games:
        if game["is_ncp"] and exclude_ncp:
            continue
        teamAGoals = 0
        teamAPlayers = []
        for stats in game["teamA"]:
            teamAPlayers.append(stats[0])
            teamAGoals += stats[2]

        teamBGoals = 0
        teamBPlayers = []
        for player in game["teamB"]:
            teamBPlayers.append(stats[0])
            teamBGoals += stats[2]
        
        for player in teamAPlayers:
            if player in goals_per_player:
                goals_per_player[player][0] += teamAGoals
                goals_per_player[player][1] += teamBGoals
            else:
                goals_per_player[player] = [teamAGoals, teamBGoals]

        for player in teamBPlayers:
            if player in goals_per_player:
                goals_per_player[player][0] += teamBGoals
                goals_per_player[player][1] += teamAGoals
            else:
                goals_per_player[player][0] = [teamBGoals, teamAGoals]
    return goals_per_player

def write_goals_per_player_to_csv(output_filepath, goals_per_player):
    with open(output_filepath, 'w+') as out:
        out.write("Player,Goals For,Goals Against\n")
        for player in goals_per_player:
            out.write("{},{},{}\n".format(player, goals_per_player[player][0], goals_per_player[player][1]))

if __name__ == "__main__":
    gpp = get_goals_per_player(r"csv\MLE Season 9 Stats - PREMIER.csv", True)
    write_goals_per_player_to_csv("S9 Premier GPP (no NCPs).csv", gpp)
