from typing import Annotated

from fastapi import Depends
from sqlalchemy import text

from ..context import ContextManager
from ..core.db import AsyncDatabaseClient

context = ContextManager()


class LoanRepository:

    connection: AsyncDatabaseClient

    def __init__(self, connection: Annotated[AsyncDatabaseClient, Depends(context.inject_db_connection)]):
        self.connection = connection

    async def borrowing(self, account_id: str, book_copy_id: str, max_loans: int = 3):
        sql = text(
            """
            INSERT INTO book_loan (book_copy_id, account_id, start_date, end_date, status)
            SELECT
                :book_copy_id,
                :account_id,
                NOW(),
                NOW() + INTERVAL '14 days',
                'borrowed'
            FROM (
                SELECT
                    (SELECT
                        COUNT(*) AS loan_count
                        FROM book_loan
                        WHERE account_id = :account_id
                        AND status IN ('borrowed')
                    ) AS user_loan_count,
                    (SELECT COUNT(*)
                        FROM book_loan
                        WHERE book_copy_id = :book_copy_id
                        AND status IN ('borrowed', 'lost')
                    ) AS book_loan_count
                ) AS conditions
            WHERE conditions.user_loan_count < 3
            AND conditions.book_loan_count = 0
            RETURNING conditions.user_loan_count, conditions.book_loan_count
            """
        )
        sql = text(
        """
        with conditions as (
            SELECT
                (SELECT
                    COUNT(*) AS loan_count
                    FROM book_loan
                    WHERE account_id = :account_id
                    AND status IN ('borrowed')
                ) AS user_loan_count,
                (SELECT COUNT(*)
                    FROM book_loan
                    WHERE book_copy_id = :book_copy_id
                    AND status IN ('borrowed', 'lost')
                ) AS book_loan_count
        )
        INSERT INTO book_loan (book_copy_id, account_id, start_date, end_date, status)
            SELECT
                :book_copy_id,
                :account_id,
                NOW(),
                NOW() + INTERVAL '14 days',
                'borrowed'
            FROM conditions
            WHERE conditions.user_loan_count < 3
            AND conditions.book_loan_count = 0
        """
        )
        async with self.connection.session() as session:
            result = await session.execute(sql, {
                "book_copy_id": book_copy_id,
                "account_id": account_id,
                "max_loans": max_loans
            })
            await session.commit()
            return result.rowcount > 0

    async def returning(self, book_copy_id: str):
        sql = text(
            """
            UPDATE book_loan
            SET status = 'returned', return_date = NOW()
            WHERE book_copy_id = :book_copy_id
            AND status IN ('borrowed', 'overdue')
            RETURNING *;
            """
        )
        async with self.connection.session() as session:
            r = await session.execute(sql, {
                "book_copy_id": book_copy_id
            })
            await session.commit()
            return r.scalar()
