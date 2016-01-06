import nflgame
import MySQLdb
import MySQLdb.cursors
import datetime
import os
import argparse
import gamestats_functions as f
import config as c

# Location of text file used to translate nflgame player IDs to CBS player IDs
lookupfile = os.path.dirname(os.path.abspath(__file__))+"/playerids.txt"

# Directory where phpffl  game statistic files should be placed.
try:
    output_dir = c.output_dir
except AttributeError:
    output_dir = os.path.dirname(os.path.abspath(__file__))+'/gamestats'

nflids = dict
def main():
    global nflids
    cur_year, cur_week = nflgame.live.current_year_and_week()
    phase = nflgame.live._cur_season_phase

    if args.y == "0": year = str(cur_year)
    else: year = args.y
    if args.w == "0": week = str(cur_week)
    else: week = args.w
    phase = args.p

    games = nflgame.games(int(year), week=int(week), kind=phase)

    print "Week: %s Year: %s Phase: %s" %(str(week),str(year),phase)

    nflids = load_nflids()

    for game in games:
        print str(game)+" "+str(game.time)
        one_game(game)


def one_game(game):
    # Get game dict and print
    gamedict = {}
    gamedict["game"] = {}
    gamedict["players"] = {}

    #  game = nflgame.one(year,week,str(home),str(away))
    if (game.playing() or game.game_over()):
        FillGameInfo(game, gamedict)
        InitTeamPlayers(gamedict)
        StatsFromGame(game, gamedict)
        StatsFromPlayers(game.players, gamedict)
        StatsFromPlays(game.drives.plays(), gamedict)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        outfile = output_dir+"/"+gamedict["game"]["ID"]
        text = print_game(gamedict)
        with open(outfile, "w") as f:
            f.write(text)

    else:
        print "Game is in pregame, starting soon."


# Fill a playersdict with stats
def StatsFromPlayers(players, gamedict):
  for player in players:
    phpffl_id = GetPhpfflID(player.playerid)
    gamedict["players"][phpffl_id] = {}
    gamedict["players"][phpffl_id]["name"] = player.name # For debugging

    for stat in player.stats:
      phpffl_stat = f.get_key(stat)
      if gamedict["players"][phpffl_id].get(phpffl_stat) is None:
        gamedict["players"][phpffl_id][phpffl_stat] = player.stats[stat]
      else:
        gamedict["players"][phpffl_id][phpffl_stat] += player.stats[stat]

def StatsFromPlays(plays, gamedict):
  for play in plays:
    for event in play.events:
      for stat in event:
        phpffl_stat = f.get_key(stat)
        # Stats for team players
        if stat == "passing_sk": # Switched to passing_sk_yds to catch "Team Sacks"
          f.team_sack(event,gamedict)
        # if stat == "defense_sk":
        #  f.team_sack(event,gamedict)
        if stat == "fumbles_lost":
          f.team_fumble(event,gamedict)
        if stat == "defense_int":
          f.team_defint(event,gamedict)
        if stat == "defense_tds":
          f.team_def_td(event,gamedict)
        if stat == "defense_safe":
          f.team_def_saf(event,gamedict)
        if stat == "puntret_tds" or stat == "kickret_tds":
          f.team_st_td(event,gamedict)
        # scenario where def recovers fumble, fumbles again and gets a TD
        if stat == "fumbles_rec_tds" and event["team"] != play.team:
          f.team_def_td(event,gamedict)

        # Stats for human players
        if stat == "kicking_fgm_yds": # Need yardages for each field goal
          phpffl_id = GetPhpfflID(event["playerid"])
          if gamedict["players"].get(phpffl_id) is None:  # new player, initialize
            gamedict["players"][phpffl_id] = {}
            #gamedict["players"][phpffl_id]["name"] = player.name # For debugging
          f.player_field_goal(phpffl_id, event, gamedict)
        if (stat == "kickret_yds" or stat == "puntret_yds") and play.note != "FUMBLE":
          phpffl_id = GetPhpfflID(event["playerid"])
          f.AddPlayerStat(phpffl_id, stat, event, gamedict)
        if (stat == "kicking_fgmissed"):
          phpffl_id = GetPhpfflID(event["playerid"])
          f.AddPlayerStat(phpffl_id, stat, event, gamedict)
        if (stat == "rushing_tds") or (stat == "receiving_tds"):
          phpffl_id = GetPhpfflID(event["playerid"])
          f.AddPlayerTD(phpffl_id, stat, event, gamedict)

# Apparently this is not used
def TeamStatsFromPlays(plays, gamedict):
  home = gamedict["game"]["home"]
  away = gamedict["game"]["away"]

  home_rushing_yds = 0
  home_passing_yds = 0
  home_total_yds = 0
  home_score = 0
  away_rushing_yds = 0
  away_passing_yds = 0
  away_total_yds = 0
  away_score = 0

  for play in plays:
    for event in play.events:
      for stat in event:
        if stat == "passing_yds" and event["team"] == home:
          home_passing_yds += event[stat]
        if stat == "passing_yds" and event["team"] == away:
          away_passing_yds += event[stat]
        if stat == "rushing_yds" and event["team"] == home:
          home_rushing_yds += event[stat]
        if stat == "rushing_yds" and event["team"] == away:
          away_rushing_yds += event[stat]
        print stat

