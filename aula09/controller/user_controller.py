from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from config.database import get_db
from domain.dto.dtos import UserDTO, UserCreateDTO, UserUpdateDTO
from repository.user_repository import UserRepository
from service.auth_service import AuthService
from service.user_service import UserService

user_router = APIRouter(prefix="/users", tags=["Users"])

auth_service = AuthService()


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


@user_router.post("/", status_code=201, description="Busca todos os usuários", response_model=UserDTO)
def create(request: UserCreateDTO,
           user_repo: UserRepository = Depends(get_user_repo),
           authorization: str = Header(alias="Authorization")):
    auth_service.validate_token(authorization)
    user_service = UserService(user_repo)
    return user_service.create_user(request)


@user_router.get("/{user_id}", status_code=200, description="Busca um usuário pelo ID", response_model=UserDTO)
def find_by_id(user_id: int, user_repo: UserRepository = Depends(get_user_repo),
               authorization: str = Header(alias="Authorization")):
    auth_service.validate_token(authorization)
    user_service = UserService(user_repo)
    return user_service.read_user(user_id)


@user_router.get("/", status_code=200, description="Busca todos os usuários", response_model=list[UserDTO])
def find_all(user_repo: UserRepository = Depends(get_user_repo),
             authorization: str = Header(alias="Authorization")):
    auth_service.validate_token(authorization)
    user_service = UserService(user_repo)
    return user_service.find_all()


@user_router.put("/{user_id}", status_code=200, description="Atualiza um usuário", response_model=UserDTO)
def update(user_id: int, request: UserUpdateDTO, user_repo: UserRepository = Depends(get_user_repo),
           authorization: str = Header(alias="Authorization")):
    auth_service.validate_token(authorization)
    user_service = UserService(user_repo)
    return user_service.update_user(user_id, request)


@user_router.delete("/{user_id}", status_code=204, description="Deleta um usuário")
def delete(user_id: int, user_repo: UserRepository = Depends(get_user_repo),
           authorization: str = Header(alias="Authorization")):
    auth_service.validate_token(authorization)
    user_service = UserService(user_repo)
    user_service.delete_user(user_id)
