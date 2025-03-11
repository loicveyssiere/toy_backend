from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends

from ..api.security.auth import UserSession

from ..context import ContextManager
from ..repositories.book_repository import BookRepository
from ..types.book import BookCopy, BookReference

context = ContextManager()

class IBookService(ABC):
    @abstractmethod
    async def create_book_reference(self, book_ref: BookReference, copies: list[BookCopy]):
        ...


class BookService(IBookService):

    book_repository: BookRepository

    # def __init__(self, book_repository: BookRepository = Depends(BookRepository)):
    #     self.book_repository = book_repository

    def __init__(self,
        user_session: Annotated[UserSession, Depends(UserSession)],
        book_repository: Annotated[BookRepository, Depends(BookRepository)],
    ):
        self.book_repository = book_repository
        self.user_session = user_session

    async def create_book_reference(self, book_ref: BookReference, copies: list[BookCopy]):
        print(self.user_session.get_user())
        ref_id = await self.book_repository.create_book_reference(book_ref)
        await self.book_repository.register_book_copies(ref_id, copies)
