from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
import os

class ReceiptPrinter:
    def __init__(self, database):
        self.db = database
        self.receipts_dir = "receipts"
        if not os.path.exists(self.receipts_dir):
            os.makedirs(self.receipts_dir)
    
    def generate_receipt(self, transaction_id):
        """Generate PDF receipt untuk transaksi"""
        # Get transaction data
        transaction = self.get_transaction_data(transaction_id)
        if not transaction:
            raise Exception("Transaksi tidak ditemukan")
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"receipt_{transaction_id}_{timestamp}.pdf"
        filepath = os.path.join(self.receipts_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4, 
                              topMargin=1*cm, bottomMargin=1*cm,
                              leftMargin=1*cm, rightMargin=1*cm)
        
        # Build content
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        # Header
        story.append(Paragraph("CAFE POS SYSTEM", title_style))
        story.append(Paragraph("Jl. Contoh No. 123, Kota", header_style))
        story.append(Paragraph("Telp: (021) 12345678", header_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Transaction info
        transaction_info = [
            ["No. Transaksi:", f"#{transaction_id}"],
            ["Tanggal:", transaction['transaction_date'].strftime("%d/%m/%Y %H:%M")],
            ["Kasir:", transaction['cashier_name'] or "Kasir"],
            ["Pelanggan:", transaction['customer_name'] or "-"],
            ["Metode Bayar:", transaction['payment_method']]
        ]
        
        info_table = Table(transaction_info, colWidths=[4*cm, 6*cm])
        info_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Items table
        items_data = [["Item", "Qty", "Harga", "Total"]]
        items_data.append(["-" * 20, "-" * 5, "-" * 10, "-" * 10])
        
        for item in transaction['items']:
            items_data.append([
                item['item_name'][:20],  # Limit nama item
                str(item['quantity']),
                f"Rp {item['unit_price']:,.0f}",
                f"Rp {item['total_price']:,.0f}"
            ])
        
        items_table = Table(items_data, colWidths=[8*cm, 2*cm, 3*cm, 3*cm])
        items_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEBELOW', (0, 1), (-1, 1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 2), (-1, -1), 4),
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 0.3*cm))
        
        # Totals
        totals_data = [
            ["", "", "Subtotal:", f"Rp {transaction['total_amount']:,.0f}"],
            ["", "", "Pajak (10%):", f"Rp {transaction['tax_amount']:,.0f}"],
            ["", "", "TOTAL:", f"Rp {transaction['final_amount']:,.0f}"]
        ]
        
        totals_table = Table(totals_data, colWidths=[8*cm, 2*cm, 3*cm, 3*cm])
        totals_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTSIZE', (0, 2), (-1, 2), 12),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('LINEABOVE', (2, 2), (-1, 2), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(totals_table)
        story.append(Spacer(1, 1*cm))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#7f8c8d')
        )
        
        story.append(Paragraph("Terima kasih atas kunjungan Anda!", footer_style))
        story.append(Paragraph("Selamat menikmati!", footer_style))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def get_transaction_data(self, transaction_id):
        """Get complete transaction data including items"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Get transaction
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        transaction = cursor.fetchone()
        
        if not transaction:
            conn.close()
            return None
        
        # Convert to dict
        transaction_dict = {
            'id': transaction[0],
            'transaction_date': datetime.fromisoformat(transaction[1]),
            'total_amount': transaction[2],
            'tax_amount': transaction[3],
            'discount_amount': transaction[4],
            'final_amount': transaction[5],
            'payment_method': transaction[6],
            'customer_name': transaction[7],
            'cashier_name': transaction[8]
        }
        
        # Get transaction items
        cursor.execute('''
            SELECT ti.*, m.name as item_name, m.description 
            FROM transaction_items ti 
            JOIN menu_items m ON ti.menu_item_id = m.id 
            WHERE ti.transaction_id = ?
        ''', (transaction_id,))
        
        items = cursor.fetchall()
        transaction_dict['items'] = []
        
        for item in items:
            transaction_dict['items'].append({
                'id': item[0],
                'menu_item_id': item[2],
                'quantity': item[3],
                'unit_price': item[4],
                'total_price': item[5],
                'notes': item[6],
                'item_name': item[7],
                'description': item[8]
            })
        
        conn.close()
        return transaction_dict
    
    def generate_daily_report(self, date):
        """Generate laporan harian dalam PDF"""
        # Get daily data
        daily_sales = self.db.get_daily_sales(date)
        transactions = self.db.get_transactions(date, date)
        popular_items = self.db.get_popular_items(date, date)
        
        # Create filename
        filename = f"daily_report_{date.replace('-', '')}.pdf"
        filepath = os.path.join(self.receipts_dir, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                              topMargin=2*cm, bottomMargin=2*cm,
                              leftMargin=2*cm, rightMargin=2*cm)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        )
        
        story.append(Paragraph("LAPORAN PENJUALAN HARIAN", title_style))
        story.append(Paragraph(f"Tanggal: {datetime.strptime(date, '%Y-%m-%d').strftime('%d %B %Y')}", 
                              ParagraphStyle('DateStyle', parent=styles['Normal'], 
                                           alignment=TA_CENTER, fontSize=14, spaceAfter=30)))
        
        # Summary
        if daily_sales:
            summary_data = [
                ["Total Transaksi", str(daily_sales[0] or 0)],
                ["Total Penjualan", f"Rp {daily_sales[1]:,.0f}" if daily_sales[1] else "Rp 0"],
                ["Rata-rata per Transaksi", f"Rp {daily_sales[2]:,.0f}" if daily_sales[2] else "Rp 0"]
            ]
            
            summary_table = Table(summary_data, colWidths=[8*cm, 6*cm])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ecf0f1')),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            story.append(Paragraph("RINGKASAN", styles['Heading2']))
            story.append(summary_table)
            story.append(Spacer(1, 1*cm))
        
        # Popular Items
        if popular_items:
            story.append(Paragraph("ITEM TERPOPULER", styles['Heading2']))
            
            popular_data = [["Item", "Terjual", "Pendapatan"]]
            for item in popular_items[:10]:  # Top 10
                popular_data.append([
                    item[0],  # name
                    str(item[2]),  # total_quantity
                    f"Rp {item[3]:,.0f}"  # total_revenue
                ])
            
            popular_table = Table(popular_data, colWidths=[8*cm, 3*cm, 3*cm])
            popular_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            story.append(popular_table)
            story.append(Spacer(1, 1*cm))
        
        # Build PDF
        doc.build(story)
        return filepath