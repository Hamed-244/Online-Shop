import os
import sqlite3

# Specify the path where the SQLite database file will be created
database_path = 'instance/Online-shop.db'

# Check if the path to the database file exists, if not create the directories
os.makedirs(os.path.dirname(database_path), exist_ok=True)

# Check if the database file already exists
if not os.path.exists(database_path):
    # Connect to the database and create it if it doesn't exist
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    # Create tables
    cur.execute('''
        CREATE TABLE User (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone_number TEXT NOT NULL,
            registration_date DATE NOT NULL,
            role TEXT NOT NULL,
            default_shipping_address INTEGER,
            FOREIGN KEY (default_shipping_address) REFERENCES ShippingAddresses(address_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE Product (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            category_id INTEGER NOT NULL,
            image TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES Category(category_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_date DATETIME NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE OrderDetails (
            order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (product_id) REFERENCES Product(product_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE Category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            parent_category_id INTEGER,
            created_at DATETIME NOT NULL,
            FOREIGN KEY (parent_category_id) REFERENCES Category(category_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE Payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            payment_method TEXT NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            payment_date DATETIME NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE ShippingAddresses (
            address_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            recipient_name TEXT NOT NULL,
            address_line1 TEXT NOT NULL,
            address_line2 TEXT,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            country TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE Feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            feedback_date DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES User(user_id),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE AdminLogs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            action_date DATETIME NOT NULL,
            ip_address TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database and tables created successfully.")
else:
    print("Database file already exists.")