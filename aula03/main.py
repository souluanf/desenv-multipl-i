from config.database import get_db
from model.models import User, Endereco


def main():
    name = 'John Doe'
    email = 'email@email.com'
    phone = '1199999999'
    password = '123123'
    cpf = '12312312312'

    with get_db() as session:
        user = User(name=name, email=email, phone=phone, password=password, cpf=cpf)
        endereco = Endereco(cep='555555', logradouro='rua', numero='123', complemento='casa', bairro='bairro',
                            cidade='cidade', estado='SP')

        user.endereco = endereco
        user.create(session=session)
        user_id = user.id
        print(f'User created with id {user_id}')

        user_read = user.read(session=session, user_id=user_id)
        print(f'User read: {user_read}')
        print(str(user_read))

        user_data = {'name': 'Jane Doe'}
        user_update = user.update(session=session, user_data=user_data)
        print(f'User updated: {user_update}')

        endereco_data = {'cep': '111111'}
        user.endereco.update(session=session, endereco_data=endereco_data)
        print(f'Endereco updated: {user.endereco}')

        user_delete = user.delete(session=session)
        print(f'User deleted with id {user_delete}')


if __name__ == '__main__':
    main()
