#!/usr/bin/env python3
"""
Script untuk build aplikasi menjadi executable dengan PyInstaller
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Jalankan command dan handle error"""
    print(f"\n{description}...")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {description} berhasil!")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} gagal!")
        print(f"Error: {e.stderr}")
        return False

def create_spec_file():
    """Buat file .spec untuk konfigurasi PyInstaller"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtWidgets', 
        'PySide6.QtGui',
        'reportlab.pdfgen',
        'reportlab.lib.pagesizes',
        'reportlab.platypus',
        'reportlab.lib.styles',
        'reportlab.lib.enums',
        'reportlab.lib.units',
        'reportlab.lib',
        'sqlite3'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CafePOS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version_file=None
)
'''
    
    with open('cafe_pos.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content.strip())
    
    print("✓ File cafe_pos.spec berhasil dibuat!")

def main():
    """Main build function"""
    print("=" * 60)
    print("CAFE POS - BUILD SCRIPT")
    print("=" * 60)
    
    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("✗ Error: File main.py tidak ditemukan!")
        print("Pastikan Anda menjalankan script ini di direktori yang sama dengan main.py")
        return False
    
    # Check if all required files exist
    required_files = [
        'main.py', 'main_window.py', 'database.py', 
        'receipt_printer.py', 'reports_window.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("✗ Error: File berikut tidak ditemukan:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("✓ Semua file yang diperlukan ditemukan!")
    
    # Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Menginstall dependencies"
    ):
        print("Mencoba install dependencies satu per satu...")
        dependencies = ['PySide6>=6.5.0', 'reportlab>=4.0.0', 'PyInstaller>=5.13.0']
        for dep in dependencies:
            run_command(f"{sys.executable} -m pip install {dep}", f"Install {dep}")
    
    # Create spec file
    create_spec_file()
    
    # Build with PyInstaller
    if not run_command(
        "pyinstaller --clean cafe_pos.spec",
        "Building aplikasi dengan PyInstaller"
    ):
        return False
    
    # Check if build successful
    if os.path.exists('dist/CafePOS.exe') or os.path.exists('dist/CafePOS'):
        print("\n" + "=" * 60)
        print("✓ BUILD BERHASIL!")
        print("=" * 60)
        print(f"Executable tersedia di: {os.path.abspath('dist')}")
        
        # Show file size
        exe_path = 'dist/CafePOS.exe' if os.path.exists('dist/CafePOS.exe') else 'dist/CafePOS'
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"Ukuran file: {size_mb:.1f} MB")
        
        print("\nCara menjalankan:")
        print("1. Buka folder 'dist'")
        print("2. Jalankan file 'CafePOS.exe' (Windows) atau 'CafePOS' (Linux/Mac)")
        print("\nCatatan:")
        print("- Pastikan folder 'dist' dan semua isinya disalin bersama-sama")
        print("- Database SQLite akan otomatis dibuat saat pertama kali dijalankan")
        print("- Folder 'receipts' akan dibuat otomatis untuk menyimpan struk dan laporan")
        
        return True
    else:
        print("\n✗ BUILD GAGAL!")
        print("File executable tidak ditemukan di folder dist/")
        return False

def clean_build():
    """Bersihkan file build"""
    print("Membersihkan file build...")
    
    folders_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['cafe_pos.spec']
    
    for folder in folders_to_remove:
        if os.path.exists(folder):
            run_command(f"rmdir /s /q {folder}" if os.name == 'nt' else f"rm -rf {folder}", 
                       f"Menghapus folder {folder}")
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"✓ File {file} dihapus!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_build()
    else:
        success = main()
        
        if not success:
            print("\nJika masih ada error, coba:")
            print("1. python build.py clean  # untuk membersihkan build sebelumnya")
            print("2. pip install --upgrade pip setuptools wheel")
            print("3. python build.py  # build ulang")
            sys.exit(1)