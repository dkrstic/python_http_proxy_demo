import time
import jwt

import datetime
from fastapi import FastAPI, Request, Response, status
from config import Config

demo_endpoint_app = FastAPI()
WAITING_TIME = Config.WAITING_TIME


@demo_endpoint_app.post("/demo")
async def demo_request(request: Request, response: Response):
    post_data = await request.json()
    headers = request.headers
    encoded_token = headers.get(Config.JWT_HEADER)
    decoded_token = jwt.decode(encoded_token, options={"require": ["iat", "jti"]}, algorithms=[Config.ALGORITHM],
                               key=Config.SECRET_KEY)
    print("Decoded token: {}".format(decoded_token))
    result = validate_token(decoded_token)
    print("Post data: {}".format(post_data))
    result["post_data"] = post_data
    response.status_code = result["status"]
    return result


def validate_token(decoded_token):
    message = ""
    status_code = status.HTTP_401_UNAUTHORIZED
    today = datetime.date.today()
    today_date = today.strftime("%Y-%m-%d")
    username = decoded_token.get(Config.USER_PARAM)
    date = decoded_token.get(Config.DATE_PARAM)
    iat = decoded_token.get(Config.IAT_PARAM)
    jti = decoded_token.get(Config.JTI_PARAM)
    print('user: {}, date: {}, iat: {}, jti: {}'.format(username, date, iat,jti))
    current_time = time.time()
    try:
        int(jti[-13:])
    except ValueError:
        message = "Wrong jwt ID structure"
        response = {"status": status_code, "message": message}
        print("Response: {}".format(response))
        return response
    if date != today_date:
        message = "Wrong date"
    if current_time > iat + WAITING_TIME:
        message = "Token expired"
    elif current_time < iat:
        message = "Wrong iat value"
    elif username not in jti or len(jti) < 15 or "-" not in jti:
        message = "jwt ID identification failure"
    else:
        status_code = status.HTTP_200_OK
    response = {"status": status_code, "message": message}
    print("Response: {}".format(response))
    return response
