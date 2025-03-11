from datetime import datetime

from pydantic import BaseModel


class RegisterBookCopy(BaseModel):
    condition: str

class CreateBookReferenceRequest(BaseModel):
    title: str
    author: str
    published_date: datetime
    copies: list[RegisterBookCopy] | None = []

class RegisterBookCopyRequest(BaseModel):
    book_reference_id: str
    copy: RegisterBookCopy


