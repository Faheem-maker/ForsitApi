from fastapi import FastAPI

from controllers import products, sales, stock

app = FastAPI()

app.include_router(products.router, prefix='/products')
app.include_router(sales.router, prefix='/sales')
app.include_router(stock.router, prefix='/stock')