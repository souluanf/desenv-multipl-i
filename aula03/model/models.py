from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship

from config.database import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    cpf = Column(String(11))
    phone = Column(String(11))

    endereco_id = Column(Integer, ForeignKey('enderecos.id', ondelete='CASCADE'))
    endereco = relationship('Endereco', back_populates='usuario', uselist=False, cascade="all, delete")

    def create(self, session: Session):
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    def update(self, session: Session, user_data):
        for key, value in user_data.items():
            setattr(self, key, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        user_id = self.id
        session.delete(self)
        session.commit()
        return user_id

    def read(self, session: Session, user_id):
        return session.query(User).filter(User.id == user_id).first()

    def __repr__(self):
        return f'<User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, cpf={self.cpf}, phone={self.phone}, endereco={self.endereco})>'


class Endereco(Base):
    __tablename__ = 'enderecos'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cep = Column(String(8))
    logradouro = Column(String(50))
    numero = Column(String(10))
    complemento = Column(String(50))
    bairro = Column(String(50))
    cidade = Column(String(50))
    estado = Column(String(2))
    usuario = relationship('User', back_populates='endereco', uselist=False)

    def update(self, session: Session, endereco_data):
        for key, value in endereco_data.items():
            setattr(self, key, value)
        session.commit()
        session.refresh(self)
        return self

    def read(self, session: Session, endereco_id):
        return session.query(Endereco).filter(Endereco.id == endereco_id).first()

    def __repr__(self):
        return f'<Endereco(id={self.id}, cep={self.cep}, logradouro={self.logradouro}, numero={self.numero}, complemento={self.complemento}, bairro={self.bairro}, cidade={self.cidade}, estado={self.estado})>'


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
