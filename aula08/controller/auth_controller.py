from fastapi import APIRouter, Header

from domain.dto.dtos import TokenResponseDto, UserTokenDataDto
from service.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

auth_service = AuthService()


@auth_router.post("/token", status_code=201, response_model=TokenResponseDto)
async def auth_token_endpoint(secret: str = Header(alias="secret")):
    return auth_service.create_access_token(secret_key=secret)


@auth_router.get("/validate", status_code=200, response_model=UserTokenDataDto)
async def validate_token_endpoint(authorization: str = Header(alias="Authorization")):
    return auth_service.validate_token(token=authorization)
