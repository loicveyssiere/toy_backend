from typing import Annotated

from fastapi import APIRouter, Depends

from ..security.auth import AdminSecurity

from ...services.book_service import BookService, IBookService
from ...types.book import BookCopy, BookReference
from .models import CreateBookReferenceRequest, RegisterBookCopyRequest

router = APIRouter()

@router.post("/", dependencies=[Depends(AdminSecurity)])
async def create_book_reference(
    create_book_reference: CreateBookReferenceRequest,
    book_service: Annotated[IBookService, Depends(BookService)]
):
    print("test")
    book_ref = BookReference()
    book_ref.title = create_book_reference.title
    book_ref.author = create_book_reference.author
    book_ref.published_date = create_book_reference.published_date

    copies: list[BookCopy] = []

    for copy in create_book_reference.copies:
        book_copy = BookCopy()
        book_copy.condition = copy.condition
        copies.append(book_copy)

    result = await book_service.create_book_reference(book_ref, copies=copies)
    print(result)
    return {"message": "ok"}


@router.post("/{book_reference_id}/register", dependencies=[Depends(AdminSecurity)])
async def register_book_copy(
    register_book_copy: RegisterBookCopyRequest
):
    pass

@router.get("/")
async def public():
    print("test")
    return 'public route'

# @router.get("/{book_id}")
# def get_book_by_id():
#     return {"message": "ok"}

# @router.delete("/{book_id}")
# def delete_book():
#     return {"message": "ok"}

# @router.get("/search")
# def search_book():
#     return {"message": "ok"}



