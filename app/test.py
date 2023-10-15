import unittest

import jwt
import time
from datetime import date

from main import get_jwt_id, create_jwt_token, Config

WAITING_TIME = Config.WAITING_TIME

class TestJwtProxy(unittest.TestCase):
    def test_jwt_id(self):
        """
        Test if jwt id (jit) satisfies format '{random_num}-{useraname}-{current_timestamp_ms}'
        """
        username = "test_user"
        result = get_jwt_id(username)
        ts_ms = time.time() * 1000
        jit_ts = int(result[-13:])
        self.assertEqual(result[-14], '-')
        self.assertGreaterEqual(ts_ms, jit_ts)  # current ts >= jit timestamp
        self.assertLessEqual(ts_ms, jit_ts + WAITING_TIME * 1000)  # current ts <= jit timestamp + 5sec

    def test_jwt_token(self):
        """
        Test if jwt token provides required payload parameters and claims
        """
        username = 'test_user'
        today = date.today()
        today_date = today.strftime("%Y-%m-%d")
        result_token = create_jwt_token(username)
        decoded_token = jwt.decode(result_token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM],
                                   options={"require": [Config.IAT_PARAM, Config.JTI_PARAM]})
        current_time = time.time()
        iat_val = decoded_token.get(Config.IAT_PARAM)
        self.assertGreaterEqual(current_time, iat_val)
        self.assertLessEqual(current_time, iat_val + WAITING_TIME)
        self.assertIn(Config.JTI_PARAM, decoded_token.keys())
        self.assertEqual(decoded_token.get('user'), 'test_user')
        self.assertEqual(decoded_token.get(Config.DATE_PARAM), today_date)


if __name__ == '__main__':
    unittest.main()
