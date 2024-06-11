import logging

from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError

from domain.dto.dtos import UserCreateDTO, UserDTO, UserUpdateDTO
from domain.model.models import User
from messaging.rabbitmq_producer import RabbitMQProducer
from repository.user_repository import IUserRepository

logger = logging.getLogger("fastapi")


class IUserService:

    def create_user(self, user_data: object):
        raise NotImplementedError

    def read_user(self, user_id: int):
        raise NotImplementedError

    def update_user(self, user_id: int, user_update: object):
        raise NotImplementedError

    def delete_user(self, user_id: int):
        raise NotImplementedError


rabbitmq_producer = RabbitMQProducer(queue='user_events')


class UserService(IUserService):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: UserCreateDTO) -> UserDTO:
        user = User(**user_data.model_dump())
        try:
            logger.info("Creating user: %s", user)
            created_user = self.user_repository.create(user)
            rabbitmq_producer.publish({"event": "create_user", "user": user_data.dict()})
        except IntegrityError as e:
            logger.error("Error creating user: %s. Detail: %s", user, e)
            raise HTTPException(status_code=409, detail=f"User already exists. Error: {e.args[0]}")
        return TypeAdapter(UserDTO).validate_python(created_user)

    def read_user(self, user_id: int) -> UserDTO:
        logger.info("Reading user with id %s", user_id)
        user = self.user_repository.read(user_id)
        if user is None:
            logger.error("User with id %s not found", user_id)
            raise HTTPException(status_code=404, detail="User not found")
        return TypeAdapter(UserDTO).validate_python(user)

    def find_all(self) -> list[UserDTO]:
        logger.info("Finding all users")
        users = self.user_repository.find_all()
        return [TypeAdapter(UserDTO).validate_python(user) for user in users]

    def update_user(self, user_id: int, user_data: UserUpdateDTO) -> UserDTO:
        logger.info("Updating user with id %s", user_id)
        user = self.user_repository.read(user_id)
        if user is None:
            logger.error("User with id %s not found", user_id)
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user_data.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        updated_user = self.user_repository.update(user, user_data)
        rabbitmq_producer.publish({"event": "update_user", "user": user_data})
        return TypeAdapter(UserDTO).validate_python(updated_user)

    def delete_user(self, user_id: int) -> int:
        logger.info("Deleting user with id %s", user_id)
        user = self.user_repository.read(user_id)
        if user is None:
            logger.error("User with id %s not found", user_id)
            raise HTTPException(status_code=404, detail="User not found")
        delete_id = self.user_repository.delete(user)
        rabbitmq_producer.publish({"event": "delete_user", "user_id": user_id})
        return delete_id
