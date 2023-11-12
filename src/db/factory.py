# Add the parent to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.category import Category
from models.Product import Product
from models.Orders import Orders
from models.orders_products import OrdersProducts

num_categories = 20
num_products = 100
num_orders = 1000

def generate_categories(num_categories):
    for i in range(1, num_categories + 1):
        title = f'Category {i}'
        Category.create(title=title)

def generate_products(num_products):
    categories = Category.select()

    # Assuming your Product model already exists
    for i in range(1, num_products + 1):
        name = f'Product {i}'
        price = 100 * i
        created_at = '2023-11-12'
        category_id = categories[i % len(categories)].id
        qty = 50 + i
        minimum_qty = 10

        Product.create(
            name=name,
            price=price,
            created_at=created_at,
            category_id=category_id,
            qty=qty,
            minimum_qty=minimum_qty
        )

def generate_order_products(num_order_products, order_id):
    products = Product.select(Product.id)

    # Assuming your OrderProduct model already exists
    for i in range(1, num_order_products + 1):
        product_id = products[i % len(products)].id  # Cycle through existing product_ids
        product_rate = 100 * i  # Replace this with your desired product rate logic
        product_qty = 2 * i  # Replace this with your desired product quantity logic
        tax_amount = 0.1 * product_rate  # Replace this with your desired tax calculation logic

        # Assuming your OrderProduct model is named OrderProduct and has the specified fields
        OrdersProducts.create(
            order_id=order_id,
            product_id=product_id,
            product_rate=product_rate,
            product_qty=product_qty,
            tax_amount=tax_amount
        )

def generate_orders(num_orders):
    for i in range(1, num_orders):

        order = Orders.create()

        generate_order_products(5, order.id)

        order.base_amount = sum(op.product_rate * op.product_qty for op in order.entries)
        order.tax_amount = sum(op.tax_amount for op in order.entries)
        order.discount_amount = 0

        order.doctype = 'SI'

        order.save()

generate_categories(num_categories)

generate_products(num_products)

generate_orders(num_orders)