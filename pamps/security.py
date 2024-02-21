"""Security utilities"""
import bcrypt

from pamps.config import settings

SECRET_KEY = settings.security.secret_key
ALGORITHM = settings.security.algorithm

def verify_password(plain_password, hashed_password) -> bool:
    """Verifica um hash em relação a uma senha"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def get_password_hash(password) -> bytes:
    """Gera um hash a partir de um texto simples"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

class HashedPassword(str):
    """Aceita uma senha em texto simples e a hash.
    Use isso como um campo em seu SQLModel
    class User(SQLModel, table=True):
        username: str
        password: HashedPassword
    """
    def __new__(cls, plain_text):
        # converte para string
        plain_text = str(plain_text)
        # print("3-Received plain_text:", plain_text) 

        # Ao criar uma instância, geramos o hash da senha em texto simples
        hashed_password = get_password_hash(plain_text)
        return super().__new__(cls, hashed_password)

    @classmethod
    def __get_validators__(cls):
        # Um ou mais validadores podem ser gerados, que serão chamados na ordem para validar a entrada.
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Aceita uma senha em texto simples e retorna uma senha hash."""
        if not isinstance(v, str):
            raise TypeError("string required")

        # O argumento v agora será considerado como um hash em vez de uma senha em texto simples
        return cls(v)
