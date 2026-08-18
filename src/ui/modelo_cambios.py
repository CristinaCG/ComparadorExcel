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


def _mezclar_color(
    color_base,
    color_cambio,
    porcentaje,
):
    """
    Mezcla un color de fondo con un color indicador.
    """

    r = int(
        color_base.red() * (1 - porcentaje)
        + color_cambio.red() * porcentaje
    )

    g = int(
        color_base.green() * (1 - porcentaje)
        + color_cambio.green() * porcentaje
    )

    b = int(
        color_base.blue() * (1 - porcentaje)
        + color_cambio.blue() * porcentaje
    )

    return QColor(r, g, b)


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
        # COLOR DE FONDO
        # =========================================================

        if role == Qt.ItemDataRole.BackgroundRole:

            paleta = QApplication.palette()

            fondo = paleta.color(
                QPalette.ColorRole.Base
            )

            if cambio.tipo == "NUEVO":

                return _mezclar_color(
                    fondo,
                    QColor(80, 180, 80),
                    0.18,
                )

            if cambio.tipo == "ELIMINADO":

                return _mezclar_color(
                    fondo,
                    QColor(220, 80, 80),
                    0.18,
                )

            if cambio.tipo == "MODIFICADO":

                return _mezclar_color(
                    fondo,
                    QColor(230, 190, 50),
                    0.22,
                )

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