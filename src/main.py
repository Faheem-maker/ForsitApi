from fastapi import FastAPI

from controllers import products, sales

app = FastAPI()

app.include_router(products.router, prefix='/products')
app.include_router(sales.router, prefix='/sales')