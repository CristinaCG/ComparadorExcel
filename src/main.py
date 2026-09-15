import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


def resource_path(relative_path):
    """Obtiene la ruta correcta en desarrollo y en el .exe de PyInstaller."""
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent

    return base_path / relative_path


def main():
    app = QApplication(sys.argv)

    # Icono de la aplicación/ventana
    icon_path = resource_path("images/pine_logo.ico")
    app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()