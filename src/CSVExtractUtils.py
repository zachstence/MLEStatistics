import re

LINE_REGEX = r"(\d+),(\d+),(\d+),(.*?),(.*?),(.*?),(\d+),(\d+),(\d+),(\d+),(\d+)"

def get_week(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    week = int(m.group(1))
    return week

def get_game(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    game = int(m.group(2))
    return game

def get_match_id(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    match_id = int(m.group(3))
    return match_id

def get_team(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    team = m.group(4)
    return team

def get_opponent(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    team = m.group(5)
    return team

def get_player(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    player = m.group(6)
    return player

def get_score(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    score = int(m.group(7))
    return score

def get_goals(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    goals = int(m.group(8))
    return goals

def get_assists(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    assists = int(m.group(9))
    return assists

def get_saves(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    saves = int(m.group(10))
    return saves

def get_shots(stats_line):
    m = re.search(LINE_REGEX, stats_line)
    if m == None:
        return 0
    shots = int(m.group(11))
    return shots