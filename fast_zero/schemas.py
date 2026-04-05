from pydantic import BaseModel, EmailStr

class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

# O que a API responde publicamente (Sem a senha!)
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

# Como o dado fica no Banco de Dados
class UserDB(UserSchema):
    id: int