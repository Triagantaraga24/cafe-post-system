from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTableWidget, QTableWidgetItem, QDateEdit,
                             QTabWidget, QGroupBox, QFormLayout, QHeaderView,
                             QMessageBox, QFrame, QComboBox)
from PySide6.QtCore import Qt, QDate, QThread, QObject, Signal
from PySide6.QtGui import QFont
from datetime import datetime, date, timedelta
import subprocess
import sys
import os

class ReportGenerator(QObject):
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, receipt_printer, report_date):
        super().__init__()
        self.receipt_printer = receipt_printer
        self.report_date = report_date
    
    def generate(self):
        try:
            filepath = self.receipt_printer.generate_daily_report(self.report_date)
            self.finished.emit(filepath)
        except Exception as e:
            self.error.emit(str(e))

class ReportsWindow(QWidget):
    def __init__(self, database):
        super().__init__()
        self.db = database
        
        self.setWindowTitle("Laporan Penjualan")
        self.setGeometry(200, 200, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # Improved stylesheet: higher contrast, readable text
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                color: #2c3e50; /* default text color */
                font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial;
                font-size: 12px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 14px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton#exportBtn {
                background-color: #27ae60;
            }
            QPushButton#exportBtn:hover {
                background-color: #229954;
            }
            QLabel#titleLabel {
                font-size: 20px;
                font-weight: 700;
                color: #2c3e50;
                padding: 8px;
            }
            QLabel#summaryLabel {
                font-size: 14px;
                font-weight: 700;
                color: #2c3e50;
                padding: 4px;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f2f2f2;
                border: 1px solid #cfd8dc;
                border-radius: 6px;
                gridline-color: #ecf0f1;
                color: #2c3e50;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #cfd8dc;
                background-color: transparent;
                border-radius: 6px;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 8px 14px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                color: #2c3e50;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #3498db;
                color: #2c3e50;
            }
            QGroupBox {
                font-weight: 700;
                border: 1px solid #cfd8dc;
                border-radius: 6px;
                margin-top: 10px;
                background-color: white;
                padding: 8px;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QDateEdit, QComboBox {
                padding: 6px;
                border: 1px solid #dfe6e9;
                border-radius: 6px;
                background-color: white;
                color: #2c3e50;
            }
            QDateEdit:focus, QComboBox:focus {
                border-color: #3498db;
            }
        """)
        
        self.init_ui()
        self.load_today_data()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Laporan Penjualan")
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Daily report tab
        daily_tab = self.create_daily_tab()
        self.tab_widget.addTab(daily_tab, "Laporan Harian")
        
        # Transaction history tab
        history_tab = self.create_history_tab()
        self.tab_widget.addTab(history_tab, "Riwayat Transaksi")
        
        # Popular items tab
        popular_tab = self.create_popular_tab()
        self.tab_widget.addTab(popular_tab, "Item Terpopuler")
        
        layout.addWidget(self.tab_widget)
        
    def create_daily_tab(self):
        daily_widget = QWidget()
        layout = QVBoxLayout(daily_widget)
        
        # Date selection
        date_group = QGroupBox("Pilih Tanggal")
        date_layout = QFormLayout(date_group)
        
        self.daily_date_edit = QDateEdit()
        self.daily_date_edit.setDate(QDate.currentDate())
        self.daily_date_edit.setCalendarPopup(True)
        date_layout.addRow("Tanggal:", self.daily_date_edit)
        
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.clicked.connect(self.load_daily_data)
        date_layout.addRow("", refresh_btn)
        
        layout.addWidget(date_group)
        
        # Summary section
        self.summary_group = QGroupBox("Ringkasan Penjualan")
        self.summary_layout = QFormLayout(self.summary_group)
        
        self.total_transactions_label = QLabel("0")
        self.total_transactions_label.setObjectName("summaryLabel")
        self.summary_layout.addRow("Total Transaksi:", self.total_transactions_label)
        
        self.total_sales_label = QLabel("Rp 0")
        self.total_sales_label.setObjectName("summaryLabel")
        self.summary_layout.addRow("Total Penjualan:", self.total_sales_label)
        
        self.avg_transaction_label = QLabel("Rp 0")
        self.avg_transaction_label.setObjectName("summaryLabel")
        self.summary_layout.addRow("Rata-rata per Transaksi:", self.avg_transaction_label)
        
        layout.addWidget(self.summary_group)
        
        # Export button
        export_layout = QHBoxLayout()
        export_daily_btn = QPushButton("Export Laporan Harian (PDF)")
        export_daily_btn.setObjectName("exportBtn")
        export_daily_btn.clicked.connect(self.export_daily_report)
        export_layout.addWidget(export_daily_btn)
        export_layout.addStretch()
        
        layout.addLayout(export_layout)
        layout.addStretch()
        
        return daily_widget
    
    def create_history_tab(self):
        history_widget = QWidget()
        layout = QVBoxLayout(history_widget)
        
        # Date range selection
        date_group = QGroupBox("Filter Tanggal")
        date_layout = QHBoxLayout(date_group)
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addDays(-7))
        self.start_date_edit.setCalendarPopup(True)
        date_layout.addWidget(QLabel("Dari:"))
        date_layout.addWidget(self.start_date_edit)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        date_layout.addWidget(QLabel("Sampai:"))
        date_layout.addWidget(self.end_date_edit)
        
        load_history_btn = QPushButton("Tampilkan")
        load_history_btn.clicked.connect(self.load_transaction_history)
        date_layout.addWidget(load_history_btn)
        
        date_layout.addStretch()
        
        layout.addWidget(date_group)
        
        # Transaction table
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(7)
        self.transaction_table.setHorizontalHeaderLabels([
            "ID", "Tanggal", "Pelanggan", "Total", "Pajak", "Final", "Metode Bayar"
        ])
        
        # Set column widths
        header = self.transaction_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        
        self.transaction_table.setColumnWidth(0, 60)
        self.transaction_table.setColumnWidth(3, 110)
        self.transaction_table.setColumnWidth(4, 90)
        self.transaction_table.setColumnWidth(5, 110)
        self.transaction_table.setColumnWidth(6, 110)
        
        self.transaction_table.setAlternatingRowColors(True)
        self.transaction_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.transaction_table)
        
        return history_widget
    
    def create_popular_tab(self):
        popular_widget = QWidget()
        layout = QVBoxLayout(popular_widget)
        
        # Date range and filters
        filter_group = QGroupBox("Filter")
        filter_layout = QHBoxLayout(filter_group)
        
        self.popular_start_date = QDateEdit()
        self.popular_start_date.setDate(QDate.currentDate().addDays(-30))
        self.popular_start_date.setCalendarPopup(True)
        filter_layout.addWidget(QLabel("Dari:"))
        filter_layout.addWidget(self.popular_start_date)
        
        self.popular_end_date = QDateEdit()
        self.popular_end_date.setDate(QDate.currentDate())
        self.popular_end_date.setCalendarPopup(True)
        filter_layout.addWidget(QLabel("Sampai:"))
        filter_layout.addWidget(self.popular_end_date)
        
        self.popular_limit_combo = QComboBox()
        self.popular_limit_combo.addItems(["10", "20", "50", "Semua"])
        filter_layout.addWidget(QLabel("Tampilkan:"))
        filter_layout.addWidget(self.popular_limit_combo)
        
        load_popular_btn = QPushButton("Tampilkan")
        load_popular_btn.clicked.connect(self.load_popular_items)
        filter_layout.addWidget(load_popular_btn)
        
        filter_layout.addStretch()
        
        layout.addWidget(filter_group)
        
        # Popular items table
        self.popular_table = QTableWidget()
        self.popular_table.setColumnCount(4)
        self.popular_table.setHorizontalHeaderLabels([
            "Item", "Harga Satuan", "Terjual", "Total Pendapatan"
        ])
        
        # Set column widths
        popular_header = self.popular_table.horizontalHeader()
        popular_header.setSectionResizeMode(0, QHeaderView.Stretch)
        popular_header.setSectionResizeMode(1, QHeaderView.Fixed)
        popular_header.setSectionResizeMode(2, QHeaderView.Fixed)
        popular_header.setSectionResizeMode(3, QHeaderView.Fixed)
        
        self.popular_table.setColumnWidth(1, 120)
        self.popular_table.setColumnWidth(2, 90)
        self.popular_table.setColumnWidth(3, 150)
        
        self.popular_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.popular_table)
        
        return popular_widget
    
    def load_today_data(self):
        """Load data for today by default"""
        today = date.today().strftime('%Y-%m-%d')
        self.load_daily_data()
        self.load_transaction_history()
        self.load_popular_items()
    
    def load_daily_data(self):
        """Load daily sales summary"""
        selected_date = self.daily_date_edit.date().toString("yyyy-MM-dd")
        
        # Get daily sales data
        daily_sales = self.db.get_daily_sales(selected_date)
        
        if daily_sales:
            self.total_transactions_label.setText(str(daily_sales[0] or 0))
            self.total_sales_label.setText(f"Rp {daily_sales[1]:,.0f}" if daily_sales[1] else "Rp 0")
            self.avg_transaction_label.setText(f"Rp {daily_sales[2]:,.0f}" if daily_sales[2] else "Rp 0")
        else:
            self.total_transactions_label.setText("0")
            self.total_sales_label.setText("Rp 0")
            self.avg_transaction_label.setText("Rp 0")
    
    def load_transaction_history(self):
        """Load transaction history for date range"""
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
        
        transactions = self.db.get_transactions(start_date, end_date)
        
        self.transaction_table.setRowCount(len(transactions))
        
        for row, transaction in enumerate(transactions):
            # ID
            self.transaction_table.setItem(row, 0, QTableWidgetItem(str(transaction[0])))
            
            # Date (safely parse, fallback if needed)
            try:
                date_str = datetime.fromisoformat(transaction[1]).strftime("%d/%m/%Y %H:%M")
            except Exception:
                date_str = str(transaction[1])
            self.transaction_table.setItem(row, 1, QTableWidgetItem(date_str))
            
            # Customer
            customer = transaction[7] if len(transaction) > 7 and transaction[7] else "-"
            self.transaction_table.setItem(row, 2, QTableWidgetItem(customer))
            
            # Total Amount
            total_item = QTableWidgetItem(f"Rp {transaction[2]:,.0f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.transaction_table.setItem(row, 3, total_item)
            
            # Tax Amount
            tax_item = QTableWidgetItem(f"Rp {transaction[3]:,.0f}")
            tax_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.transaction_table.setItem(row, 4, tax_item)
            
            # Final Amount
            final_item = QTableWidgetItem(f"Rp {transaction[5]:,.0f}")
            final_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.transaction_table.setItem(row, 5, final_item)
            
            # Payment Method
            method = transaction[6] if len(transaction) > 6 else "-"
            self.transaction_table.setItem(row, 6, QTableWidgetItem(method))
    
    def load_popular_items(self):
        """Load popular items for date range"""
        start_date = self.popular_start_date.date().toString("yyyy-MM-dd")
        end_date = self.popular_end_date.date().toString("yyyy-MM-dd")
        
        limit_text = self.popular_limit_combo.currentText()
        limit = None if limit_text == "Semua" else int(limit_text)
        
        popular_items = self.db.get_popular_items(start_date, end_date, limit or 1000)
        
        self.popular_table.setRowCount(len(popular_items))
        
        for row, item in enumerate(popular_items):
            # Item name
            self.popular_table.setItem(row, 0, QTableWidgetItem(item[0]))
            
            # Unit price
            price_item = QTableWidgetItem(f"Rp {item[1]:,.0f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.popular_table.setItem(row, 1, price_item)
            
            # Quantity sold
            qty_item = QTableWidgetItem(str(item[2]))
            qty_item.setTextAlignment(Qt.AlignCenter)
            self.popular_table.setItem(row, 2, qty_item)
            
            # Total revenue
            revenue_item = QTableWidgetItem(f"Rp {item[3]:,.0f}")
            revenue_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.popular_table.setItem(row, 3, revenue_item)
    
    def export_daily_report(self):
        """Export daily report to PDF"""
        selected_date = self.daily_date_edit.date().toString("yyyy-MM-dd")
        
        try:
            # Import here to avoid top-level circular imports if any
            from receipt_printer import ReceiptPrinter
            receipt_printer = ReceiptPrinter(self.db)
            
            # Generate report in background thread
            self.generate_report_thread = QThread()
            self.report_generator = ReportGenerator(receipt_printer, selected_date)
            self.report_generator.moveToThread(self.generate_report_thread)
            
            # Connect signals
            self.generate_report_thread.started.connect(self.report_generator.generate)
            self.report_generator.finished.connect(self.on_report_generated)
            self.report_generator.error.connect(self.on_report_error)
            self.report_generator.finished.connect(self.generate_report_thread.quit)
            self.report_generator.error.connect(self.generate_report_thread.quit)
            
            # Start generation
            self.generate_report_thread.start()
            
            # Inform user (non-blocking)
            QMessageBox.information(self, "Info", "Sedang membuat laporan. Setelah selesai, Anda akan diberitahu.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal membuat laporan: {str(e)}")
    
    def on_report_generated(self, filepath):
        """Called when report generation is completed"""
        reply = QMessageBox.question(
            self, 
            "Laporan Berhasil", 
            f"Laporan berhasil dibuat!\n\nLokasi: {filepath}\n\nBuka file sekarang?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.open_file(filepath)
    
    def on_report_error(self, error_message):
        """Called when report generation fails"""
        QMessageBox.critical(self, "Error", f"Gagal membuat laporan: {error_message}")
    
    def open_file(self, filepath):
        """Open file with system default application"""
        try:
            if sys.platform.startswith('win'):
                os.startfile(filepath)
            elif sys.platform.startswith('darwin'):  # macOS
                subprocess.run(['open', filepath])
            else:  # Linux and others
                subprocess.run(['xdg-open', filepath])
        except Exception as e:
            QMessageBox.warning(self, "Peringatan", 
                              f"File berhasil dibuat tetapi tidak bisa dibuka otomatis: {str(e)}\n\n"
                              f"Silakan buka manual: {filepath}")