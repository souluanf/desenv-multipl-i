from datetime import timedelta, datetime
from os import getenv

from dotenv import load_dotenv
from fastapi import HTTPException, status
from jwt import encode, decode, ExpiredSignatureError, DecodeError, InvalidTokenError

from domain.dto.dtos import TokenResponseDto, UserTokenDataDto

load_dotenv()

TOKEN_EXPIRE_SECONDS = int(getenv('TOKEN_EXPIRE_SECONDS'))
TOKEN_SECRET_KEY = getenv('TOKEN_SECRET_KEY')


class AuthService:

    def create_access_token(self, secret_key: str):
        self.validate_secret(secret_key)
        access_token_expires = timedelta(seconds=TOKEN_EXPIRE_SECONDS)
        expires_at = datetime.utcnow() + access_token_expires
        to_encode = {"expires_at": expires_at.isoformat()}
        access_token = encode(to_encode, secret_key, algorithm="HS256")
        return TokenResponseDto(access_token=access_token, expires_at=expires_at)

    def validate_secret(self, secret: str):
        if secret != TOKEN_SECRET_KEY:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret key")

    def validate_token(self, token: str):
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token scheme")
        token = token[len("Bearer "):]
        try:
            payload = decode(token, TOKEN_SECRET_KEY, algorithms=["HS256"])
            expires_at = datetime.fromisoformat(payload["expires_at"])
            if datetime.utcnow() > expires_at:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
            return UserTokenDataDto(**payload)
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except (DecodeError, InvalidTokenError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
