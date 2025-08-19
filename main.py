import sys
from PySide6.QtWidgets import QApplication, QSplashScreen, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont
from main_window import MainWindow

class CafePOSApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Maron Cafe POS System")
        self.app.setApplicationVersion("1.0.0")
        
        # Set application style
        self.app.setStyle('Fusion')
        
        # Create and show splash screen
        self.show_splash()
        
        # Initialize main window
        self.main_window = MainWindow()
        
        # Setup timer to show main window after splash
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_main_window)
        self.timer.start(2000)  # Show splash for 2 seconds
    
    def show_splash(self):
        """Show splash screen"""
        # Create splash screen
        splash_pix = QPixmap(400, 300)
        splash_pix.fill(Qt.white)
        
        self.splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        
        # Add text to splash screen
        self.splash.showMessage(
            "Maron Cafe POS System\n\nRaga Triagantara\nVersi 1.0.0\n\nMemuat aplikasi...",
            Qt.AlignCenter | Qt.AlignBottom,
            Qt.black
        )
        
        # Set splash screen font
        font = QFont("Arial", 12)
        font.setBold(True)
        
        self.splash.show()
        self.app.processEvents()
    
    def show_main_window(self):
        """Show main window and close splash"""
        self.timer.stop()
        self.splash.close()
        self.main_window.show()
        self.main_window.activateWindow()
        self.main_window.raise_()
    
    def run(self):
        """Run the application"""
        return self.app.exec()

def main():
    """Main entry point"""
    try:
        app = CafePOSApp()
        sys.exit(app.run())
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()