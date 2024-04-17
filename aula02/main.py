import sqlite3
from abc import ABC, abstractmethod

import psycopg2


class ICrud(ABC):

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def read(self, _id):
        pass

    @abstractmethod
    def update(self, _id, data):
        pass

    @abstractmethod
    def delete(self, _id):
        pass


class DbConnection(ABC):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, ext_type, exc_val, exc_tb):
        pass


class SqliteConnection(DbConnection):

    def __init__(self, dbname):
        self.dbname = dbname + '.db'

    def __enter__(self):
        self.conn = sqlite3.connect(self.dbname)
        return self.conn

    def __exit__(self, ext_type, exc_val, exc_tb):
        self.conn.close()


class PostgresConnection(DbConnection):
    def __init__(self, dbname, user, password, host):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host

    def __enter__(self):
        self.conn = psycopg2.connect(
            database=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host
        )
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class GenericCrud(ICrud):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create(self, data):
        with self.db_connection as conn:
            cursor = conn.cursor()
            if isinstance(self.db_connection, PostgresConnection):
                placeholders = "%s, %s, %s, %s"
                returning_clause = "RETURNING _id"
            else:
                placeholders = "?, ?, ?, ?"
                returning_clause = ""
            sql = f"INSERT INTO users (email, cpf, nome, senha) VALUES ({placeholders}) {returning_clause};"
            cursor.execute(sql, (data['email'], data['cpf'], data['nome'], data['senha']))
            conn.commit()

            # Pegar o ID gerado
            if isinstance(self.db_connection, PostgresConnection):
                user_id = cursor.fetchone()[0]
            else:
                user_id = cursor.lastrowid
            return user_id

    def read(self, _id):
        with self.db_connection as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users WHERE _id = {_id}")
            return cursor.fetchone()

    def update(self, _id, data):
        with self.db_connection as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET email = %s, cpf = %s, nome = %s, senha = %s WHERE _id = %s;",
                           (data['email'], data['cpf'], data['nome'], data['senha'], _id))
            conn.commit()

    def delete(self, _id):
        with self.db_connection as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE _id = %s;", (_id,))
            conn.commit()


def create_tables(db_connection):
    with db_connection as conn:
        is_postgres = isinstance(db_connection, PostgresConnection)
        user_table_sql = """CREATE TABLE IF NOT EXISTS users (
                                _id {0} PRIMARY KEY,
                                email VARCHAR(255) NOT NULL,
                                cpf VARCHAR(11) NOT NULL UNIQUE,
                                nome VARCHAR(255) NOT NULL,
                                senha VARCHAR(255) NOT NULL
                            );""".format("SERIAL" if is_postgres else "INTEGER")
        try:
            cur = conn.cursor()
            cur.execute(user_table_sql.replace("?", "%s") if is_postgres else user_table_sql)
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()


if __name__ == '__main__':
    db_connection = PostgresConnection(dbname='users2', user='postgres', password='postgres', host='localhost')

    create_tables(db_connection)

    crud = GenericCrud(db_connection)
    user_data = {"email": "user@example.com", "cpf": "654654", "nome": "Example User", "senha": "password"}

    user_id = crud.create(user_data)
    if user_id:
        print(f"User created with ID: {user_id}")

    user = crud.read(user_id)
    if user:
        print(f"User data: {user}")

    user_data["email"] = "teste@teste.com"
    crud.update(user_id, user_data)
    user = crud.read(user_id)
    if user:
        print(f"User data updated: {user}")

    crud.delete(user_id)
    user = crud.read(user_id)
    if not user:
        print("User deleted successfully")
