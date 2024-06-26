from datetime import datetime, timedelta, UTC

import jwt

from core.db_config import config
from core.exceptions import DecodeTokenException, ExpiredTokenException


class TokenHelper:
    @staticmethod
    def encode(payload: dict, expire_period: int = 36000) -> str:
        token = jwt.encode(
            payload={
                **payload,
                "exp": datetime.now(UTC) + timedelta(seconds=expire_period),
            },
            key=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        )#.decode("utf8")
        return token

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
                options={"verify_exp": False},
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
