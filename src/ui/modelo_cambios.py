from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)

from PySide6.QtGui import (
    QColor
)

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

        # ---------------------------------------------------------
        # TEXTO
        # ---------------------------------------------------------


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

        # ---------------------------------------------------------
        # COLOR DE FONDO
        # ---------------------------------------------------------

        if role == Qt.ItemDataRole.BackgroundRole:

            if cambio.tipo == "NUEVO":
                return QColor(220, 245, 220)

            if cambio.tipo == "ELIMINADO":
                return QColor(250, 220, 220)

            if cambio.tipo == "MODIFICADO":
                return QColor(255, 245, 200)

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