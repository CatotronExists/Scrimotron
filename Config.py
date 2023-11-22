from Keys import db
db_team_data = db["TeamData"] # defines teamdata (TeamData Collection)
db_bot_data = db["BotData"] # defines botdata (BotData Collection)

### Auto Event Configs
## Hours Before event starts
setup = 1 # 1 hour before
checkin = 1 # 1 hour before
poi_selection = 48 # 2 days before
delay = 0 # Minute in the hour to check

### Assets
# Images
logo = "https://cdn.discordapp.com/icons/988302458533085234/6e2c8b045e0150185d14ffcd8cf6a2e3.png"
banner = ""