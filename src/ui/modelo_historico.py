from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)


class ModeloHistorico(QAbstractTableModel):

    COLUMNAS = [
        "Fecha",
        "Identificador",
        "Archivo anterior",
        "Archivo nuevo",
        "Hoja anterior",
        "Hoja nueva",
        "Cambios",
    ]

    def __init__(self):
        super().__init__()

        self.comparaciones = []

    def rowCount(
        self,
        parent=QModelIndex(),
    ):
        return len(self.comparaciones)

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

        if role != Qt.ItemDataRole.DisplayRole:
            return None

        comparacion = self.comparaciones[
            index.row()
        ]

        valores = [
            comparacion["fecha"],
            comparacion["identificador"],
            comparacion["archivo_anterior"],
            comparacion["archivo_nuevo"],
            comparacion["hoja_anterior"],
            comparacion["hoja_nueva"],
            comparacion.get("num_cambios", 0),
        ]

        valor = valores[index.column()]

        if valor is None:
            return ""

        return str(valor)

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
        comparaciones,
    ):

        self.beginResetModel()

        self.comparaciones = comparaciones

        self.endResetModel()

    def obtener_comparacion(
        self,
        fila: int,
    ):
        if fila < 0 or fila >= len(self.comparaciones):
            return None

        return self.comparaciones[fila]