import sqlite3
import os

def setup_database(db_name="database/retail_shop.db"):
    # Ensure database directory exists
    os.makedirs(os.path.dirname(db_name), exist_ok=True)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, 
            category TEXT, price REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Sales (
            sale_id INTEGER PRIMARY KEY, product_id INTEGER, 
            quantity INTEGER, sale_date TEXT, 
            FOREIGN KEY (product_id) REFERENCES Products(product_id))''')

    cursor.execute("SELECT COUNT(*) FROM Products")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO Products (name, category, price) VALUES (?, ?, ?)', [
            ('Deep Freezer 300L', 'Appliances', 25000.00),
            ('Wireless Controller', 'Gaming', 1500.00),
            ('Laptop 15-inch', 'Electronics', 55000.00)
        ])
        cursor.executemany('INSERT INTO Sales (product_id, quantity, sale_date) VALUES (?, ?, ?)', [
            (1, 1, '2026-09-01'), (2, 3, '2026-09-03'), (3, 2, '2026-09-05')
        ])
        conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()