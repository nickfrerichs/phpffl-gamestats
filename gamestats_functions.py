def get_key(stat):
  if stat == "passing_cmp": return "Cpl"
  if stat == "passing_att": return "PassAtt"
  if stat == "passing_yds": return "PS Yds"
  if stat == "passing_ints": return "Int"
  if stat == "passing_tds": return "TD-P"
  if stat == "rushing_yds": return "RU Yds"
  if stat == "rushing_tds": return "TD-Ru"
  if stat == "receiving_rec": return "Rec"
  if stat == "receiving_yds": return "REC Yds"
  if stat == "receiving_tds": return "TD-Re"
  if stat == "fumbles_lost": return "Fum"
  if stat == "defense_tkl": return "Tk"
  if stat == "defense_sk": return "Sck"
  if stat == "defense_int": return "Intercepts"
  if stat == "defense_ffum": return "FF"
  if stat == "kicking_xpmade": return "XP"
  if stat == "kicking_xptot": return "XPAtt"
  if stat == "kicking_xpmissed": return "XPM"
  if stat == "kicking_fgmissed": return "Ms FG"
  if stat == "passing_twoptm": return "2-ptP"
  if stat == "rushing_twoptm": return "2-ptR"
  if stat == "receiving_twoptm": return "2-ptR"
  #if stat == "rushing_twopta": return "2-ptR"
  #if stat == "receiving_twopta": return "2-ptR"
  if stat == "kickret_yds": return "KR Yds"
  if stat == "puntret_yds": return "PR Yds"
  if stat == "kickret_tds": return "TD-S"
  if stat == "puntret_tds": return "TD-S"
  if stat == "passing_int": return "Int"
  if stat == "final overtime": return "Final"
  return stat


def team_sack(event, gamedict):
  home = gamedict["game"]["home"]
  away = gamedict["game"]["away"]
  if event["team"] == away:
    if gamedict["players"]["TOL_"+away].get("Sckd") == None:
      gamedict["players"]["TOL_"+away]["Sckd"] = 0.0
    gamedict["players"]["TOL_"+away]["Sckd"] += event["passing_sk"]
    if gamedict["players"]["TDEF_"+home].get("Sck") == None:
      gamedict["players"]["TDEF_"+home]["Sck"] = 0.0
    gamedict["players"]["TDEF_"+home]["Sck"] += event["passing_sk"]
    if gamedict["players"]["TDEFST_"+home].get("Sck") == None:
      gamedict["players"]["TDEFST_"+home]["Sck"] = 0.0
    gamedict["players"]["TDEFST_"+home]["Sck"] += event["passing_sk"]
  else:
    if gamedict["players"]["TOL_"+home].get("Sckd") == None:
      gamedict["players"]["TOL_"+home]["Sckd"] = 0.0
    gamedict["players"]["TOL_"+home]["Sckd"] += event["passing_sk"]
    if gamedict["players"]["TDEF_"+away].get("Sck") == None:
      gamedict["players"]["TDEF_"+away]["Sck"] = 0.0
    gamedict["players"]["TDEF_"+away]["Sck"] += event["passing_sk"]
    if gamedict["players"]["TDEFST_"+away].get("Sck") == None:
      gamedict["players"]["TDEFST_"+away]["Sck"] = 0.0
    gamedict["players"]["TDEFST_"+away]["Sck"] += event["passing_sk"]

def team_fumble(event,gamedict):
  home = gamedict["game"]["home"]
  away = gamedict["game"]["away"]
  if event["team"] == away:
    if gamedict["players"]["TDEF_"+home].get("Fum") == None:
      gamedict["players"]["TDEF_"+home]["Fum"] = 0
    gamedict["players"]["TDEF_"+home]["Fum"] = gamedict["players"]["TDEF_"+home]["Fum"] + event["fumbles_lost"]
    if gamedict["players"]["TDEFST_"+home].get("Fum") == None:
      gamedict["players"]["TDEFST_"+home]["Fum"] = 0
    gamedict["players"]["TDEFST_"+home]["Fum"] = gamedict["players"]["TDEFST_"+home]["Fum"] + event["fumbles_lost"]
  else:
    if gamedict["players"]["TDEF_"+away].get("Fum") == None:
      gamedict["players"]["TDEF_"+away]["Fum"] = 0
    gamedict["players"]["TDEF_"+away]["Fum"] = gamedict["players"]["TDEF_"+away]["Fum"] + event["fumbles_lost"]
    if gamedict["players"]["TDEFST_"+away].get("Fum") == None:
      gamedict["players"]["TDEFST_"+away]["Fum"] = 0
    gamedict["players"]["TDEFST_"+away]["Fum"] = gamedict["players"]["TDEFST_"+away]["Fum"] + event["fumbles_lost"]


