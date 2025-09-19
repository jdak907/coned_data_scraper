from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import sys, os
from . import datafunctions as hu

def resource_path(relative_path: str) -> str:
    """Resolve asset paths for PyInstaller or local dev."""
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Utility Login")
        self.is_coned_login = True
        layout = QVBoxLayout(self)
        btn_coned = QPushButton("ConEd Login")
        btn_onr = QPushButton("O&R Login")
        btn_coned.clicked.connect(self._set_coned)
        btn_onr.clicked.connect(self._set_onr)
        layout.addWidget(btn_coned)
        layout.addWidget(btn_onr)
    def _set_coned(self):
        self.is_coned_login = True
        self.accept()
    def _set_onr(self):
        self.is_coned_login = False
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ConEd/O&R Data Utility")
        self.setGeometry(100, 100, 425, 400)
        self.status_label = QLabel("Offline ...")
        self.status_label.setStyleSheet("background-color: grey; color: white;")
        self.status_label.setFixedHeight(22)
        self.status_label.setContentsMargins(6, 0, 0, 0)
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        logo = QLabel(self)
        icon_path = resource_path("icons/coned_oru.png")
        if os.path.exists(icon_path):
            logo.setPixmap(QPixmap(icon_path))
            logo.setFixedSize(logo.sizeHint())
        btn_load = QPushButton("Load Account List")
        btn_load.clicked.connect(self._on_load)
        btn_login = QPushButton("Log In")
        btn_login.clicked.connect(self._on_login)
        btn_hu = QPushButton("Request HU Data")
        btn_hu.clicked.connect(self._on_hu)
        btn_idr = QPushButton("Request IDR Data Files")
        btn_idr.clicked.connect(self._on_idr)
        btn_quit = QPushButton("Quit")
        btn_quit.clicked.connect(self._on_quit)
        layout = QVBoxLayout()
        layout.addWidget(logo)
        layout.addWidget(btn_load)
        layout.addWidget(btn_login)
        layout.addWidget(btn_hu)
        layout.addWidget(btn_idr)
        layout.addWidget(btn_quit)
        layout.addWidget(self.status_label)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
    def _on_load(self):
        try:
            hu.load_accounts_list()
            self._set_status("Accounts loaded", "#1565c0")
        except Exception as e:
            self._err(str(e))
    def _on_login(self):
        dlg = LoginDialog(self)
        if dlg.exec():
            try:
                hu.log_in()
                self._set_status("Credentials OK", "#1b5e20")
                hu.log_in_mfa()
                self._set_status("MFA successful", "#2e7d32")
                if dlg.is_coned_login:
                    hu.coned_portal()
                    self._set_status("ConEd portal ready", "#1976d2")
                else:
                    hu.onr_portal()
                    self._set_status("O&R portal ready", "#ef6c00")
            except Exception as e:
                self._err(str(e))
    def _on_hu(self):
        try:
            hu.get_hu()
            self._set_status("HU requests complete", "#00695c")
        except Exception as e:
            self._err(str(e))
    def _on_idr(self):
        try:
            hu.get_idr()
            self._set_status("IDR requests complete", "#006064")
        except Exception as e:
            self._err(str(e))
    def _on_quit(self):
        try:
            if hu.driver:
                hu.driver.quit()
        finally:
            self.close()
    def _set_status(self, text: str, bg: str):
        self.status_label.setText(text + " ...")
        self.status_label.setStyleSheet(f"background-color: {bg}; color: white;")
    def _err(self, message: str):
        QMessageBox.critical(self, "Error", message)

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
