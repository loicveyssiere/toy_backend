
from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends

from ..repositories.loan_repository import LoanRepository

from ..api.security.auth import UserSession
from ..context import ContextManager



context = ContextManager()


class ILoanService(ABC):
    @abstractmethod
    async def borrowing(self, id: str):
        ...

    @abstractmethod
    async def returning(self, id: str):
        ...

class LoanService(ILoanService):

    user_session: UserSession
    loan_repository: LoanRepository


    def __init__(self,
        user_session: Annotated[UserSession, Depends(UserSession)],
        loan_repository: Annotated[LoanRepository, Depends(LoanRepository)],
    ):
        self.loan_repository = loan_repository
        self.user_session = user_session

    async def borrowing(self, book_copy_id: str):
        account_id = self.user_session.get_user().account_id
        processed = await self.loan_repository.borrowing(account_id, book_copy_id)
        return processed

    async def returning(self, book_copy_id: str):
        account_id = self.user_session.get_user().account_id
        await self.loan_repository.returning(account_id, book_copy_id)
