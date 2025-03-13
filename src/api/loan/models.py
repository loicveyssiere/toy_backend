from pydantic import BaseModel


class BorrowingRequest(BaseModel):
    book_copy_id: str

class ReturningRequest(BaseModel):
    book_copy_id: str