def team_defint(event,gamedict):

  home = gamedict["game"]["home"]
  away = gamedict["game"]["away"]

  if event["team"] == home:
    if gamedict["players"]["TDEF_"+home].get("Int") == None:
      gamedict["players"]["TDEF_"+home]["Int"] = 0
    gamedict["players"]["TDEF_"+home]["Int"] += event["defense_int"]
    if gamedict["players"]["TDEFST_"+home].get("Int") == None:
      gamedict["players"]["TDEFST_"+home]["Int"] = 0
    gamedict["players"]["TDEFST_"+home]["Int"] += event["defense_int"]
  else:
    if gamedict["players"]["TDEF_"+away].get("Int") == None:
      gamedict["players"]["TDEF_"+away]["Int"] = 0
    gamedict["players"]["TDEF_"+away]["Int"] += event["defense_int"]
    if gamedict["players"]["TDEFST_"+away].get("Int") == None:
      gamedict["players"]["TDEFST_"+away]["Int"] = 0
    gamedict["players"]["TDEFST_"+away]["Int"] += event["defense_int"]


def team_def_td(event,gamedict):

  home = gamedict["game"]["home"]
  away = gamedict["game"]["away"]

  if event["team"] == home:
    if gamedict["players"]["TDEF_"+home].get("TD-D") == None:
      gamedict["players"]["TDEF_"+home]["TD-D"] = 0
    gamedict["players"]["TDEF_"+home]["TD-D"] += 1
    if gamedict["players"]["TDEFST_"+home].get("TD-D") == None:
      gamedict["players"]["TDEFST_"+home]["TD-D"] = 0
    gamedict["players"]["TDEFST_"+home]["TD-D"] += 1
  else:
    if gamedict["players"]["TDEF_"+away].get("TD-D") == None:
      gamedict["players"]["TDEF_"+away]["TD-D"] = 0
    gamedict["players"]["TDEF_"+away]["TD-D"] += 1
    if gamedict["players"]["TDEFST_"+away].get("TD-D") == None:
      gamedict["players"]["TDEFST_"+away]["TD-D"] = 0
    gamedict["players"]["TDEFST_"+away]["TD-D"] += 1


def team_def_saf(event,gamedict):

  home = gamedict["game"]["home"]
  away = gamedict["game"]["away"]

  if event["team"] == home:
    if gamedict["players"]["TDEF_"+home].get("Sfty") == None:
      gamedict["players"]["TDEF_"+home]["Sfty"] = 0
    gamedict["players"]["TDEF_"+home]["Sfty"] += event["defense_safe"]
    if gamedict["players"]["TDEFST_"+home].get("Sfty") == None:
      gamedict["players"]["TDEFST_"+home]["Sfty"] = 0
    gamedict["players"]["TDEFST_"+home]["Sfty"] += event["defense_safe"]
  else:
    if gamedict["players"]["TDEF_"+away].get("Sfty") == None:
      gamedict["players"]["TDEF_"+away]["Sfty"] = 0
    gamedict["players"]["TDEF_"+away]["Sfty"] += event["defense_safe"]
    if gamedict["players"]["TDEFST_"+away].get("Sfty") == None:
      gamedict["players"]["TDEFST_"+away]["Sfty"] = 0
    gamedict["players"]["TDEFST_"+away]["Sfty"] += event["defense_safe"]


def team_st_td(event,gamedict):
  home = gamedict["game"]["home"]
  away = gamedict["game"]["away"]

  if event["team"] == home:
    if gamedict["players"]["TDEFST_"+home].get("TD-S") == None:
      gamedict["players"]["TDEFST_"+home]["TD-S"] = 0
    gamedict["players"]["TDEFST_"+home]["TD-S"] += 1
    if gamedict["players"]["TST_"+home].get("TD-S") == None:
      gamedict["players"]["TST_"+home]["TD-S"] = 0
    gamedict["players"]["TST_"+home]["TD-S"] += 1
    if gamedict["players"]["TDEF_"+home].get("TD-S") == None:
      gamedict["players"]["TDEF_"+home]["TD-S"] = 0
    gamedict["players"]["TDEF_"+home]["TD-S"] += 1
  else:
    if gamedict["players"]["TDEFST_"+away].get("TD-S") == None:
      gamedict["players"]["TDEFST_"+away]["TD-S"] = 0
    gamedict["players"]["TDEFST_"+away]["TD-S"] += 1
    if gamedict["players"]["TST_"+away].get("TD-S") == None:
      gamedict["players"]["TST_"+away]["TD-S"] = 0
    gamedict["players"]["TST_"+away]["TD-S"] += 1
    if gamedict["players"]["TDEF_"+away].get("TD-S") == None:
      gamedict["players"]["TDEF_"+away]["TD-S"] = 0
    gamedict["players"]["TDEF_"+away]["TD-S"] += 1


