from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QHeaderView, QMenu


class ModeloFiltradoCambios(QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.filtros = {}

    def set_filtro(self, columna, valores):
        """
        Aplica un filtro a una columna.

        valores:
            Conjunto de valores que queremos mostrar.
        """

        if valores:
            self.filtros[columna] = valores
        else:
            self.filtros.pop(columna, None)

        self.invalidateFilter()

    def limpiar_filtros(self):
        """Elimina todos los filtros."""

        self.filtros.clear()
        self.invalidateFilter()

    def filterAcceptsRow(
        self,
        source_row,
        source_parent,
    ):
        modelo = self.sourceModel()

        for columna, valores in self.filtros.items():

            index = modelo.index(
                source_row,
                columna,
                source_parent,
            )

            valor = modelo.data(
                index,
                Qt.ItemDataRole.DisplayRole,
            )

            if valor is None:
                valor = ""

            if str(valor) not in valores:
                return False

        return True


class CabeceraFiltrable(QHeaderView):

    def __init__(
        self,
        orientation,
        parent=None,
    ):
        super().__init__(
            orientation,
            parent,
        )

        self.setSectionsClickable(True)

        self.sectionClicked.connect(
            self.mostrar_filtro
        )

    def mostrar_filtro(self, columna):

        modelo = self.model()

        if modelo is None:
            return

        # -----------------------------------------------------
        # Obtener valores únicos
        # -----------------------------------------------------

        valores = set()

        for fila in range(modelo.rowCount()):

            index = modelo.index(
                fila,
                columna,
            )

            valor = modelo.data(
                index,
                Qt.ItemDataRole.DisplayRole,
            )

            if valor is None:
                valor = ""

            valores.add(str(valor))

        valores = sorted(valores)

        # -----------------------------------------------------
        # Crear menú
        # -----------------------------------------------------

        menu = QMenu(self)

        accion_todos = menu.addAction(
            "Todos"
        )

        menu.addSeparator()

        acciones = {}

        for valor in valores:

            accion = menu.addAction(
                valor
            )

            accion.setCheckable(True)
            accion.setChecked(True)

            acciones[accion] = valor

        menu.addSeparator()

        accion_limpiar = menu.addAction(
            "Limpiar filtro"
        )

        # -----------------------------------------------------
        # Mostrar menú
        # -----------------------------------------------------

        accion = menu.exec(
            self.mapToGlobal(
                self.rect().bottomLeft()
            )
        )

        if accion is None:
            return

        # -----------------------------------------------------
        # Todos
        # -----------------------------------------------------

        if accion == accion_todos:

            modelo.set_filtro(
                columna,
                None,
            )

            return

        # -----------------------------------------------------
        # Limpiar
        # -----------------------------------------------------

        if accion == accion_limpiar:

            modelo.set_filtro(
                columna,
                None,
            )

            return

        # -----------------------------------------------------
        # Aplicar selección
        # -----------------------------------------------------

        seleccionados = {
            valor
            for accion_item, valor
            in acciones.items()
            if accion_item.isChecked()
        }

        modelo.set_filtro(
            columna,
            seleccionados,
        )