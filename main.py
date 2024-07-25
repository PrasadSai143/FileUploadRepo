import json
import os
import random
from typing import Any
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
from product import  ProductRequest 

from fastapi.responses import FileResponse

from productsreponse import ProductResponse

app = FastAPI()

origins = [
    'http://localhost:4200',
    'http://localhost:3000',
    'http://localhost',
    'http:localhost:8000'
]

app.add_middleware(CORSMiddleware,allow_origins = origins,allow_credentials=True, allow_methods=["*"], allow_headers=["*"] )

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    UPLOAD_DIRECTORY = "uploaded_files"
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    with open(f"uploaded_files/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}

@app.get("/getfile/{filename}")
async def get_file(filename: str):
    UPLOAD_DIRECTORY = "uploaded_files"
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

@app.get("/getproducts", response_model=Any)
async def get_products():
    UPLOAD_DIRECTORY = "uploaded_files"
    productlist = []
    with open('product.json', 'r') as file:
        products = json.load(file)
    
    for item in products['Products']:
        productRes = ProductResponse(id = item['id'],name = item['name'],price = item['price'], photo =f"http://127.0.0.1:8000/getfile/{item['photo']}")
        productlist.append(productRes)
    return productlist

@app.post("/createproduct", response_model=Any)
async def create_product( name: str = Form(...),price: float = Form(...),fileup: UploadFile = File(...)):
    try:
        UPLOAD_DIRECTORY = "uploaded_files"
        json_filepath = 'product.json'
        if not os.path.exists(UPLOAD_DIRECTORY):
            os.makedirs(UPLOAD_DIRECTORY)

        file_path = os.path.join(UPLOAD_DIRECTORY, fileup.filename)

        if os.path.exists(file_path):
            return "File found"
        
        new_product = {"id": random.randint(0, 10), "name":name, "price": price, "photo": fileup.filename}
        with open(json_filepath, 'r') as file:
            products = json.load(file)
            products['Products'].append(new_product)
            print("Current products:", products['Products'])
         
        with open(json_filepath, 'w') as file:
            json.dump(products, file)
        with open(f"uploaded_files/{fileup.filename}", "wb") as buffer:
            shutil.copyfileobj(fileup.file, buffer)

        return new_product
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Internal server error")
             








if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port = 8000)