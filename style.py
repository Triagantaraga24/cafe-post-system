MAIN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}
QWidget#leftPanel, QWidget#rightPanel {
    background-color: white;
    border: 1px solid #bdc3c7;
    border-radius: 5px;
    padding: 8px;
}
QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 5px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #2980b9;
}
QPushButton:pressed {
    background-color: #21618c;
}

/* Tombol Kategori */
QPushButton#categoryBtn {
    background-color: #7f8c8d;
    min-height: 40px;
    font-size: 14px;
    color: white;
}
QPushButton#categoryBtn:checked {
    background-color: #3498db;
    color: white;
}

/* Tombol Menu */
QPushButton#menuBtn {
    background-color: white;
    color: #2c3e50;
    border: 2px solid #bdc3c7;
    min-height: 80px;
    text-align: left;
    font-size: 12px;
}
QPushButton#menuBtn:hover {
    border-color: #3498db;
    background-color: #ebf3fd;
}

/* Tombol Tambah ke Keranjang */
QPushButton#addToCartBtn {
    background-color: #27ae60;
    min-height: 30px;
    color: white;
}
QPushButton#addToCartBtn:hover {
    background-color: #229954;
}

/* Tombol Hapus Item */
QPushButton#removeBtn {
    background-color: #e74c3c;
    color: white;
    font-weight: bold;
    max-width: 30px;
    max-height: 30px;
    border-radius: 50px;
    font-size: 12px;
}
QPushButton#removeBtn:hover {
    background-color: #c0392b;
}

/* Label */
QLabel#titleLabel {
    font-size: 18px;
    font-weight: bold;
    color: #2c3e50;
    padding: 8px;
}
QLabel#totalLabel {
    font-size: 24px;
    font-weight: bold;
    color: #27ae60;
}

/* Separator */
QFrame#separator {
    background-color: #bdc3c7;
}

/* Tabel */
QTableWidget {
    background-color: white;
    border: 1px solid #bdc3c7;
    border-radius: 5px;
    gridline-color: #ecf0f1;
    color: #2c3e50;
}
QTableWidget::item {
    padding: 8px;
}
QTableWidget::item:selected {
    background-color: #3498db;
    color: white;
}

/* Input Fields */
QLineEdit, QSpinBox, QComboBox, QTextEdit, QDateEdit {
    padding: 8px;
    border: 2px solid #bdc3c7;
    border-radius: 5px;
    background-color: white;
    color: #2c3e50;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QTextEdit:focus, QDateEdit:focus {
    border-color: #3498db;
}

/* SpinBox */
QSpinBox {
    background-color: white;
    border: 1px solid #c59d5f;
    border-radius: 4px;
    padding: 2px;
}
QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 16px;
    background-color: #c59d5f;
    border-left: 1px solid #b48a4a;
}
QSpinBox::up-button:hover {
    background-color: #a07848;
}
QSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 16px;
    background-color: #c59d5f;
    border-left: 1px solid #b48a4a;
}
QSpinBox::down-button:hover {
    background-color: #a07848;
}

/* GroupBox */
QGroupBox {
    font-weight: bold;
    color: #2c3e50;
    border: 1px solid #bdc3c7;
    border-radius: 5px;
    margin-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #bdc3c7;
    background-color: white;
    border-radius: 5px;
}
QTabBar::tab {
    background-color: #ecf0f1;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    color: #2c3e50;
}
QTabBar::tab:selected {
    background-color: white;
    border-bottom: 2px solid #3498db;
    color: #2c3e50;
}

/* Item Menu */
QWidget#menuItem {
    background-color: #fffaf5;
    border: 1px solid #e0d6c9;
    border-radius: 10px;
}
QWidget#menuItem:hover {
    border-color: #c59d5f;
    background-color: #fff5ec;
}
QLabel#menuItemName {
    font-weight: bold;
    font-size: 14px;
    color: #4b3832;
}
QLabel#menuItemDesc {
    font-size: 10px;
    color: #7b6f67;
}
QLabel#menuItemPrice {
    font-size: 12px;
    font-weight: bold;
    color: #6b8e23;
}
QPushButton#menuAddBtn {
    background-color: #c59d5f;
    color: white;
    font-size: 12px;
    font-weight: bold;
    padding: 6px;
    border-radius: 6px;
}
QPushButton#menuAddBtn:hover {
    background-color: #a07848;
}
QPushButton#menuAddBtn:pressed {
    background-color: #8c6231;
}
"""
