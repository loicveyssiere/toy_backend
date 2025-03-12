
import time

import jwt


class AuthSessionManager:
    def __init__(self, jwt_secret: str, jwt_algorithm: str = "HS256"):
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm

    def sign_jwt(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "expires": time.time() + 500
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

        return token

    def decode_jwt(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.jwt_secret, algorithms=self.jwt_algorithm)
        except Exception as e:
            # TODO Handle exeptions correlty
            print(e)
            return None
