
from src.services.book_service import IBookService
from src.types.book import BookCopy, BookReference
from src.types.user import UserAuthenticated


class MockBookService(IBookService):
    async def create_book_reference(self, book: BookReference, copies: list[BookCopy]):
        return "00000-000000-000000-0000000"

    async def register_book_copies(self, user: UserAuthenticated, ref_id: str, copies: list[BookCopy]):
        pass
