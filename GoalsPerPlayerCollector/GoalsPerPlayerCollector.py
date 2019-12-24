import re
import pprint

LINE_REGEX = r"^(\d+),(\d+),(\d+),(.*?),(.*?),(.*?),(\d+),(\d+),(\d+),(\d+),(\d+)\n$"

def is_ncp(stats_line):
    return False

def get_goals(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    goals = int(m.group(8))
    return goals

def get_player(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    player = m.group(6)
    return player


def get_goals_per_player(csv_filepath):
    goals_per_player = {}
    with open(csv_filepath, 'r') as csv:
        lines = csv.readlines()
    for line in lines[2:]:
        player = get_player(line)
        goals = get_goals(line)
        if player in goals_per_player:
            goals_per_player[player] += goals
        else:
            goals_per_player[player] = goals
    return goals_per_player

if __name__ == "__main__":
    gpp = get_goals_per_player("GoalsPerPlayerCollector\\csv\\MLE Season 9 Stats - PREMIER.csv")
    pprint.pprint(gpp)