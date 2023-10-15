import requests
import time


TEST_PROXY_URL = 'http://127.0.0.1:8000/demo'
PAUSE_TIME = 1

def test_proxy(test_proxy_url, post_data, STATUS_OK=200):
    res = requests.post(test_proxy_url, json=post_data)
    test_data = res.json()
    assert res.status_code == STATUS_OK
    assert test_data["message"]["post_data"] == post_data


if __name__ == "__main__":
    test_data = {"username": "tebra", "city": "SU"}
    time.sleep(PAUSE_TIME)
    test_proxy(TEST_PROXY_URL, test_data)
