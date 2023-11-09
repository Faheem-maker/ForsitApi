from fastapi import FastAPI

from controllers import products

app = FastAPI()

app.include_router(products.router, prefix='/products')

@app.get('/')
async def root():
    return {
        "message": "Hello world"
    }