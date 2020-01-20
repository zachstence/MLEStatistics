import re

LINE_REGEX = r"(\d+),(\d+),(\d+),(.*?),(.*?),(.*?),(\d*),(\d*),(\d*),(\d*),(\d*)"

def get_week(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return -1
    week = int(m.group(1))
    return week

def get_game(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return -1
    game = int(m.group(2))
    return game

def get_match_id(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return -1
    match_id = int(m.group(3))
    return match_id

def get_team(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return ""
    team = m.group(4)
    return team

def get_opponent(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return ""
    team = m.group(5)
    return team

def get_player(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        print(stats_line)
        return ""
    player = m.group(6)
    return player

def get_score(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    score = m.group(7)
    if score == "":
        return 0
    else:
        return int(score)

def get_goals(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    goals = m.group(8)
    if goals == "":
        return 0
    else:
        return int(goals)

def get_assists(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    assists = m.group(9)
    if assists == "":
        return 0
    else:
        return int(assists)

def get_saves(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    saves = m.group(10)
    if saves == "":
        return 0
    else:
        return int(saves)

def get_shots(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    shots = m.group(11)
    if shots == "":
        return 0
    else:
        return int(shots)