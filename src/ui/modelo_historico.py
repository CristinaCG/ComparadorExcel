from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)

from PySide6.QtGui import (
    QColor,
)

from src.ui.modelo_cambios import _obtener_colores_cambio


class ModeloHistorico(QAbstractTableModel):

    COLUMNAS = [
        "Identificador",
        "Clave",
        "Tipo",
        "Columna",
        # "Valor 1",
        # "Valor 2",
    ]

    def __init__(self, cambios=None):
        super().__init__()

        self.cambios = list(cambios or [])

    def rowCount(
        self,
        parent=QModelIndex(),
    ):
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
                cambio["identificador"],
                cambio["clave"],
                cambio["tipo"],
                cambio["columna"],
                # cambio["valor_1"],
                # cambio["valor_2"],
            ]

            valor = valores[index.column()]

            if valor is None:
                return ""

            return str(valor)

        # =========================================================
        # ESTILOS DE COLOR DE FONDO Y TEXTO
        # =========================================================

        if role in (Qt.ItemDataRole.BackgroundRole, Qt.ItemDataRole.ForegroundRole):
            fondo, texto = _obtener_colores_cambio(cambio["tipo"])

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

        self.cambios = list(cambios)

        self.endResetModel()

    def obtener_cambio(
        self,
        fila: int,
    ):

        if fila < 0 or fila >= len(self.cambios):
            return None

        return self.cambios[fila]