def player_field_goal(phpffl_id, event, gamedict):

  if gamedict["players"].get(phpffl_id) is None:  # new player, initialize
    gamedict["players"][phpffl_id] = {}

  distance = event["kicking_fgm_yds"]

  if distance > 0 and distance <= 24:
    if gamedict["players"][phpffl_id].get("FG-20") == None:
       gamedict["players"][phpffl_id]["FG-20"] = 0
    gamedict["players"][phpffl_id]["FG-20"] = gamedict["players"][phpffl_id]["FG-20"] + 1
  if distance > 24 and distance <= 29:
    if gamedict["players"][phpffl_id].get("FG-25") == None:
       gamedict["players"][phpffl_id]["FG-25"] = 0
    gamedict["players"][phpffl_id]["FG-25"] = gamedict["players"][phpffl_id]["FG-25"] + 1
  if distance > 29 and distance <= 34:
    if gamedict["players"][phpffl_id].get("FG-30") == None:
       gamedict["players"][phpffl_id]["FG-30"] = 0
    gamedict["players"][phpffl_id]["FG-30"] = gamedict["players"][phpffl_id]["FG-30"] + 1
  if distance > 34 and distance <= 39:
    if gamedict["players"][phpffl_id].get("FG-35") == None:
       gamedict["players"][phpffl_id]["FG-35"] = 0
    gamedict["players"][phpffl_id]["FG-35"] = gamedict["players"][phpffl_id]["FG-35"] + 1
  if distance > 39 and distance <= 44:
    if gamedict["players"][phpffl_id].get("FG-40") == None:
       gamedict["players"][phpffl_id]["FG-40"] = 0
    gamedict["players"][phpffl_id]["FG-40"] = gamedict["players"][phpffl_id]["FG-40"] + 1
  if distance > 44 and distance <= 49:
    if gamedict["players"][phpffl_id].get("FG-45") == None:
       gamedict["players"][phpffl_id]["FG-45"] = 0
    gamedict["players"][phpffl_id]["FG-45"] = gamedict["players"][phpffl_id]["FG-45"] + 1
  if distance > 49 and distance <= 54:
    if gamedict["players"][phpffl_id].get("FG-50") == None:
       gamedict["players"][phpffl_id]["FG-50"] = 0
    gamedict["players"][phpffl_id]["FG-50"] = gamedict["players"][phpffl_id]["FG-50"] + 1
  if distance >= 55:
    if gamedict["players"][phpffl_id].get("FG-55") == None:
       gamedict["players"][phpffl_id]["FG-55"] = 0
    gamedict["players"][phpffl_id]["FG-55"] = gamedict["players"][phpffl_id]["FG-55"] + 1

def AddPlayerStat(phpffl_id,stat,event,gamedict):
  if gamedict["players"].get(phpffl_id) is None:  # new player, initialize
    gamedict["players"][phpffl_id] = {}

#  e_playerid = event["playerid"]
  phpfflkey = get_key(stat)
  if gamedict["players"][phpffl_id].get(phpfflkey) is None:  # If first time seeing this stat, add it.
    gamedict["players"][phpffl_id][phpfflkey] = event[stat]
  else: # Otherwise check if it's an integer and add it.
    gamedict["players"][phpffl_id][phpfflkey] = gamedict["players"][phpffl_id][phpfflkey] + event[stat]

def AddPlayerTD(phpffl_id, stat, event, gamedict):
  if gamedict["players"].get(phpffl_id) is None:  # new player, initialize
    gamedict["players"][phpffl_id] = {}

  if event.get("rushing_yds") is not None:
    yards = int(event["rushing_yds"])
  if event.get("receiving_yds") is not None:
    yards = int(event["receiving_yds"])

  if yards > 0 and yards <= 1:
    yards = 1
  if yards > 1 and yards <= 9:
    yards = 9
  if yards > 9 and yards <= 19:
    yards = 19
  if yards > 19 and yards <= 29:
    yards = 29
  if yards > 29 and yards <= 39:
    yards = 39
  if yards > 39 and yards <= 49:
    yards = 49
  if yards > 49 and yards <= 59:
    yards = 59
  if yards > 59 and yards <= 69:
    yards = 69
  if yards > 69 and yards <= 79:
    yards = 79
  if yards > 79 and yards <= 89:
    yards = 89
  if yards > 89 and yards <= 99:
    yards = 99
  if yards > 100:
    yards = 100
  yards = "TD-"+str(yards)

  if gamedict["players"][phpffl_id].get(yards) is None:  # If first time seeing this stat, add i
    gamedict["players"][phpffl_id][yards] = 1
  else: # Otherwise check if it's an integer and add it.
    gamedict["players"][phpffl_id][yards] = gamedict["players"][phpffl_id][yards] + 1


