from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)

from PySide6.QtGui import (
    QColor,
    QPalette,
)

from PySide6.QtWidgets import QApplication


def _obtener_colores_cambio(tipo: str, es_oscuro: bool):
    """
    Devuelve la pareja (fondo, texto) con contraste adecuado
    según el tipo de cambio y si el tema es oscuro o claro.
    """

    if es_oscuro:
        if tipo == "NUEVO":
            return QColor(20, 60, 30), QColor(140, 230, 160)
        if tipo == "ELIMINADO":
            return QColor(70, 25, 25), QColor(255, 160, 160)
        if tipo == "MODIFICADO":
            return QColor(65, 50, 15), QColor(255, 220, 130)
    else:
        if tipo == "NUEVO":
            return QColor("#C3FAC4"), QColor("#1A2530")
        if tipo == "ELIMINADO":
            return QColor("#FF746C"), QColor("#FFFFFF")
        if tipo == "MODIFICADO":
            return QColor("#FFEE8C"), QColor("#1A2530")

    return None, None


class ModeloCambios(QAbstractTableModel):

    COLUMNAS = [
        "Clave",
        "Tipo",
        "Columna",
    ]

    def __init__(self, cambios=None):
        super().__init__()

        self.cambios = cambios or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.cambios)

    def columnCount(
        self,
        parent=QModelIndex(),
    ):
        return len(self.COLUMNAS)

    def data(
        self,
        index,
        role=Qt.ItemDataRole.DisplayRole,
    ):

        if not index.isValid():
            return None

        cambio = self.cambios[index.row()]

        # =========================================================
        # TEXTO
        # =========================================================

        if role == Qt.ItemDataRole.DisplayRole:

            valores = [
                cambio.clave,
                cambio.tipo,
                cambio.columna,
            ]

            valor = valores[index.column()]

            if valor is None:
                return ""

            return str(valor)

        # =========================================================
        # ESTILOS DE COLOR DE FONDO Y TEXTO
        # =========================================================

        paleta = QApplication.palette()
        fondo_base = paleta.color(QPalette.ColorRole.Base)
        es_oscuro = fondo_base.lightness() < 128

        fondo, texto = _obtener_colores_cambio(cambio.tipo, es_oscuro)

        if role == Qt.ItemDataRole.BackgroundRole:
            return fondo

        if role == Qt.ItemDataRole.ForegroundRole:
            return texto

        return None

    def headerData(
        self,
        section,
        orientation,
        role=Qt.ItemDataRole.DisplayRole,
    ):

        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:

            return self.COLUMNAS[section]

        return str(section + 1)

    def actualizar(
        self,
        cambios,
    ):

        self.beginResetModel()

        self.cambios = cambios

        self.endResetModel()

    def obtener_cambio(
        self,
        fila: int,
    ):
        """
        Devuelve el objeto Cambio correspondiente
        a una fila del modelo.
        """

        if fila < 0 or fila >= len(self.cambios):
            return None

        return self.cambios[fila]
