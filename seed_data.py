import psycopg2
import os
from dotenv import load_dotenv
from faker import Faker
import random

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def seed_database():
    fake = Faker()
    conn = get_connection()
    cur = conn.cursor()

    # 1. Create Tables
    print("Creating tables...")
    cur.execute("""
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            customer_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            city VARCHAR(50)
        );

        CREATE TABLE products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(100),
            category VARCHAR(50),
            price DECIMAL(10, 2)
        );

        CREATE TABLE orders (
            order_id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES customers(customer_id),
            order_date DATE,
            total_amount DECIMAL(10, 2)
        );

        CREATE TABLE order_items (
            item_id SERIAL PRIMARY KEY,
            order_id INT REFERENCES orders(order_id),
            product_id INT REFERENCES products(product_id),
            quantity INT
        );
    """)

    # 2. Insert 300 Customers
    print("Seeding Customers...")
    for _ in range(300):
        cur.execute("INSERT INTO customers (name, email, city) VALUES (%s, %s, %s)",
                    (fake.name(), fake.email(), fake.city()))

    # 3. Insert 300 Products
    print("Seeding Products...")
    categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Toys']
    for _ in range(300):
        cur.execute("INSERT INTO products (product_name, category, price) VALUES (%s, %s, %s)",
                    (fake.catch_phrase(), random.choice(categories), round(random.uniform(10, 500), 2)))

    # 4. Insert 300 Orders
    print("Seeding Orders...")
    for _ in range(300):
        cur.execute("INSERT INTO orders (customer_id, order_date, total_amount) VALUES (%s, %s, %s)",
                    (random.randint(1, 300), fake.date_this_year(), round(random.uniform(50, 2000), 2)))

    # 5. Insert 300 Order Items
    print("Seeding Order Items...")
    for _ in range(300):
        cur.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                    (random.randint(1, 300), random.randint(1, 300), random.randint(1, 5)))

    conn.commit()
    cur.close()
    conn.close()
    print("Database seeded successfully with 1,200 total rows!")

if __name__ == "__main__":
    seed_database()