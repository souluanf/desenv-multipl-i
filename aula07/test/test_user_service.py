from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from domain.dto.dtos import UserCreateDTO, UserUpdateDTO
from domain.model.models import User
from service.user_service import UserService


@pytest.fixture
def mock_user_repo():
    return Mock()


@pytest.fixture
def user_service(mock_user_repo):
    return UserService(mock_user_repo)


def test_create_user_success(mock_user_repo, user_service):
    user_data = UserCreateDTO(name="John Doe", email="john@example.com", password="securepassword", cpf="12345678901",
                              phone="1234567890")
    mock_user = User(id=1, **user_data.model_dump())
    mock_user_repo.create.return_value = mock_user

    result = user_service.create_user(user_data)

    assert result.email == "john@example.com"
    mock_user_repo.create.assert_called_once()


def test_create_user_failure(mock_user_repo, user_service):
    user_data = UserCreateDTO(name="John Doe", email="john@example.com", password="securepassword", cpf="12345678901", phone="1234567890")
    mock_user_repo.create.side_effect = IntegrityError(None, None, BaseException("User already exists"))

    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(user_data)

    assert exc_info.value.status_code == 409
    assert "User already exists" in str(exc_info.value.detail)


def test_read_user_success(mock_user_repo, user_service):
    user = User(id=1, name="John Doe", email="john@example.com", password="securepassword", cpf="12345678901",
                phone="1234567890")
    mock_user_repo.read.return_value = user

    result = user_service.read_user(1)

    assert result.id == 1
    assert result.name == "John Doe"
    mock_user_repo.read.assert_called_once_with(1)


def test_read_user_not_found(mock_user_repo, user_service):
    mock_user_repo.read.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.read_user(999)

    assert exc_info.value.status_code == 404
    assert "User not found" in str(exc_info.value.detail)


def test_delete_user_success(mock_user_repo, user_service):
    user = User(
        id=1,
        name="John Doe",
        email="john@email.com",
        password="securepassword",
        cpf="12345678901",
        phone="1234567890"
    )

    mock_user_repo.read.return_value = user
    mock_user_repo.delete.return_value = 1

    result = user_service.delete_user(1)

    assert result == 1
    mock_user_repo.delete.assert_called_once_with(user)


def test_delete_user_not_found(mock_user_repo, user_service):
    mock_user_repo.read.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.delete_user(999)

    assert exc_info.value.status_code == 404
    assert "User not found" in str(exc_info.value.detail)


def test_update_user_success(mock_user_repo, user_service):
    original_user = User(id=1, name="John Doe", email="john@example.com", password="secure", cpf="12345678901",
                         phone="1234567890")
    user_update_data = UserUpdateDTO(email="updatedjohn@example.com")
    updated_user = User(id=1, name="John Doe", email="updatedjohn@example.com", password="secure", cpf="12345678901",
                        phone="1234567890")

    mock_user_repo.read.return_value = original_user
    mock_user_repo.update.return_value = updated_user

    result = user_service.update_user(1, user_update_data)

    assert result.email == "updatedjohn@example.com"
    mock_user_repo.update.assert_called_once()
    assert mock_user_repo.update.call_args[0][
               0].email == "updatedjohn@example.com"


def test_update_user_not_found(mock_user_repo, user_service):
    user_update_data = UserUpdateDTO(email="updatedjohn@example.com")
    mock_user_repo.read.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.update_user(999, user_update_data)

    assert exc_info.value.status_code == 404
    assert "User not found" in str(exc_info.value.detail)
    mock_user_repo.read.assert_called_once_with(999)


def test_find_all_users(mock_user_repo, user_service):
    users = [
        User(
            id=1,
            name="John Doe",
            email="jane@teste.com",
            password="securepassword",
            cpf="12345678901",
            phone="1234567890"
        ),
        User(
            id=2,
            name="Jane Doe",
            email="jane@teste.com",
            password="securepassword",
            cpf="12345678901",
            phone="1234567890"
        )
    ]
    mock_user_repo.find_all.return_value = users

    result = user_service.find_all()

    assert len(result) == 2
    assert result[0].name == "John Doe"
    assert result[1].name == "Jane Doe"
    mock_user_repo.find_all.assert_called_once()
