"""User related data models"""
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from pamps.security import HashedPassword
from pydantic import BaseModel
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pamps.models.post import Post


class User(SQLModel, table=True):
    """Represents the User Model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    password: str
    # it populates the .user attribute on the Post Model
    posts: List["Post"] = Relationship(back_populates="user")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Se a senha for fornecida, inicialize a instância de HashedPassword
        if "password" in kwargs:
            # print("2.1-Received kwargs:", kwargs) 
            plain_password = str(kwargs['password']) 
            self.password = HashedPassword(plain_password)

    @classmethod
    def model_validate(cls, obj):
        """Este método é chamado quando é instanciado a partir de um ORM.
        Ele converte o objeto carregado do banco de dados para a instância da classe."""
        if "password" in obj.__dict__:
            # Se o atributo 'password' está presente, assumimos que é uma senha em texto simples
            # print("2.2-Received obj:", obj) 
            obj.__dict__["password"] = HashedPassword(obj.__dict__["password"])
        return super().model_validate(obj)
    

        
class UserResponse(BaseModel):
    """Serializer for User Response"""

    username: str
    avatar: Optional[str] = None
    bio: Optional[str] = None

    
class UserRequest(BaseModel):
    """Serializer for User request payload"""

    email: str
    username: str
    password: str
    avatar: Optional[str] = None
    bio: Optional[str] = None


