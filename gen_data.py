import csv, random, os
from datetime import datetime, timedelta

random.seed(42)
os.makedirs('data', exist_ok=True)

num_customers = 80
num_products = 60
num_orders = 140
num_reviews = 160

first_names = [
    "Alice","Brianna","Carlos","Diana","Ethan","Fatima","Gavin","Hannah","Ivan","Jasmine",
    "Kareem","Lila","Mason","Nora","Omar","Priya","Quinn","Ravi","Sara","Tariq",
    "Uma","Victor","Willow","Xavier","Yara","Zane","Leo","Maya","Noah","Olivia",
    "Parker","Rosa","Sophie","Trent","Uriah","Valerie","Wes","Ximena","Yusuf","Zelda"
]
last_names = [
    "Martin","Patel","Mendes","Chen","Rogers","Khan","Lewis","Jones","Novak","Ortiz",
    "Singh","Freeman","Lopez","Garcia","Hassan","Iyer","Jenkins","Kim","Larsen","Morales",
    "Nguyen","Owens","Peters","Quintana","Reed","Sharma","Turner","Underwood","Vega","White",
    "Xu","Young","Zimmerman","Alvarez","Bates","Castro","Dunn","Ellis","Fowler","Griffin"
]

def random_phone():
    return f"+1-{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"

countries = ["USA","Canada","UK","Germany","Australia","India"]
loyalty = ["Bronze","Silver","Gold","Platinum"]

start_signup = datetime(2021,1,1)

def random_date(start, end):
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=seconds)

customers = []
for i in range(1, num_customers+1):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = name.lower().replace(' ', '.') + f"{i}@example.com"
    signup = random_date(start_signup, datetime(2024,12,31))
    customers.append({
        "customer_id": f"C{i:04d}",
        "name": name,
        "email": email,
        "phone": random_phone(),
        "signup_date": signup.strftime('%Y-%m-%d'),
        "country": random.choice(countries),
        "loyalty_tier": random.choices(loyalty, weights=[0.4,0.3,0.2,0.1])[0]
    })

categories = ["Electronics","Home","Fitness","Outdoors","Accessories","Gaming"]
product_names = {
    "Electronics": ["Smart Speaker","4K Monitor","Wireless Earbuds","Smartphone","Action Camera"],
    "Home": ["Robot Vacuum","Air Purifier","Espresso Machine","Smart Thermostat","LED Strip Lights"],
    "Fitness": ["Fitness Tracker","Yoga Mat","Adjustable Dumbbells","Rowing Machine","Smart Scale"],
    "Outdoors": ["Camping Tent","Hiking Backpack","Portable Grill","Kayak","Solar Lantern"],
    "Accessories": ["Phone Case","Portable Charger","Bluetooth Tracker","USB-C Hub","Noise-Canceling Headphones"],
    "Gaming": ["Gaming Console","VR Headset","Mechanical Keyboard","Gaming Chair","Graphics Tablet"]
}

products = []
product_id = 1
for cat, names in product_names.items():
    for _ in range(10):
        name = random.choice(names)
        price = round(random.uniform(25, 1200), 2)
        products.append({
            "product_id": f"P{product_id:04d}",
            "name": name,
            "category": cat,
            "price": price,
            "stock": random.randint(50, 500),
            "rating": round(random.uniform(3.5,5.0),1)
        })
        product_id += 1
        if len(products) >= num_products:
            break
    if len(products) >= num_products:
        break

shipping_methods = ["Standard","Express","Two-Day"]
order_statuses = ["Pending","Processing","Shipped","Delivered","Returned"]

orders = []
order_totals = {}
order_dates = {}
for i in range(1, num_orders+1):
    customer = random.choice(customers)
    order_date = random_date(datetime(2022,1,1), datetime(2024,12,31))
    orders.append({
        "order_id": f"O{i:05d}",
        "customer_id": customer["customer_id"],
        "order_date": order_date.strftime('%Y-%m-%d'),
        "status": random.choices(order_statuses, weights=[0.1,0.2,0.4,0.25,0.05])[0],
        "shipping_method": random.choice(shipping_methods),
        "city": random.choice(["New York","Toronto","London","Berlin","Sydney","Mumbai"])
    })
    order_totals[f"O{i:05d}"] = 0
    order_dates[f"O{i:05d}"] = order_date

order_items = []
order_item_id = 1
for order in orders:
    num_items = random.randint(1,5)
    selected_products = random.sample(products, num_items)
    for product in selected_products:
        quantity = random.randint(1,4)
        unit_price = product["price"] * random.uniform(0.9,1.1)
        unit_price = round(unit_price,2)
        line_total = round(unit_price * quantity,2)
        order_totals[order["order_id"]] += line_total
        order_items.append({
            "order_item_id": f"OI{order_item_id:06d}",
            "order_id": order["order_id"],
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": line_total
        })
        order_item_id += 1

for order in orders:
    order["total_amount"] = round(order_totals[order["order_id"]],2)

review_texts = [
    "Excellent quality and fast shipping!",
    "Product works as expected.",
    "Good value for the price.",
    "Satisfied overall, but packaging could be better.",
    "Exceeded my expectations!",
    "Decent, but I had to contact support.",
    "Would recommend to friends.",
    "Battery life could be longer.",
    "Love the design and functionality.",
    "Not as described, requested refund."
]

reviews = []
for i in range(1, num_reviews+1):
    order = random.choice(orders)
    order_id = order["order_id"]
    customer_id = order["customer_id"]
    order_products = [item for item in order_items if item["order_id"] == order_id]
    product = random.choice(order_products)
    review_date = order_dates[order_id] + timedelta(days=random.randint(1,30))
    reviews.append({
        "review_id": f"R{i:05d}",
        "order_id": order_id,
        "product_id": product["product_id"],
        "customer_id": customer_id,
        "rating": random.randint(1,5),
        "review_text": random.choice(review_texts),
        "review_date": review_date.strftime('%Y-%m-%d')
    })

files = [
    ("data/customers.csv", customers, ["customer_id","name","email","phone","signup_date","country","loyalty_tier"]),
    ("data/products.csv", products, ["product_id","name","category","price","stock","rating"]),
    ("data/orders.csv", orders, ["order_id","customer_id","order_date","status","shipping_method","city","total_amount"]),
    ("data/order_items.csv", order_items, ["order_item_id","order_id","product_id","quantity","unit_price","line_total"]),
    ("data/reviews.csv", reviews, ["review_id","order_id","product_id","customer_id","rating","review_text","review_date"])
]

for path, rows, headers in files:
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
