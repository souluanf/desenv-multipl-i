from http.client import HTTPException
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from controller.user_controller import user_router, get_user_repo
from domain.dto.dtos import UserDTO, UserUpdateDTO
from domain.model.models import User
from service.auth_service import AuthService
from service.user_service import UserService


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(user_router)
    return TestClient(app)


@pytest.fixture
def mock_user_service():
    mock = Mock(spec=UserService)
    return mock


@pytest.fixture
def mock_user_repo(mock_user_service):
    mock_repo = Mock()
    mock_repo.return_value = mock_user_service
    return mock_repo


@pytest.fixture
def auth_service():
    return AuthService()


@pytest.fixture
def mock_token(auth_service):
    return auth_service.create_access_token(secret_key='123').access_token


def test_create_user_endpoint(client, mock_user_service, mock_token):
    client.app.dependency_overrides[UserService] = lambda: mock_user_service
    user_dto = UserDTO(id=1, name="John Doe", email="john@example.com", password="securepassword", cpf="12345678901",
                       phone="1234567890")
    mock_user_service.create_user.return_value = user_dto

    response = client.post("/users/",
                           json={"name": "John Doe", "email": "john@example.com", "password": "securepassword",
                                 "cpf": "12345678901", "phone": "1234567890"},
                           headers={"Authorization": f"Bearer {mock_token}"}
                           )

    assert response.status_code == 201
    assert response.json()['email'] == "john@example.com"


def test_find_user_by_id_not_found(client, mock_user_service, mock_token):
    client.app.dependency_overrides[UserService] = lambda: mock_user_service
    mock_user_service.read_user.return_value = None

    response = client.get("/users/999",
                          headers={"Authorization": f"Bearer {mock_token}"})

    assert response.status_code == 404


def test_delete_user_success(client, mock_user_repo, mock_token):
    client.app.dependency_overrides[get_user_repo] = lambda: mock_user_repo
    user_id = 1
    user = User(id=user_id, name="John Doe", email="john@example.com", password="secure", cpf="12345678901",
                phone="1234567890")
    mock_user_repo.read.return_value = user
    mock_user_repo.delete.return_value = user_id

    response = client.delete(f"/users/{user_id}",
                             headers={"Authorization": f"Bearer {mock_token}"})

    assert response.status_code == 204
    mock_user_repo.read.assert_called_once_with(user_id)
    mock_user_repo.delete.assert_called_once_with(user)


def test_update_user_success(client, mock_user_service, mock_token):
    client.app.dependency_overrides[UserService] = lambda: mock_user_service
    user_update = UserUpdateDTO(email="newjohn@example.com")
    updated_user = UserDTO(id=1, name="John Doe", email="newjohn@example.com", password="secure", cpf="12345678901",
                           phone="1234567890")
    mock_user_service.update_user.return_value = updated_user

    response = client.put("/users/1", json=user_update.model_dump(exclude_unset=True),
                          headers={"Authorization": f"Bearer {mock_token}"})

    assert response.status_code == 200
    assert response.json()['email'] == "newjohn@example.com"


def test_update_user_not_found(client, mock_user_service, mock_token):
    client.app.dependency_overrides[UserService] = lambda: mock_user_service
    user_update = UserUpdateDTO(email="newjohn@example.com")
    mock_user_service.update_user.side_effect = HTTPException(BaseException)

    response = client.put("/users/999", json=user_update.model_dump(exclude_unset=True),
                          headers={"Authorization": f"Bearer {mock_token}"})

    assert response.status_code == 404
    assert "User not found" in response.json()['detail']


def test_find_all_users(client, mock_user_repo, mock_user_service, mock_token):
    client.app.dependency_overrides[UserService] = lambda: mock_user_service
    client.app.dependency_overrides[get_user_repo] = lambda: mock_user_repo

    mock_users = [
        User(id=1, name="John Doe", email="john@example.com", password="secure", cpf="12345678901", phone="1234567890"),
        User(id=2, name="Jane Doe", email="jane@example.com", password="secure", cpf="98765432100", phone="0987654321")
    ]

    mock_users_dto = [
        UserDTO(id=1, name="John Doe", email="john@example.com", password="secure", cpf="12345678901",
                phone="1234567890"),
        UserDTO(id=2, name="Jane Doe", email="jane@example.com", password="secure", cpf="98765432100",
                phone="0987654321")
    ]
    mock_user_repo.find_all.return_value = mock_users
    mock_user_service.find_all.return_value = mock_users_dto

    response = client.get("/users",
                          headers={"Authorization": f"Bearer {mock_token}"})

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    assert response_data[0]['email'] == "john@example.com"
    assert response_data[1]['email'] == "jane@example.com"
