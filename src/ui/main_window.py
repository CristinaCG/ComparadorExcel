from pathlib import Path

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFileDialog


class MainWindow:
    def __init__(self):
        ui_path = Path(__file__).parent / "main_window.ui"

        loader = QUiLoader()
        ui_file = QFile(str(ui_path))

        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(
                f"No se pudo abrir el archivo UI: {ui_path}"
            )

        self.ui = loader.load(ui_file)
        ui_file.close()

        if self.ui is None:
            raise RuntimeError("No se pudo cargar la interfaz.")

        self._conectar_eventos()

    def show(self):
        self.ui.show()

    def _conectar_eventos(self):
        self.ui.pushButtonArchivo1.clicked.connect(
            self.seleccionar_archivo1
        )

        self.ui.pushButtonArchivo2.clicked.connect(
            self.seleccionar_archivo2
        )

        self.ui.pushButtonComparar.clicked.connect(
            self.comparar
        )

    def seleccionar_archivo1(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self.ui,
            "Seleccionar Excel 1",
            "",
            "Archivos Excel (*.xlsx *.xls)"
        )

        if ruta:
            self.ui.lineEditArchivo1.setText(ruta)

    def seleccionar_archivo2(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self.ui,
            "Seleccionar Excel 2",
            "",
            "Archivos Excel (*.xlsx *.xls)"
        )

        if ruta:
            self.ui.lineEditArchivo2.setText(ruta)

    def comparar(self):
        print("Botón comparar pulsado")

    def show(self):
        self.ui.show()