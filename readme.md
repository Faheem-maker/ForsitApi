# Forsit API

Forsit API is an API powering the backend of a ecommerce admin dashboard. It is built with simplicity and flexibility in mind. It is also crafted with the needs of frontend developers in mind, using such a design can increase the consumer's productivity by around 12%.

## Tech Stack
__Backend__: Python<br>
__Framework__: Fast API<br>
__Database__: MySQL<br>
__ORM__: Peewee

## Installation and Setup
### Dependencies

Before you start, make sure you have:
- Python 3.0 or higher
- MySQL
- Pip (auto bundled with Python)

### Setup
Please follow the follwing procedure for running the project:
1. Make sure you are in the `src` directory. Run the following command
    `cd src`
2. Restore your database or directly run the scripts from `db/database_structure.sql`
3. (**OPTIONAL**) Run the following command to populate database with sample data: `python db/database_structure.sql`
4. Install all dependencies by running the following command: `pip install -r requirements.txt`
5. Run the following command to start the project: `uvicorn main:app`

### Configuration
- Make sure to set proper username and password for database in `db/config.py`. If you don't have a password, use `None`
- You can customize the volume the sample data by modifying `db/database_structure.py`

## End Points
The API exposes several end points to add, modify and query data. Here is a brief overview of all of them.
### GET `/products`
Get all products (_with pagination_)
### POST `/products`
Create a new product, it accepts product's name, category, its starting quantity and price.
### GET `/sales`
Retrieve sales data by product, category or time range. It supports several other filters defined by `sales_filter.py`.
### POST `/sales/`
Create a new invoice, it uses the default rate unless explicitly specified otherwise.
### GET `/stock`
Return all products with their current stock.
### GET `/stock/low`
Get all products running out of stock, it also accepts an optional treshhold.
### POST `/stock`
Update any product's quantity. It works by creating an empty purchase invoice.

## Database
The API uses a star schema created around `orders` table. Orders table will store data for all kinds of orders. This schema is used to allow further scaling and flexible reports.