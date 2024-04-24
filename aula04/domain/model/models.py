from sqlalchemy import Column, Integer, String

from config.database import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    cpf = Column(String(11))
    phone = Column(String(11))

    def __repr__(self):
        return f'<User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, cpf={self.cpf}, phone={self.phone})>'


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)