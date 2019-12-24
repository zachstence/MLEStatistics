import pprint
import GenUtils

def get_goals_per_player(csv_filepath, exclude_ncp):
    goals_per_player = {}
    games = GenUtils.get_games_from_csv(csv_filepath)
    for game in games:
        if game["is_ncp"] and exclude_ncp:
            continue
        for stats in game["teamA"] + game["teamB"]:
            player = stats[0]
            goals = stats[2]
            if player in goals_per_player:
                goals_per_player[player] += goals
            else:
                goals_per_player[player] = goals
    return goals_per_player

def write_goals_per_player_to_csv(output_filepath, goals_per_player):
    with open(output_filepath, 'w+') as out:
        out.write("Player,Goals\n")
        for player in goals_per_player:
            out.write("{},{}\n".format(player, goals_per_player[player]))

if __name__ == "__main__":
    gpp = get_goals_per_player(r"csv\MLE Season 9 Stats - PREMIER.csv", True)
    write_goals_per_player_to_csv("S9 Premier GPP.csv", gpp)
