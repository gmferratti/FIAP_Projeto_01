class Config:
    TESTING = False
    USE_LOCAL_DATA = False


class TestConfig(Config):
    TESTING = True
    USE_LOCAL_DATA = True
