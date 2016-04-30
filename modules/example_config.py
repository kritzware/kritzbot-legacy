# Bot IRC/Chat connection
HOST = "irc.chat.twitch.tv"
PORT = 6667
PASS = "oauth:pass_key" # Obtainable from https://twitchapps.com/tmi/
NICK = "bot_account_name"
CHANNEL = "channel_where_bot_will_live"

# Bot admin
ADMIN = "specify an admin for your bot"

# MySQL database connection
db_host = 'sql_host'
db_user = 'sql_user'
db_pass = 'sql_password'
db_name = 'database_name'
db_autocommit = True

# TWitter API
CONSUMER_KEY = 	'xxxx' # Obtainable from https://apps.twitter.com/
CONSUMER_SECRET = 'xxxx'
ACCESS_TOKEN = 'xxxx'
ACCESS_TOKEN_SECRET = 'xxxx'

# Channel specific settings
COMMAND_LINK = 'commands_url_page_here'
SOUNDS_LINK = 'sounds_url_page_here'
TWITTER = 'twitter.com/your_twitter_username_here'
MERCH = 'link_to_merch_store'
DISCORD = 'discord_link_here'
CURRENCY = 'the_name_for_channel_currency'
# NA = 'US/Eastern', GMT = 'Europe/London'
TIME_ZONE = 'specify_timezone'
PLAYSOUND_COST = 500 # Cost for playing sounds
VIEWER_POINT_GAIN = 1 # How many points a user gains per minute
DUEL_EXPIRE = 120 # When duels expire (seconds)
DUEL_COOLDOWN = 180 # Cooldown for duel usage
AUTO_MESSAGES = 1200 # Rate at which bot sends auto messages 