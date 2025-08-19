# Cafe POS System

Aplikasi Point of Sale (POS) berbasis desktop untuk Maron Cafe.

## Fitur Utama

### 🏪 Manajemen Menu
- **Kategori Menu**: Kopi, Makanan Ringan, Non-Kopi
- **Tampilan Grid**: Menu ditampilkan dalam bentuk card yang menarik
- **Filter Kategori**: Mudah beralih antar kategori menu
- **Data Menu Lengkap**: Nama, harga, deskripsi, dan status ketersediaan

### 🛒 Sistem Kasir
- **Keranjang Belanja**: Tambah, edit kuantitas, dan hapus item
- **Informasi Pelanggan**: Input nama pelanggan (opsional)
- **Perhitungan Otomatis**: Subtotal, pajak (10%), dan total
- **Metode Pembayaran**: Cash, Credit Card, Debit Card, E-Wallet

### 🧾 Struk & Receipt
- **Generate PDF**: Struk otomatis dalam format PDF menggunakan ReportLab
- **Design Professional**: Header cafe, detail transaksi, dan total
- **Auto Save**: Struk tersimpan di folder `receipts`
- **Print Ready**: Format siap cetak dengan layout yang rapi

### 📊 Sistem Laporan
- **Laporan Harian**: Ringkasan penjualan per hari
- **Riwayat Transaksi**: Daftar semua transaksi dengan filter tanggal
- **Item Terpopuler**: Analisis produk yang paling laris
- **Export PDF**: Laporan dapat diekspor ke PDF
- **Dashboard Analytics**: Statistik penjualan yang informatif

### 🎨 User Interface
- **Modern Design**: Antarmuka yang bersih dan profesional
- **Responsive Layout**: Menyesuaikan berbagai ukuran layar
- **Color Scheme**: Palet warna yang eye-friendly
- **Hover Effects**: Interaksi yang smooth dan responsif
- **Typography**: Font yang mudah dibaca

## Teknologi yang Digunakan

- **Bahasa**: Python 3.8+
- **GUI Framework**: PySide6 (Qt for Python)
- **Database**: SQLite3
- **PDF Generation**: ReportLab
- **Packaging**: PyInstaller

## Struktur Database

### Tabel Categories
- `id`: Primary key
- `name`: Nama kategori (Kopi, Makanan Ringan, Non-Kopi)
- `created_at`: Timestamp

### Tabel Menu Items
- `id`: Primary key
- `name`: Nama menu
- `price`: Harga
- `category_id`: Foreign key ke categories
- `description`: Deskripsi menu
- `is_available`: Status ketersediaan
- `created_at`: Timestamp

### Tabel Transactions
- `id`: Primary key
- `transaction_date`: Tanggal transaksi
- `total_amount`: Total sebelum pajak
- `tax_amount`: Jumlah pajak
- `discount_amount`: Diskon (future feature)
- `final_amount`: Total akhir
- `payment_method`: Metode pembayaran
- `customer_name`: Nama pelanggan
- `cashier_name`: Nama kasir

### Tabel Transaction Items
- `id`: Primary key
- `transaction_id`: Foreign key ke transactions
- `menu_item_id`: Foreign key ke menu_items
- `quantity`: Jumlah
- `unit_price`: Harga satuan
- `total_price`: Total harga item
- `notes`: Catatan khusus

## Instalasi & Setup

