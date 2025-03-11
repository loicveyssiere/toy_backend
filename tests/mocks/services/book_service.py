
from src.services.book_service import IBookService
from src.types.book import BookCopy, BookReference


class MockBookService(IBookService):
    async def create_book_reference(self, book: BookReference, copies: list[BookCopy]):
        return
