from dotenv import load_dotenv

load_dotenv("config.env")

HEROKU = (
    False  # NOTE Make it false if you're not deploying on heroku or docker.
)

if HEROKU:
    from os import environ

    BOT_TOKEN = environ.get("BOT_TOKEN", None)
    API_ID = int(environ.get("API_ID", 6))
    API_HASH = environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
    SESSION_STRING = environ.get("SESSION_STRING", None)
    USERBOT_PREFIX = environ.get("USERBOT_PREFIX", ".")
    SUDO_USERS_ID = [int(x) for x in environ.get("SUDO_USERS_ID", "").split()]
    LOG_GROUP_ID = int(environ.get("LOG_GROUP_ID", None))
    GBAN_LOG_GROUP_ID = int(environ.get("GBAN_LOG_GROUP_ID", None))
    MESSAGE_DUMP_CHAT = int(environ.get("MESSAGE_DUMP_CHAT", None))
    WELCOME_DELAY_KICK_SEC = int(environ.get("WELCOME_DELAY_KICK_SEC", None))
    MONGO_URL = environ.get("MONGO_URL", None)
    ARQ_API_URL = environ.get("ARQ_API_URL", None)
    ARQ_API_KEY = environ.get("ARQ_API_KEY", None)
    LOG_MENTIONS = bool(int(environ.get("LOG_MENTIONS", None)))
    RSS_DELAY = int(environ.get("RSS_DELAY", None))
    PM_PERMIT = bool(int(environ.get("PM_PERMIT", None)))
else:
    BOT_TOKEN = "5064215617:AAH7cc824W-cRtjdmsEi-VaIfjTmM0U9gRI"
    API_ID = 2344247
    API_HASH = "853cae451f8091db916cd9ad395bbf12"
    SUDO_USERS_ID = [
        4543744343,
        543214651351,
    ]  # Sudo users have full access to everything, don't trust anyone
    LOG_GROUP_ID = -1001615868326
    GBAN_LOG_GROUP_ID = -1001615868326
    MESSAGE_DUMP_CHAT = -1001615868326
    WELCOME_DELAY_KICK_SEC = 600
    MONGO_URL = "mongodb+srv://yukino:yukinon@cluster0.vrlpf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    ARQ_API_KEY = "KBSFBD-AJYHUP-NUFRSH-BFNHZY-ARQ"
    ARQ_API_URL = "https://thearq.tech"
    LOG_MENTIONS = True
    RSS_DELAY = 600  # In seconds
    PM_PERMIT = True