def DiffGameStats(oldgame, game, gamedict):
  home = gamedict["game"]["home"]
  away = gamedict["game"]["away"]
  # Team offensive line - Home
  gamedict["players"]["TOL_"+home]["Tm RU"] = game.stats_home.rushing_yds - oldgame.stats_home.rushing_yds
  gamedict["players"]["TOL_"+home]["Tm PS"] = game.stats_home.passing_yds - oldgame.stats_home.passing_yds
  # Team offensive line - Away
  gamedict["players"]["TOL_"+away]["Tm RU"] = game.stats_away.rushing_yds - oldgame.stats_away.rushing_yds
  gamedict["players"]["TOL_"+away]["Tm PS"] = game.stats_away.passing_yds - oldgame.stats_away.passing_yds
  # Team defense - Home
  gamedict["players"]["TDEF_"+home]["PA"] = game.score_away - oldgame.score_away
  gamedict["players"]["TDEF_"+home]["YA"] = game.stats_away.total_yds - oldgame.stats_away.total_yds
  # Team defense - Away
  gamedict["players"]["TDEF_"+away]["PA"] = game.score_home - oldgame.score_home
  gamedict["players"]["TDEF_"+away]["YA"] = game.stats_home.total_yds - oldgame.stats_home.total_yds
  # Def/ST Home
  gamedict["players"]["TDEFST_"+away]["PA"] = game.score_home - oldgame.score_home
  gamedict["players"]["TDEFST_"+away]["YA"] = game.stats_away.total_yds - oldgame.stats_away.total_yds
  # Special teams - Home
  # Special teams - Away


def StatsFromGame(game, gamedict):
  home = gamedict["game"]["home"]
  away = gamedict["game"]["away"]
  # Team offensive line - Home
  gamedict["players"]["TOL_"+home]["Tm RU"] = game.stats_home.rushing_yds
  gamedict["players"]["TOL_"+home]["Tm PS"] = game.stats_home.passing_yds
  # Team offensive line - Away
  gamedict["players"]["TOL_"+away]["Tm RU"] = game.stats_away.rushing_yds
  gamedict["players"]["TOL_"+away]["Tm PS"] = game.stats_away.passing_yds
  # Team defense - Home
  gamedict["players"]["TDEF_"+home]["PA"] = game.score_away
  gamedict["players"]["TDEF_"+home]["YA"] = game.stats_away.total_yds
  # Team defense - Away
  gamedict["players"]["TDEF_"+away]["PA"] = game.score_home
  gamedict["players"]["TDEF_"+away]["YA"] = game.stats_home.total_yds
  # Def/ST Home
  gamedict["players"]["TDEFST_"+away]["PA"] = game.score_home
  gamedict["players"]["TDEFST_"+away]["YA"] = game.stats_away.total_yds
  # Special teams - Home
  # Special teams - Away


def FillGameInfo(game, gamedict):
  gamedict["game"]["homescore"] = game.score_home
  gamedict["game"]["awayscore"] = game.score_away
  gamedict["game"]["date"] = game.schedule
  year = str(game.schedule["eid"])[0:4]
  gamedict["game"]["ID"] = year+str(game.schedule["month"]).strip().zfill(2)+str(game.schedule["day"]).strip().zfill(2)+"_"+game.away+"@"+game.home
  gamedict["game"]["away"] = game.away
  gamedict["game"]["home"] = game.home
  gamedict["game"]["season"] = game.season()
  gamedict["game"]["week"] = str(game.schedule["week"]).strip()
  gamedict["game"]["status"] = f.get_key(str(game.time))

def InitTeamPlayers(gamedict):
  home = gamedict["game"]["home"]
  away = gamedict["game"]["away"]
  gamedict["players"]["TOL_"+home] = {}
  gamedict["players"]["TOL_"+home]["name"] = "TOL_"+home
  gamedict["players"]["TOL_"+away] = {}
  gamedict["players"]["TOL_"+away]["name"] = "TOL_"+away
  gamedict["players"]["TDEF_"+home] = {}
  gamedict["players"]["TDEF_"+home]["name"] = "TDEF_"+home
  gamedict["players"]["TDEF_"+away] = {}
  gamedict["players"]["TDEF_"+away]["name"] = "TDEF_"+away
  gamedict["players"]["TDEFST_"+home] = {}
  gamedict["players"]["TDEFST_"+home]["name"] = "TDEFST_"+home
  gamedict["players"]["TDEFST_"+away] = {}
  gamedict["players"]["TDEFST_"+away]["name"] = "TDEFST_"+away
  gamedict["players"]["TST_"+home] = {}
  gamedict["players"]["TST_"+home]["name"] = "TST_"+home
  gamedict["players"]["TST_"+away] = {}
  gamedict["players"]["TST_"+away]["name"] = "TST_"+away

def GetPhpfflID(p):
    if nflids.get(p) is not None:
        return nflids[p]
    else:
        logerror("Player not found in phpffl: "+p)
        return p

def load_nflids():
    ids = dict()
    with open(lookupfile) as f:
        for line in f:
            nfl_id,phpffl_id = line.strip().split(",")
            ids[nfl_id] = phpffl_id
    return ids

def print_game(gamedict):
    text = ""
    text += "a:"+str(len(gamedict))+":{"
    for key, value in gamedict.items():
        if str(type(value)) == "<type 'dict'>":
            text += "s:"+str(len(str(key)))+":"+"\""+str(key)+"\";"
            text += print_game(value)
        else:
            text += "s:"+str(len(str(key)))+":"+"\""+str(key)+"\";"
            text += "s:"+str(len(str(value)))+":"+"\""+str(value)+"\";"
    text += "}"
    return text

def logerror(text):
  f = open("gamestats_error.log", "a")
  f.write(str(datetime.datetime.now())+" - "+text+"\n")
  f.close()



parser = argparse.ArgumentParser(description='Update phpffl static files')

parser.add_argument('-y', action="store", default="0", required=False, help="Year")
parser.add_argument('-w', action="store", default="0", required=False, help="Week")
parser.add_argument('-p', action="store", default="REG", required=False, help="Phase: PRE, REG, POST")

args = parser.parse_args()

main()
