from fastapi import APIRouter, Depends

from src.api.security.auth import PublicSecurity

router = APIRouter()

@router.get('/ping', dependencies=[Depends(PublicSecurity)])
async def fake():
    return {
        "message": "pong"
    }
