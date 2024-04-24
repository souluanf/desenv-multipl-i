from pydantic import parse_obj_as

from domain.dto.dtos import UserCreateDTO, UserDTO, UserUpdateDTO
from domain.model.models import User
from repository.user_repository import IUserRepository


class IUserService:

    def create_user(self, user_data: object):
        raise NotImplementedError

    def read_user(self, user_id: int):
        raise NotImplementedError

    def update_user(self, user_id: int, user_update: object):
        raise NotImplementedError

    def delete_user(self, user_id: int):
        raise NotImplementedError


class UserService(IUserService):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: UserCreateDTO) -> UserDTO:
        user = User(**user_data.dict())
        created_user = self.user_repository.create(user)
        return parse_obj_as(UserDTO, created_user)

    def read_user(self, user_id: int) -> UserDTO:
        user = self.user_repository.read(user_id)
        if user is None:
            raise Exception('User not found')
        return parse_obj_as(UserDTO, user)

    def update_user(self, user_id: int, user_data: UserUpdateDTO) -> UserDTO:
        user = self.user_repository.read(user_id)
        if user is None:
            raise Exception('User not found')

        user_data = user_data.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        updated_user = self.user_repository.update(user, user_data)
        return parse_obj_as(UserDTO, updated_user)

    def delete_user(self, user_id: int) -> int:
        user = self.user_repository.read(user_id)
        if user is None:
            raise Exception('User not found')
        return self.user_repository.delete(user)
