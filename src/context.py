from .api.security.auth_manager import AuthSessionManager
from .core.db import AsyncDatabaseClient

class ContextManager:
    
    _instance = None

    db_connection: AsyncDatabaseClient = None
    auth_session_manager: AuthSessionManager = None

    def __new__(cls):
        if cls._instance is None:
            print("create context singleton")
            cls._instance = super(ContextManager, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def set_db_connection(self, db_connection: AsyncDatabaseClient):
        self.db_connection = db_connection

    def set_auth_session_manager(self, auth_session_manager: AuthSessionManager):
        self.auth_session_manager = auth_session_manager

    def inject_db_connection(self) -> AsyncDatabaseClient:
        if self.db_connection is None:
            # TODO handle correctly errors
            raise Exception("db_connection is not already initialized")
        return self.db_connection

    def inject_auth_session_manager(self) -> AuthSessionManager:
        return self.auth_session_manager


