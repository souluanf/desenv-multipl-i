from config.database import get_db
from domain.dto.dtos import UserCreateDTO, UserUpdateDTO
from repository.user_repository import UserRepository
from service.user_service import UserService


def main():
    with get_db() as session:
        user_repository = UserRepository(session)
        user_service = UserService(user_repository)

        user_create = UserCreateDTO(
            name='John Doe',
            email='email@email.com',
            phone='1199999999',
            password='123123',
            cpf='111.111.111-11',
        )

        user = user_service.create_user(user_create)
        print(f'User created with id {user.id}')

        user_read = user_service.read_user(user.id)
        print(f'User read: {user_read}')

        user_update = UserUpdateDTO(name='Jane Doe')
        user_updated = user_service.update_user(user.id, user_update)
        print(f'User updated: {user_updated}')

        user_delete = user_service.delete_user(user.id)
        print(f'User deleted with id {user_delete}')


if __name__ == '__main__':
    main()
