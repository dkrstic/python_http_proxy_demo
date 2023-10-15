import random

import aiohttp
import time
import jwt
import uvicorn
from datetime import date
from urllib.parse import urljoin
from fastapi import FastAPI, Request, Response
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import Config

app = FastAPI()
app.request_cnt = 0
app.timer = time.time()
templates = Jinja2Templates(directory="app/templates")


@app.post("/demo")
async def proxy_request(request: Request, response: Response):
    target_url = urljoin(Config.TARGET_ENDPOINT, request.url.path)
    post_data = await request.json()
    username = post_data[Config.USERNAME_PARAM]
    jwt_token = create_jwt_token(username)
    headers = {Config.JWT_HEADER: jwt_token, Config.CONTENT_TYPE_PARAM: Config.DEFAULT_CONTENT_TYPE}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(target_url, json=post_data) as res:
            res_body = await res.json()
    res_status = res.status
    response.status_code = res_status
    result = {"status": res_status, "message": res_body}
    app.request_cnt += 1
    print(result)
    return result


@app.get("/status", response_class=HTMLResponse)
async def get_status(request: Request):
    elapsed = int(time.time() - app.timer)
    cnt = app.request_cnt
    return templates.TemplateResponse("status.html", {"request": request, "elapsed": elapsed, "cnt": cnt})


def create_jwt_token(username):
    today = date.today()
    today_date = today.strftime("%Y-%m-%d")
    jwt_id = get_jwt_id(username)
    payload = {Config.IAT_PARAM: int(time.time()), Config.JTI_PARAM: jwt_id, Config.USER_PARAM: username,
               Config.DATE_PARAM: today_date}
    return jwt.encode(payload, Config.SECRET_KEY, Config.ALGORITHM)


def get_jwt_id(username):
    ran_id = str(random.randint(Config.RAND_RANGE_START, Config.RAND_RANGE_END))
    ts = str(int(time.time() * 1000))
    jwt_id = '-'.join([ran_id, username, ts])
    return jwt_id


if __name__ == "__main__":
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
