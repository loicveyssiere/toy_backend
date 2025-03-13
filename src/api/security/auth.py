from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ...context import ContextManager
from ...types.user import UserAuthenticated
from .auth_manager import AuthSessionManager

context_manager = ContextManager()

class UserSession:

    user: UserAuthenticated | None = None
    raw_user: dict | None = None

    def __init__(self):
        print("Start User Sessions")

    def set_user_from_raw(self, raw_user: object):
        if raw_user is None:
            self.raw_user = None
            self.user = None
        else:
            self.raw_user = raw_user
            self.user = UserAuthenticated()
            #TODO check object
            self.user.account_id = self.raw_user["account_id"]
            self.user.name = self.raw_user["name"]
            self.user.role = self.raw_user["role"]

    def get_user(self) -> UserAuthenticated:
        return self.user

    def is_authenticated(self) -> bool:
        return self.user is not None

    def is_admin(self) -> bool:
        return self.user.role == "admin"


class APISecurity:

    is_public: bool = False
    require_admin: bool = False
    user_session: UserSession
    auth_session_manager: AuthSessionManager

    def __init__(self,
            auth: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
            auth_session_manager: AuthSessionManager = Depends(context_manager.inject_auth_session_manager),
            user_session = Depends(UserSession)
        ):
        print("Hello from AuthSSecurityessionManager")
        self.token = auth.credentials if auth is not None else None
        self.user_session = user_session
        self.auth_session_manager = auth_session_manager

        self.set_user_session()
        self.handle_http_errors()

    def set_user_session(self):
        if self.token is None:
            self.user_session = None
        else:
            raw_user = self.auth_session_manager.decode_jwt(self.token)
            self.user_session.set_user_from_raw(raw_user)

    def handle_http_errors(self):
        if self.token is None:
            raise HTTPException(status_code=401, detail="User not authenticated")
        if not self.user_session.is_authenticated():
            raise HTTPException(status_code=401, detail="User not authenticated")
        if self.require_admin and not self.user_session.is_admin():
            raise HTTPException(status_code=403, detail="Admin access required")

class AdminSecurity(APISecurity):
    def __init__(
        self,
        auth: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        auth_session_manager: AuthSessionManager = Depends(context_manager.inject_auth_session_manager),
        user_session: UserSession = Depends(UserSession),
    ):
        self.require_admin = True
        super().__init__(auth, auth_session_manager, user_session)


class PublicSecurity(APISecurity):
    def __init__(
        self,
        auth: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        auth_session_manager: AuthSessionManager = Depends(context_manager.inject_auth_session_manager),
        user_session: UserSession = Depends(UserSession),
    ):
        super().__init__(auth, auth_session_manager, user_session)

    def handle_http_errors(self):
        pass



# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = False):
#         super(JWTBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
#         if credentials:
#             if not credentials.scheme == "Bearer":
#                 raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
#             if not self.verify_jwt(credentials.credentials):
#                 raise HTTPException(status_code=403, detail="Invalid token or expired token.")
#             return credentials.credentials
#         else:
#             raise HTTPException(status_code=403, detail="Invalid authorization code.")

#     def verify_jwt(self, jwtoken: str) -> bool:
#         isTokenValid: bool = False

#         try:
#             payload = decode_jwt(jwtoken)
#         except:
#             payload = None
#         if payload:
#             isTokenValid = True

#         return isTokenValid

# async def public_endpoint(auth_service: Annotated[AuthService, Depends(AuthService)]):
#     print("1234")
#     auth_service.user = "public" 

# async def block_all_endpoints_by_default(auth_service: Annotated[AuthService, Depends(AuthService)]):
#     print("booo")
#     print("Here " + str(auth_service.get_user()))
#     if auth_service.get_user() is None:
#         print("CRITICAL", "not supposed to happen")
#         raise HTTPException(status_code=403, detail="Unauthorized")
