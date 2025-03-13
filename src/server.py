from fastapi import Depends, FastAPI

from .api.book.routes import router as book_router
from .api.loan.routes import router as loan_router
from .api.security.auth_manager import AuthSessionManager
from .context import ContextManager
from .core.config import settings
from .core.db import AsyncDatabaseClient

db_connection = AsyncDatabaseClient()
auth_session_manager = AuthSessionManager("secretsecretsecretsecretsecretsecretsecret")
context = ContextManager()
context.set_db_connection(db_connection)
context.set_auth_session_manager(auth_session_manager)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    #dependencies=[Depends(block_all_endpoints_by_default)]
)

app.include_router(book_router, prefix="/api/books")
app.include_router(loan_router, prefix="/api/loans")
