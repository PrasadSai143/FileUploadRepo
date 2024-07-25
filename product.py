
from fastapi import File, Form, UploadFile
from pydantic import BaseModel


class ProductRequest(BaseModel):
    name: str = Form(...)
    price: float = Form(...)
    fileup: UploadFile = File(...)