from Keys import db
db_team_data = db["TeamData"] # defines teamdata (TeamData Collection)
db_bot_data = db["BotData"] # defines botdata (BotData Collection)

### Auto Event Configs
## Hours Before event starts
setup = 1 # 1 hour before
checkin = 1 # 1 hour before
poi_selection = 48 # 2 days before