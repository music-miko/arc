from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

class Config(object):
    # required config variables
    API_HASH = getenv("API_HASH", 261715b51a1c353b199550c729e85c7b)                # get from my.telegram.org
    API_ID = int(getenv("API_ID", 28932292)                  # get from my.telegram.org
    BOT_TOKEN = getenv("BOT_TOKEN", 7682956374:AAGGJG041qNNImAWKnnUrmocHLdNu7XBlhQ)              # get from @BotFather
    DATABASE_URL = getenv("DATABASE_URL", None)        # from https://cloud.mongodb.com/
    HELLBOT_SESSION = getenv("HELLBOT_SESSION", BQG5eMQAgdMyrxOOptRQDcnJz58XTwXfQ6nAkhderv1of100UUmxv99Crh0pZXqfezmlY97Kj4p7WhfEV8AE0XQGoVTWMoS_mi96yT5_fHUCkU3RkpE5OqA8yFXJ3dlOvsQ8mR4fesD0eY0yvItHWqdvLwk7pPqJXoDRkrutIEC45DnIOZWoFDukhR4TtaXX7gcKnyC78oSdnMxhwE-VIV7JxGUEh6a8xYfheweXGptnQ-KMiJHQmLRThOCxUpy4jPovMTEIsHxVpUr1Is8Z_tl7ToL5Rw3CSdZIapqZkDX3MAKdmM4Bmv8SP1i1JDMMP9_vbDCUmoawImCAXZ0wgwwTBRqGCgAAAAHjQxQ5AA)  # enter your session string here
    LOGGER_ID = int(getenv("LOGGER_ID", -1002333699774))            # make a channel and get its ID
    OWNER_ID = getenv("OWNER_ID", "7428444089")                  # enter your id here

    # optional config variables
    BLACK_IMG = getenv("BLACK_IMG", "https://telegra.ph/file/2c546060b20dfd7c1ff2d.jpg")        # black image for progress
    BOT_NAME = getenv("BOT_NAME", "\x40\x4d\x75\x73\x69\x63\x5f\x48\x65\x6c\x6c\x42\x6f\x74")   # dont put fancy texts here.
    BOT_PIC = getenv("BOT_PIC", "https://te.legra.ph/file/5d5642103804ae180e40b.jpg")           # put direct link to image here
    LEADERBOARD_TIME = getenv("LEADERBOARD_TIME", "3:00")   # time in 24hr format for leaderboard broadcast
    LYRICS_API = getenv("LYRICS_API", None)             # from https://docs.genius.com/
    MAX_FAVORITES = int(getenv("MAX_FAVORITES", 30))    # max number of favorite tracks
    PLAY_LIMIT = int(getenv("PLAY_LIMIT", 0))           # time in minutes. 0 for no limit
    PRIVATE_MODE = getenv("PRIVATE_MODE", "off")        # "on" or "off" to enable/disable private mode
    SONG_LIMIT = int(getenv("SONG_LIMIT", 0))           # time in minutes. 0 for no limit
    TELEGRAM_IMG = getenv("TELEGRAM_IMG", None)         # put direct link to image here
    TG_AUDIO_SIZE_LIMIT = int(getenv("TG_AUDIO_SIZE_LIMIT", 104857600))     # size in bytes. 0 for no limit
    TG_VIDEO_SIZE_LIMIT = int(getenv("TG_VIDEO_SIZE_LIMIT", 1073741824))    # size in bytes. 0 for no limit
    TZ = getenv("TZ", "Asia/Kolkata")   # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

    # do not edit these variables
    BANNED_USERS = filters.user()
    CACHE = {}
    CACHE_DIR = "./cache/"
    DELETE_DICT = {}
    DWL_DIR = "./downloads/"
    GOD_USERS = filters.user()
    PLAYER_CACHE = {}
    QUEUE_CACHE =  {}
    SONG_CACHE = {}
    SUDO_USERS = filters.user()


# get all config variables in a list
all_vars = [i for i in Config.__dict__.keys() if not i.startswith("__")]
