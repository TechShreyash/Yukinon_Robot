from dotenv import load_dotenv

load_dotenv("config.env")

HEROKU = (
    False  # NOTE Make it false if you're not deploying on heroku or docker.
)

BOT_TOKEN = "5064215617:AAH7cc824W-cRtjdmsEi-VaIfjTmM0U9gRI"
API_ID = 2344247
API_HASH = "853cae451f8091db916cd9ad395bbf12"
SUDO_USERS_ID = [
    1906005317,
    1693701096,
    1577304873,
    1791795037,
]  # Sudo users have full access to everything, don't trust anyone
LOG_GROUP_ID = -1001615868326
GBAN_LOG_GROUP_ID = -1001615868326
MESSAGE_DUMP_CHAT = -1001704010414
WELCOME_DELAY_KICK_SEC = 600
MONGO_URL = "mongodb+srv://yukino:yukinon@cluster0.vrlpf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
ARQ_API_KEY = "KBSFBD-AJYHUP-NUFRSH-BFNHZY-ARQ"
ARQ_API_URL = "https://thearq.tech"
LOG_MENTIONS = True
RSS_DELAY = 600  # In seconds
PM_PERMIT = True