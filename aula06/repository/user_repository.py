from sqlalchemy.orm import Session

from domain.model.models import User


class IUserRepository:
    def create(self, user: object):
        raise NotImplementedError

    def read(self, user_id: int):
        raise NotImplementedError

    def update(self, user: object, user_data: dict):
        raise NotImplementedError

    def delete(self, user: object):
        raise NotImplementedError

    def find_all(self):
        raise NotImplementedError


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User, user_data) -> User:
        for key, value in user_data.items():
            setattr(user, key, value)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> int:
        user_id = user.id
        self.session.delete(user)
        self.session.commit()
        return user_id

    def read(self, user_id):
        return self.session.query(User).filter(User.id == user_id).first()

    def find_all(self):
        return self.session.query(User).all()
