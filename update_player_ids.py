import sys
import MySQLdb
import MySQLdb.cursors
import json
import nflgame
import os
import config as c


db = MySQLdb.connect(host=c.dbhost, user=c.dbuser, passwd=c.dbpass, db=c.dbname, cursorclass=MySQLdb.cursors.DictCursor)

# File to save a lookup table to be used for nflgame -> cbs player id lookup
lookupfile = os.path.dirname(os.path.abspath(__file__))+"/playerids.txt"

nflids = dict()
new_adds = 0

def main():
  global nflids
  cur = db.cursor()
  nflids = load_nflids()
  nomatch = 0
  done = 0
  players = nflgame.players
  active = " and active = 'yes'"
  #active = ""

  for p in players:
    first = players[p].first_name.replace(".","")
    last = players[p].last_name
    pos = players[p].position
    team = players[p].team
    status = players[p].status
#    print "%s %s" % (first, last)
#    if status != "ACT":
#      continue
    if nflids.get(str(p)) is not None:
      done += 1
      continue
    cur.execute("Select ID from players where replace(firstname,'.','') like '%%%s%%' and lastname = '%s' %s" % (first.replace("'","''"),last.replace("'","''"),active))
    query = ("Select ID from players where replace(firstname,'.','') like '%%%s%%' and lastname = '%s' %s" % (first.replace("'","''"),last.replace("'","''"),active))

    if cur.rowcount == 0: # Not found in phpffl players table
      print "No match in phpffl using: ( %s+%s ) nfl_id: %s" % (first, last, p)
      nomatch += 1
      continue
    elif cur.rowcount == 1: # Found using firstname and lastname
      row = cur.fetchone()
      AddID(p, row["ID"])
    else: # Found too many, add position to query
      cur.execute("Select ID from players where replace(firstname,'.','') like '%%%s%%' and lastname = '%s' and positionID = '%s' %s" % (first.replace("'","''"),last.replace("'","''"),pos,active))
      if cur.rowcount == 0: # Not found after adding pos in phpffl players table, must be a duplicate
        print 'Duplicate in phpffl using: ( %s+%s ) nfl_id: %s' % (first,last,p)
        continue
      elif cur.rowcount == 1: # Found using firstname, lastname, and pos
        row = cur.fetchone()
        AddID(p, row["ID"])
      else: # Found too many, add team to query
        if pos == None:
          cur.execute("Select ID from players where replace(firstname,'.','') like '%%%s%%' and lastname = '%s' and teamID = '%s' %s" % (first.replace("'","''"),last.replace("'","''"),team,active))
        else:
          cur.execute("Select ID from players where replace(firstname,'.','') like '%%%s%%' and lastname = '%s' and positionID = '%s' and teamID = '%s' %s" % (first.replace("'","''"),last.replace("'","''"),pos,team,active))
        if cur.rowcount == 1: # Found using firstname, lastname, pos, and team
          row = cur.fetchone()
          AddID(p, row["ID"])
        else: # Not found and is and is a duplicate
	  print 'Duplicate in phpffl using: ( %s+%s+POS:"%s" ) nfl_id: %s' % (first,last,pos,p)
          continue

  save_nflids()
  print
  print "-----------------------------------"
  print "Newly added: %s" % (str(new_adds))
  print "Already exist: %s" % str(done)
  print "No match in phpffl: %s" % str(nomatch)

def load_nflids():
    ids = dict()
    if not os.path.isfile(lookupfile):
        open(lookupfile, 'a').close()
    with open(lookupfile) as f:
        for line in f:
            nfl_id,phpffl_id = line.strip().split(",")
            ids[nfl_id] = phpffl_id
    return ids

def save_nflids():
    with open(lookupfile,'w') as f:
        for n in nflids:
            f.write(n+','+nflids[n]+'\n')

def AddID(nfl_id, phpffl_id):
    global new_adds
    nflids[nfl_id] = phpffl_id
    new_adds += 1
main()
