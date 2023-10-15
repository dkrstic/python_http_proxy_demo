class Config:
    TARGET_ENDPOINT = 'http://127.0.0.1:5000'
    SECRET_KEY = 'a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf'
    USER_PARAM = 'user'
    USERNAME_PARAM = 'username'
    JWT_HEADER = 'x-my-jwt'
    CONTENT_TYPE_PARAM = 'CONTENT-TYPE'
    DEFAULT_CONTENT_TYPE = 'application/json'
    IAT_PARAM = 'iat'
    JTI_PARAM = 'jti'
    DATE_PARAM = 'date'
    ALGORITHM = 'HS512'
    WAITING_TIME = 5

    HOST = '0.0.0.0'
    PORT = 8000

    RAND_RANGE_START = 0
    RAND_RANGE_END = 1000000