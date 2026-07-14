from pwdlib import PasswordHash
from jose import jwt , JWTError
from dotenv import load_dotenv 
import os
load_dotenv()



password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)





SECRET_KEY=os.getenv("SECRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")

# hash and generate token 
def create_token(payload : dict):
    return jwt.encode(payload , key = SECRET_KEY , algorithm=JWT_ALGORITHM)

#decode token and return payload 
def decode_token(token : str):
     return  jwt.decode(token,key=SECRET_KEY , algorithms=JWT_ALGORITHM)