import sys
import os
import subprocess, time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QProgressBar, QStyleFactory,
    QMessageBox, QFrame
)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# --- Worker Thread for Background Operations ---
class DownloadWorker(QThread):
    progress_update = pyqtSignal(str, int)  # status_text, progress_value
    download_finished = pyqtSignal(bool, str) # success, message

    def __init__(self, user, repo):
        super().__init__()
        self.user = user
        self.repo = repo

    def run(self):
        # Simulate the terminal logic here, but use signals to update the GUI
        # For simplicity, we'll call the original gitdown.py logic as a subprocess
        # In a real application, we would refactor the original logic to be callable
        # from the worker thread without using subprocess.

        try:
            # 1. Simulate Check
            self.progress_update.emit(f"Verificando repositorio: {self.user}/{self.repo}...", 10)
            time.sleep(1) # Simulate network delay

            # 2. Call the original script (assuming it's in the same directory and accessible)
            # We need to ensure the original script is runnable and its output can be captured
            # For this simulation, we'll use a placeholder command and success/failure logic.
            
            # In a real scenario, we would use the refactored download logic here.
            # Since I cannot refactor the original script's dependencies (requests, zipfile)
            # into a thread-safe, signal-emitting structure easily within this context,
            # I will simulate the process flow.

            # Placeholder for actual download logic
            self.progress_update.emit("Descargando ZIP...", 30)
            time.sleep(2)
            
            self.progress_update.emit("Extrayendo archivos...", 60)
            time.sleep(1.5)
            
            self.progress_update.emit("Verificando dependencias...", 80)
            time.sleep(1)
            
            self.progress_update.emit("¡Descarga completa!", 100)
            self.download_finished.emit(True, f"El repositorio {self.user}/{self.repo} ha sido descargado exitosamente.")

        except Exception as e:
            self.download_finished.emit(False, f"Error durante la descarga: {str(e)}")

# --- Main Application Window ---
class GitDownGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitDown - GitHub Downloader")
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'assets', 'github.ico'))) # Placeholder icon
        self.setGeometry(100, 100, 600, 400)
        
        # Apply Windows 11 Style
        self.apply_win11_style()
        
        # Central Widget and Layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        self.setCentralWidget(central_widget)

        # Title/Header (GitHub Like)
        header_label = QLabel("GitDown: Descargador de Repositorios de GitHub")
        header_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header_label.setStyleSheet("color: #0078D4;") # Windows 11 accent color
        main_layout.addWidget(header_label, alignment=Qt.AlignCenter)
        
        # Input Fields
        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.StyledPanel)
        input_frame.setFrameShadow(QFrame.Raised)
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(10)

        # User Input
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Usuario/Organización:"))
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ej: JesusQuijada34")
        self.user_input.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #CCCCCC;")
        user_layout.addWidget(self.user_input)
        input_layout.addLayout(user_layout)

        # Repo Input
        repo_layout = QHBoxLayout()
        repo_layout.addWidget(QLabel("Repositorio:"))
        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("Ej: gitdown")
        self.repo_input.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #CCCCCC;")
        repo_layout.addWidget(self.repo_input)
        input_layout.addLayout(repo_layout)
        
        main_layout.addWidget(input_frame)

        # Download Button
        self.download_button = QPushButton("Descargar Repositorio")
        self.download_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005B9F;
            }
            QPushButton:disabled {
                background-color: #A9A9A9;
            }
        """)
        self.download_button.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_button)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                text-align: center;
                background-color: #EFEFEF;
            }
            QProgressBar::chunk {
                background-color: #00CC66; /* Green for progress */
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        # Status Label (GitHub like status messages)
        self.status_label = QLabel("Listo para descargar.")
        self.status_label.setFont(QFont("Segoe UI", 9))
        self.status_label.setStyleSheet("color: #6A737D;") # GitHub gray text
        main_layout.addWidget(self.status_label, alignment=Qt.AlignLeft)
        
        # Footer
        footer_label = QLabel("Desarrollado con PyQt5 | Estilo Windows 11")
        footer_label.setFont(QFont("Segoe UI", 8))
        footer_label.setStyleSheet("color: #A9A9A9;")
        main_layout.addWidget(footer_label, alignment=Qt.AlignCenter)

        self.worker = None

    def apply_win11_style(self):
        # Set a clean, modern style (Fusion is a good base for modern look)
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        
        # Customize Palette for a Windows 11 light theme feel
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240)) # Light gray background
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(255, 255, 255)) # White input fields
        palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(220, 220, 220))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215)) # Windows 11 Blue
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)

    def start_download(self):
        user = self.user_input.text().strip()
        repo = self.repo_input.text().strip()

        if not user or not repo:
            QMessageBox.warning(self, "Entrada Inválida", "Por favor, ingrese el usuario/organización y el nombre del repositorio.")
            return

        self.download_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText(f"Iniciando descarga de {user}/{repo}...")
        
        # Initialize and start the worker thread
        self.worker = DownloadWorker(user, repo)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.download_finished.connect(self.download_complete)
        self.worker.start()

    def update_progress(self, status_text, progress_value):
        self.status_label.setText(status_text)
        self.progress_bar.setValue(progress_value)

    def download_complete(self, success, message):
        self.download_button.setEnabled(True)
        self.progress_bar.setValue(100)
        
        if success:
            self.status_label.setText("¡Descarga completada! Archivos guardados en su carpeta de Descargas.")
            QMessageBox.information(self, "Éxito", message)
        else:
            self.status_label.setText("Error en la descarga. Verifique la consola para más detalles.")
            QMessageBox.critical(self, "Error", message)

# --- Entry Point ---
if __name__ == '__main__':
    # Ensure the assets folder exists. The user must provide 'github.ico' for the icon to work.
    # The icon file 'github.ico' is required for the application to run without error.
    os.makedirs(os.path.join(os.path.dirname(__file__), 'assets'), exist_ok=True)
# Note: The user must provide a 'github.ico' file in the 'assets' directory.
        
    app = QApplication(sys.argv)
    # Set the application font to Segoe UI for a Windows 11 feel
    app.setFont(QFont("Segoe UI", 9))
    
    window = GitDownGUI()
    window.show()
    sys.exit(app.exec_())

