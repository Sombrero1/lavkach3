from enum import Enum


class CacheTag(Enum):
    GET_USER_LIST = "get_user_list"
    WS_SESSION = "ws_session"
    MODEL = 'model'

class CacheStrategy(str, Enum):
    FULL: str = 'FULL'
    NONE: str = 'NONE'