### 1. Clone atau Download Project
```bash
# Jika menggunakan git
git clone <repository-url>
cd cafe-pos-system

# Atau download dan extract file ZIP
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Aplikasi

#### Development Mode:
```bash
python main.py
```

#### Build ke Executable:
```bash
python build.py
```

Executable akan tersedia di folder `dist/CafePOS.exe`

## File Structure

```
cafe-pos-system/
├── main.py                 # Entry point aplikasi
├── main_window.py          # Main window dan UI utama
├── database.py             # Database operations dan CRUD
├── receipt_printer.py      # PDF receipt generator
├── reports_window.py       # Window laporan dan analytics
├── requirements.txt        # Python dependencies
├── build.py               # Build script untuk PyInstaller
├── cafe_pos.spec          # PyInstaller configuration
├── README.md              # Dokumentasi
├── receipts/              # Folder output struk PDF
└── cafe_pos.db           # SQLite database (auto-generated)
```

## Penggunaan Aplikasi

### 1. Menu Management
- Aplikasi sudah dilengkapi dengan sample data menu
- Menu terbagi dalam 3 kategori utama
- Klik tombol kategori untuk filter menu
- Klik "Tambah ke Keranjang" untuk menambah item

### 2. Proses Transaksi
1. **Pilih Menu**: Browse dan pilih menu dari kategori yang tersedia
2. **Review Keranjang**: Cek item, quantity, dan total
3. **Input Data**: Masukkan nama pelanggan (opsional)
4. **Pilih Pembayaran**: Tentukan metode pembayaran
5. **Checkout**: Klik tombol checkout untuk finalisasi
6. **Struk Otomatis**: Sistem akan generate dan simpan struk PDF

### 3. Laporan
- Akses melalui tombol "Laporan" di panel kanan
- **Tab Harian**: Lihat performa penjualan hari ini
- **Tab Riwayat**: Browse transaksi dengan filter tanggal
- **Tab Popular**: Analisis produk terlaris
- Export laporan ke PDF dengan satu klik

## Kustomisasi

### Menambah Menu Baru
Edit file `database.py` di fungsi `insert_initial_data()`:

```python
# Tambah menu baru
('Nama Menu Baru', harga, category_id, 'Deskripsi'),
```

### Mengubah Pajak
Edit di `main_window.py`:

```python
tax = subtotal * 0.12  # Ganti 0.12 (12%) dengan persentase yang diinginkan
```

### Styling UI
Semua styling CSS ada di `main_window.py` dalam method `setStyleSheet()`. Anda bisa memodifikasi:
- Warna tema
- Font size
- Border radius
- Hover effects
- Dan lainnya

## Build untuk Distribusi

### Windows:
```bash
python build.py
```

Hasil: `dist/CafePOS.exe` (single file executable)

### Linux/Mac:
```bash
python build.py
```

Hasil: `dist/CafePOS` (executable file)

### Tips Build:
- Pastikan semua dependencies sudah terinstall
- Build di environment yang sama dengan target deployment
- Test executable di komputer lain untuk memastikan tidak ada dependency yang terlewat

## Troubleshooting

### Database Issues
- Database akan otomatis terbuat saat pertama kali run
- Jika ada error, hapus file `cafe_pos.db` dan restart aplikasi
- Sample data akan auto-populate saat database pertama dibuat

### PDF Generation Issues
- Pastikan folder `receipts` memiliki permission write
- Jika error font, pastikan system fonts tersedia
- ReportLab membutuhkan write permission untuk temporary files

### Build Issues
```bash
# Clean build files
python build.py clean

# Upgrade build tools
pip install --upgrade pip setuptools wheel pyinstaller

# Build ulang
python build.py
```

### Missing DLL (Windows)
Jika ada error DLL saat run executable:
- Install Visual C++ Redistributable
- Atau build dengan flag `--onefile --windowed`

## Kontribusi

Untuk berkontribusi pada project ini:

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Lisensi

Project ini menggunakan lisensi MIT. Lihat file `LICENSE` untuk detail lengkap.

## Support

Jika mengalami masalah atau membutuhkan bantuan:

1. Cek bagian Troubleshooting di atas
2. Buka issue di repository GitHub
3. Sertakan informasi:
   - OS dan versi Python
   - Error message lengkap
   - Steps to reproduce

## Pengembangan Selanjutnya

Fitur yang bisa dikembangkan:
- [ ] User authentication dan multi-user
- [ ] Inventory management
- [ ] Customer loyalty program
- [ ] Integration dengan payment gateway
- [ ] Barcode scanner support
- [ ] Multi-language support
- [ ] Cloud backup database
- [ ] Real-time dashboard
- [ ] Mobile app companion

---

**Dibuat dengan ❤️ menggunakan Python dan PySide6**