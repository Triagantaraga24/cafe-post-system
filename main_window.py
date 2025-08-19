from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                             QComboBox, QSpinBox, QTextEdit, QLineEdit, QFrame,
                             QMessageBox, QTabWidget, QScrollArea, QGridLayout,
                             QGroupBox, QFormLayout, QDateEdit, QHeaderView)
from PySide6.QtCore import Qt, QDate
from datetime import datetime
from database import Database
from receipt_printer import ReceiptPrinter
from style import MAIN_STYLE

class CartItem:
    def __init__(self, menu_item, quantity=1, notes=""):
        self.id = menu_item[0]
        self.name = menu_item[1]
        self.price = menu_item[2]
        self.category = menu_item[6] if len(menu_item) > 6 else ""
        self.quantity = quantity
        self.notes = notes
        self.total = self.price * quantity


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.receipt_printer = ReceiptPrinter(self.db)
        self.cart_items = []
        self.current_category = None

        self.setWindowTitle("Maron Cafe POS System")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)

        # Semua style sheet di sini
        self.setStyleSheet(MAIN_STYLE)

        self.init_ui()
        self.load_categories()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(self.create_menu_panel(), 2)
        main_layout.addWidget(self.create_cart_panel(), 1)

    def create_menu_panel(self):
        menu_widget = QWidget()
        menu_widget.setObjectName("leftPanel")
        
        menu_layout = QVBoxLayout(menu_widget)
        title_label = QLabel("Menu")
        title_label.setObjectName("titleLabel")
        menu_layout.addWidget(title_label)

        self.category_layout = QHBoxLayout()
        menu_layout.addLayout(self.category_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.menu_widget = QWidget()
        self.menu_layout = QGridLayout(self.menu_widget)
        self.menu_layout.setSpacing(10)
        scroll_area.setWidget(self.menu_widget)
        menu_layout.addWidget(scroll_area)
        return menu_widget

    def create_cart_panel(self):
        cart_widget = QWidget()
        cart_widget.setObjectName("rightPanel")
        cart_layout = QVBoxLayout(cart_widget)
        cart_title = QLabel("Keranjang")
        cart_title.setObjectName("titleLabel")
        cart_layout.addWidget(cart_title)

        customer_group = QGroupBox("Informasi Pelanggan")
        customer_layout = QFormLayout(customer_group)
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("Nama pelanggan (opsional)")
        customer_layout.addRow("Nama:", self.customer_name_input)
        cart_layout.addWidget(customer_group)

        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["Item", "Harga", "Qty", "Total", "Delete"])
        self.cart_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.cart_table.setColumnWidth(0, 10)
        self.cart_table.setColumnWidth(1, 80)
        self.cart_table.setColumnWidth(2, 70)
        self.cart_table.setColumnWidth(3, 100)
        self.cart_table.setColumnWidth(4, 50)
        cart_layout.addWidget(self.cart_table)

        total_group = QGroupBox("Total")
        total_layout = QFormLayout(total_group)
        self.subtotal_label = QLabel("Rp 0")
        self.tax_label = QLabel("Rp 0")
        self.total_label = QLabel("Rp 0")
        self.total_label.setObjectName("totalLabel")
        total_layout.addRow("Subtotal:", self.subtotal_label)
        total_layout.addRow("Pajak (12%):", self.tax_label)
        total_layout.addRow("Total:", self.total_label)
        cart_layout.addWidget(total_group)

        payment_group = QGroupBox("Metode Pembayaran")
        payment_layout = QFormLayout(payment_group)
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Cash", "Credit Card", "Debit Card", "E-Wallet"])
        payment_layout.addRow("Metode:", self.payment_combo)
        cart_layout.addWidget(payment_group)

        self.checkout_btn = QPushButton("Checkout")
        cart_layout.addWidget(self.checkout_btn)

        self.clear_cart_btn = QPushButton("Kosongkan Keranjang")
        cart_layout.addWidget(self.clear_cart_btn)

        self.reports_btn = QPushButton("Laporan")
        cart_layout.addWidget(self.reports_btn)

        self.checkout_btn.clicked.connect(self.checkout)
        self.clear_cart_btn.clicked.connect(self.clear_cart)
        self.reports_btn.clicked.connect(self.show_reports)

        return cart_widget

    def load_categories(self):
        for i in reversed(range(self.category_layout.count())):
            self.category_layout.itemAt(i).widget().setParent(None)

        all_btn = QPushButton("Semua")
        all_btn.setObjectName("categoryBtn")
        all_btn.setCheckable(True)
        all_btn.setChecked(True)
        all_btn.clicked.connect(lambda: self.load_menu_items(None))
        self.category_layout.addWidget(all_btn)

        categories = self.db.get_categories()
        for category in categories:
            btn = QPushButton(category[1])
            btn.setObjectName("categoryBtn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, cat_id=category[0]: self.load_menu_items(cat_id))
            self.category_layout.addWidget(btn)

        self.load_menu_items(None)

    def load_menu_items(self, category_id):
        self.current_category = category_id

        for i in range(self.category_layout.count()):
            btn = self.category_layout.itemAt(i).widget()
            if isinstance(btn, QPushButton):
                if category_id is None and i == 0:
                    btn.setChecked(True)
                elif category_id is not None and i > 0:
                    categories = self.db.get_categories()
                    if i-1 < len(categories) and categories[i-1][0] == category_id:
                        btn.setChecked(True)
                    else:
                        btn.setChecked(False)
                else:
                    btn.setChecked(False)

        for i in reversed(range(self.menu_layout.count())):
            self.menu_layout.itemAt(i).widget().setParent(None)

        menu_items = self.db.get_menu_items(category_id)

        row, col = 0, 0
        max_cols = 3

        for item in menu_items:
            item_widget = self.create_menu_item_widget(item)
            self.menu_layout.addWidget(item_widget, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def create_menu_item_widget(self, item):
        item_widget = QWidget()
        item_widget.setObjectName("menuItem")
        item_widget.setFixedSize(200, 150)

        layout = QVBoxLayout(item_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        name_label = QLabel(item[1])
        name_label.setObjectName("menuItemName")
        name_label.setWordWrap(True)
        layout.addWidget(name_label)

        if item[4]:
            desc_label = QLabel(item[4])
            desc_label.setObjectName("menuItemDesc")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        price_label = QLabel(f"Rp {item[2]:,.0f}")
        price_label.setObjectName("menuItemPrice")
        layout.addWidget(price_label)

        add_btn = QPushButton("Tambah ke Keranjang")
        add_btn.setObjectName("menuAddBtn")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(lambda: self.add_to_cart(item))
        layout.addWidget(add_btn)

        return item_widget

    def add_to_cart(self, menu_item):
        for i, cart_item in enumerate(self.cart_items):
            if cart_item.id == menu_item[0]:
                self.cart_items[i].quantity += 1
                self.cart_items[i].total = self.cart_items[i].price * self.cart_items[i].quantity
                break
        else:
            cart_item = CartItem(menu_item)
            self.cart_items.append(cart_item)

        self.update_cart_display()

    def update_cart_display(self):
        self.cart_table.setRowCount(len(self.cart_items))
        self.cart_table.verticalHeader().setDefaultSectionSize(36)

        for i, cart_item in enumerate(self.cart_items):
            self.cart_table.setItem(i, 0, QTableWidgetItem(cart_item.name))

            price_item = QTableWidgetItem(f"Rp {cart_item.price:,.0f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(i, 1, price_item)

            qty_spin = QSpinBox()
            qty_spin.setMinimum(1)
            qty_spin.setValue(cart_item.quantity)
            qty_spin.setFixedWidth(50)
            qty_spin.valueChanged.connect(lambda value, idx=i: self.update_cart_quantity(idx, value))
            self.cart_table.setCellWidget(i, 2, qty_spin)

            total_item = QTableWidgetItem(f"Rp {cart_item.total:,.0f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(i, 3, total_item)

            remove_btn = QPushButton("×")
            remove_btn.setObjectName("removeBtn")
            remove_btn.setCursor(Qt.PointingHandCursor)
            remove_btn.clicked.connect(lambda checked, idx=i: self.remove_from_cart(idx))
            self.cart_table.setCellWidget(i, 4, remove_btn)

        self.update_totals()

    def update_cart_quantity(self, index, quantity):
        if index < len(self.cart_items):
            self.cart_items[index].quantity = quantity
            self.cart_items[index].total = self.cart_items[index].price * quantity
            self.update_cart_display()

    def remove_from_cart(self, index):
        if index < len(self.cart_items):
            del self.cart_items[index]
            self.update_cart_display()

    def update_totals(self):
        subtotal = sum(item.total for item in self.cart_items)
        tax = subtotal * 0.12
        total = subtotal + tax

        self.subtotal_label.setText(f"Rp {subtotal:,.0f}")
        self.tax_label.setText(f"Rp {tax:,.0f}")
        self.total_label.setText(f"Rp {total:,.0f}")

    def clear_cart(self):
        reply = QMessageBox.question(self, 'Konfirmasi', 
                                   'Apakah Anda yakin ingin mengosongkan keranjang?',
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.cart_items.clear()
            self.update_cart_display()

    def checkout(self):
        if not self.cart_items:
            QMessageBox.warning(self, "Peringatan", "Keranjang kosong!")
            return

        subtotal = sum(item.total for item in self.cart_items)
        tax = subtotal * 0.10
        total = subtotal + tax

        customer_name = self.customer_name_input.text()
        payment_method = self.payment_combo.currentText()

        transaction_id = self.db.create_transaction(
            total_amount=subtotal,
            tax_amount=tax,
            discount_amount=0,
            final_amount=total,
            payment_method=payment_method,
            customer_name=customer_name,
            cashier_name="Kasir"
        )

        for cart_item in self.cart_items:
            self.db.add_transaction_item(
                transaction_id=transaction_id,
                menu_item_id=cart_item.id,
                quantity=cart_item.quantity,
                unit_price=cart_item.price,
                total_price=cart_item.total
            )

        try:
            receipt_path = self.receipt_printer.generate_receipt(transaction_id)
            QMessageBox.information(self, "Sukses", 
                                  f"Transaksi berhasil!\nStruk tersimpan di: {receipt_path}")
        except Exception as e:
            QMessageBox.warning(self, "Peringatan", 
                              f"Transaksi berhasil, tetapi gagal mencetak struk: {str(e)}")

        self.cart_items.clear()
        self.customer_name_input.clear()
        self.update_cart_display()

    def show_reports(self):
        from reports_window import ReportsWindow
        self.reports_window = ReportsWindow(self.db)
        self.reports_window.show()
