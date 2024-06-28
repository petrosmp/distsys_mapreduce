from os import getenv


class Config:
    SECRET_KEY: str = getenv("SECRET_KEY")
