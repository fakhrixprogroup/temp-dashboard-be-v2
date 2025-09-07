import base64
from datetime import datetime, timedelta
import os
import shutil
from uuid import uuid4
from fastapi import Depends, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.database import async_session

from jose import jwt, JWTError

from app.schemas.sys_schema import TokenData

SECRET_KEY = os.getenv("SECRET_KEY", "temp_dashboard_rest_cuiiiii!!!!!!!!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

async def get_db():
    async with async_session() as session:
        yield session

bearer_scheme = HTTPBearer()

async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token tidak valid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = creds.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None:
            raise credentials_exception
        return TokenData(user_id=user_id, role=role)

    except JWTError:
        raise credentials_exception

async def upload_photo(
    user: TokenData = Depends(get_current_user),
    file: UploadFile | None = None
):
    print(f"masuk sini : {file}")
    if file:
        print(f"masuk file : {file}")
        upload_dir = f"uploads/{user.user_id}"
        os.makedirs(upload_dir, exist_ok=True)

        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid4()}.{file_extension}"  
        file_path = os.path.join(upload_dir, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return { "url": f"{upload_dir}/{unique_filename}" }

def create_access_token(data: dict, expires_delta: timedelta = None):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"error create_access_token : {e}")
        return None

def get_basic_auth_header(username: str, password: str) -> dict:
    auth_value = f"{username}:{password}"
    encoded_auth = base64.b64encode(auth_value.encode()).decode("utf-8")
    return {"Authorization": f"Basic {encoded_auth}", "api-version": "2024-11-11"}