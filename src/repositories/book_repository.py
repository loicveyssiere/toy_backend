from typing import Annotated

from fastapi import Depends
from sqlalchemy import text

from ..types.user import UserAuthenticated

from ..context import ContextManager
from ..core.db import AsyncDatabaseClient
from ..types.book import BookCopy, BookReference

context = ContextManager()


class BookRepository:

    connection: AsyncDatabaseClient

    def __init__(self, connection: Annotated[AsyncDatabaseClient, Depends(context.inject_db_connection)]):
        self.connection = connection

    async def create_book_reference(self, user: UserAuthenticated, book_ref: BookReference, copies=list[BookCopy]):
        sql = text("INSERT INTO book_reference (title, author, published_date) VALUES (:title, :author, :published_date) RETURNING id")
        async with self.connection.session() as session:

            r = await session.execute(sql, {
                "title": book_ref.title,
                "author": book_ref.author,
                "published_date": book_ref.published_date
            })
            await session.commit()
            return r.scalar()

    async def register_book_copies(self, user: UserAuthenticated, ref_id: str, copies: list[BookCopy]):
        sql = text("INSERT INTO book_copy (condition, book_reference_id) VALUES (:condition, :book_reference_id) RETURNING id")
        async with self.connection.session() as session:
            for copy in copies:
                await session.execute(sql, {"condition": copy.condition, "book_reference_id": ref_id})
            await session.commit()
