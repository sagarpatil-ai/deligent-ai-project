import csv
import os
import sqlite3

DATA_DIR = 'data'
DB_DIR = 'database'
DB_PATH = os.path.join(DB_DIR, 'ecommerce.db')

FILES = {
    'customers': os.path.join(DATA_DIR, 'customers.csv'),
    'products': os.path.join(DATA_DIR, 'products.csv'),
    'orders': os.path.join(DATA_DIR, 'orders.csv'),
    'order_items': os.path.join(DATA_DIR, 'order_items.csv'),
    'reviews': os.path.join(DATA_DIR, 'reviews.csv'),
}

os.makedirs(DB_DIR, exist_ok=True)

if not all(os.path.exists(path) for path in FILES.values()):
    missing = [name for name, path in FILES.items() if not os.path.exists(path)]
    raise FileNotFoundError(f"Missing source files: {missing}")


def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def parse_int(value):
    return int(value) if value != '' else None


def parse_float(value):
    return float(value) if value != '' else None


customers = load_csv(FILES['customers'])
products = load_csv(FILES['products'])
orders = load_csv(FILES['orders'])
order_items = load_csv(FILES['order_items'])
reviews = load_csv(FILES['reviews'])

conn = sqlite3.connect(DB_PATH)
conn.execute('PRAGMA foreign_keys = ON;')
cur = conn.cursor()

schema_statements = [
    "DROP TABLE IF EXISTS reviews",
    "DROP TABLE IF EXISTS order_items",
    "DROP TABLE IF EXISTS orders",
    "DROP TABLE IF EXISTS products",
    "DROP TABLE IF EXISTS customers",
    '''CREATE TABLE customers (
        customer_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        signup_date TEXT,
        country TEXT,
        loyalty_tier TEXT
    )''',
    '''CREATE TABLE products (
        product_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        price REAL,
        stock INTEGER,
        rating REAL
    )''',
    '''CREATE TABLE orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        order_date TEXT,
        status TEXT,
        shipping_method TEXT,
        city TEXT,
        total_amount REAL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )''',
    '''CREATE TABLE order_items (
        order_item_id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        quantity INTEGER,
        unit_price REAL,
        line_total REAL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )''',
    '''CREATE TABLE reviews (
        review_id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        customer_id TEXT NOT NULL,
        rating INTEGER,
        review_text TEXT,
        review_date TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )'''
]

for stmt in schema_statements:
    cur.execute(stmt)

cur.executemany(
    '''INSERT INTO customers VALUES (:customer_id,:name,:email,:phone,:signup_date,:country,:loyalty_tier)''',
    customers
)

cur.executemany(
    '''INSERT INTO products VALUES (:product_id,:name,:category,:price,:stock,:rating)''',
    [
        {
            **p,
            'price': parse_float(p['price']),
            'stock': parse_int(p['stock']),
            'rating': parse_float(p['rating'])
        }
        for p in products
    ]
)

cur.executemany(
    '''INSERT INTO orders VALUES (:order_id,:customer_id,:order_date,:status,:shipping_method,:city,:total_amount)''',
    [
        {
            **o,
            'total_amount': parse_float(o['total_amount'])
        }
        for o in orders
    ]
)

cur.executemany(
    '''INSERT INTO order_items VALUES (:order_item_id,:order_id,:product_id,:quantity,:unit_price,:line_total)''',
    [
        {
            **oi,
            'quantity': parse_int(oi['quantity']),
            'unit_price': parse_float(oi['unit_price']),
            'line_total': parse_float(oi['line_total'])
        }
        for oi in order_items
    ]
)

cur.executemany(
    '''INSERT INTO reviews VALUES (:review_id,:order_id,:product_id,:customer_id,:rating,:review_text,:review_date)''',
    [
        {
            **r,
            'rating': parse_int(r['rating'])
        }
        for r in reviews
    ]
)

conn.commit()

for table in ['customers','products','orders','order_items','reviews']:
    cur.execute(f'SELECT COUNT(*) FROM {table}')
    count = cur.fetchone()[0]
    print(f"{table}: {count} rows inserted")

conn.close()
