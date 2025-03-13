from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ...services.loan_service import ILoanService, LoanService
from ..loan.models import BorrowingRequest, ReturningRequest
from ..security.auth import APISecurity

router = APIRouter()

@router.post("/borrowing", dependencies=[Depends(APISecurity)])
async def borrowing(
    borrowing_request: BorrowingRequest,
    loan_service: Annotated[ILoanService, Depends(LoanService)]
    ):
    processed = await loan_service.borrowing(borrowing_request.book_copy_id)
    if not processed:
        raise HTTPException(status_code=403, detail="Not processed")
    else:
        return {"message": "processed"}

@router.post("/returning", dependencies=[Depends(APISecurity)])
async def returning(
    returning_request: ReturningRequest,
    loan_service: Annotated[ILoanService, Depends(LoanService)]
    ):
    await loan_service.returning(returning_request.book_copy_id)
