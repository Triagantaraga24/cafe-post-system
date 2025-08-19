import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_path = "cafe_pos.db"
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inisialisasi database dan tabel"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabel kategori
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel menu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category_id INTEGER,
                description TEXT,
                is_available BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Tabel transaksi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_amount REAL NOT NULL,
                tax_amount REAL DEFAULT 0,
                discount_amount REAL DEFAULT 0,
                final_amount REAL NOT NULL,
                payment_method TEXT DEFAULT 'Cash',
                customer_name TEXT,
                cashier_name TEXT
            )
        ''')
        
        # Tabel detail transaksi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaction_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER,
                menu_item_id INTEGER,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                notes TEXT,
                FOREIGN KEY (transaction_id) REFERENCES transactions (id),
                FOREIGN KEY (menu_item_id) REFERENCES menu_items (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insert data awal jika belum ada
        self.insert_initial_data()
    
    def insert_initial_data(self):
        """Insert data kategori dan menu awal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Cek apakah sudah ada data
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            # Insert kategori
            categories = [
                ('Kopi',),
                ('Makanan Ringan',),
                ('Non-Kopi',)
            ]
            cursor.executemany("INSERT INTO categories (name) VALUES (?)", categories)
            
            # Insert menu items
            menu_items = [
                # Kopi (category_id = 1)
                ('Espresso', 15000, 1, 'Kopi hitam pekat'),
                ('Americano', 18000, 1, 'Espresso dengan air panas'),
                ('Cappuccino', 22000, 1, 'Espresso dengan susu dan foam'),
                ('Latte', 25000, 1, 'Espresso dengan susu steamed'),
                ('Mocha', 28000, 1, 'Latte dengan cokelat'),
                
                # Makanan Ringan (category_id = 2)
                ('Croissant', 15000, 2, 'Pastry mentega berlapis'),
                ('Sandwich Club', 35000, 2, 'Sandwich dengan ayam dan sayuran'),
                ('Muffin Blueberry', 18000, 2, 'Muffin dengan blueberry segar'),
                ('Cookies Choco Chip', 12000, 2, 'Kue kering cokelat chip'),
                ('Cake Slice Red Velvet', 25000, 2, 'Potongan kue red velvet'),
                
                # Non-Kopi (category_id = 3)
                ('Teh Tarik', 12000, 3, 'Teh dengan susu'),
                ('Chocolate Ice', 20000, 3, 'Minuman cokelat dingin'),
                ('Lemon Tea', 15000, 3, 'Teh dengan lemon segar'),
                ('Milkshake Vanilla', 25000, 3, 'Milkshake rasa vanilla'),
                ('Fresh Orange Juice', 18000, 3, 'Jus jeruk segar')
            ]
            cursor.executemany(
                "INSERT INTO menu_items (name, price, category_id, description) VALUES (?, ?, ?, ?)", 
                menu_items
            )
            
            conn.commit()
        
        conn.close()
    
    # CRUD Operations untuk Categories
    def get_categories(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY name")
        categories = cursor.fetchall()
        conn.close()
        return categories
    
    # CRUD Operations untuk Menu Items
    def get_menu_items(self, category_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        if category_id:
            cursor.execute('''
                SELECT m.*, c.name as category_name 
                FROM menu_items m 
                JOIN categories c ON m.category_id = c.id 
                WHERE m.category_id = ? AND m.is_available = 1
                ORDER BY m.name
            ''', (category_id,))
        else:
            cursor.execute('''
                SELECT m.*, c.name as category_name 
                FROM menu_items m 
                JOIN categories c ON m.category_id = c.id 
                WHERE m.is_available = 1
                ORDER BY c.name, m.name
            ''')
        items = cursor.fetchall()
        conn.close()
        return items
    
    def get_menu_item_by_id(self, item_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, c.name as category_name 
            FROM menu_items m 
            JOIN categories c ON m.category_id = c.id 
            WHERE m.id = ?
        ''', (item_id,))
        item = cursor.fetchone()
        conn.close()
        return item
    
    # CRUD Operations untuk Transactions
    def create_transaction(self, total_amount, tax_amount, discount_amount, final_amount, 
                          payment_method='Cash', customer_name='', cashier_name=''):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (total_amount, tax_amount, discount_amount, final_amount, 
                                    payment_method, customer_name, cashier_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (total_amount, tax_amount, discount_amount, final_amount, payment_method, customer_name, cashier_name))
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return transaction_id
    
    def add_transaction_item(self, transaction_id, menu_item_id, quantity, unit_price, total_price, notes=''):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transaction_items (transaction_id, menu_item_id, quantity, unit_price, total_price, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (transaction_id, menu_item_id, quantity, unit_price, total_price, notes))
        conn.commit()
        conn.close()
    
    def get_transactions(self, start_date=None, end_date=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM transactions"
        params = []
        
        if start_date and end_date:
            query += " WHERE DATE(transaction_date) BETWEEN ? AND ?"
            params = [start_date, end_date]
        
        query += " ORDER BY transaction_date DESC"
        
        cursor.execute(query, params)
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    
    def get_transaction_items(self, transaction_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ti.*, m.name as item_name, m.description 
            FROM transaction_items ti 
            JOIN menu_items m ON ti.menu_item_id = m.id 
            WHERE ti.transaction_id = ?
        ''', (transaction_id,))
        items = cursor.fetchall()
        conn.close()
        return items
    
    def get_daily_sales(self, date):
        """Mendapatkan total penjualan harian"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                COUNT(*) as transaction_count,
                SUM(final_amount) as total_sales,
                AVG(final_amount) as avg_transaction
            FROM transactions 
            WHERE DATE(transaction_date) = ?
        ''', (date,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_popular_items(self, start_date=None, end_date=None, limit=10):
        """Mendapatkan item terpopuler"""
        conn = self.get_connection()
        cursor = conn.cursor()
        query = '''
            SELECT 
                m.name,
                m.price,
                SUM(ti.quantity) as total_quantity,
                SUM(ti.total_price) as total_revenue
            FROM transaction_items ti
            JOIN menu_items m ON ti.menu_item_id = m.id
            JOIN transactions t ON ti.transaction_id = t.id
        '''
        params = []
        
        if start_date and end_date:
            query += " WHERE DATE(t.transaction_date) BETWEEN ? AND ?"
            params = [start_date, end_date]
        
        query += '''
            GROUP BY m.id, m.name, m.price
            ORDER BY total_quantity DESC
            LIMIT ?
        '''
        params.append(limit)
        
        cursor.execute(query, params)
        items = cursor.fetchall()
        conn.close()
        return items