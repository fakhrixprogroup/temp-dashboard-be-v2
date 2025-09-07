import shutil
import os
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File
from app.schemas.sys_schema import BaseResponse, TokenData
from app.utils.sys import get_current_user

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    user: TokenData = Depends(get_current_user)
):
    upload_dir = f"uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return BaseResponse(
        message="File uploaded successfully",
        data={ "url": file_path }
    )