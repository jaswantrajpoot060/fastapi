from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
import pyodbc
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status
import jwt
from jwt import encode
import config
from employeeModel import Employee
from connection_db import connect_to_database
from employeeServices import getall_employee, get_employee, createdata_employee, updatedata_employee, \
    delete_data_employee
from jwtconfig import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

app = FastAPI()

@app.get("/employee")
async def get_all_employee(conn=Depends(connect_to_database)):
    return getall_employee(conn)


@app.get("/employee/{id}")
def getbyid_employee(id: int, conn=Depends(connect_to_database)):
    return get_employee(id, conn)


@app.post("/employee")
def create_employee(employee: Employee):
    return createdata_employee(employee)


@app.put("/employee/{id}")
def update_employee(id: int, employee: Employee):
    return updatedata_employee(id,employee)


@app.delete("/employee/{id}")
def delete_employee(id: int):
    return delete_data_employee(id)


# OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy database
users_db = {
    "user": {
        "username": "user",
        "password": "password"  # Note: Plain text password
    }
}

# User model
class User(BaseModel):
    username: str

# Function to authenticate user
def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user or user["password"] != password:
        return None
    return user

# Function to create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to create refresh token
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    user = users_db.get(username)
    if user is None:
        raise credentials_exception
    return User(username=username)

# Login route
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user["username"]})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Protected route
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
