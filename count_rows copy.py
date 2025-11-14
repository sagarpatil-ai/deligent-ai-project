import csv
import os

files = ['customers','products','orders','order_items','reviews']
for name in files:
    path = os.path.join('data', f'{name}.csv')
    with open(path, newline='', encoding='utf-8') as f:
        count = sum(1 for _ in f) - 1
    print(f"{name}: {count} rows")
