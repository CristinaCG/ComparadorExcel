from pathlib import Path

from difflib import SequenceMatcher

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
)

from qextrawidgets.widgets.views import QFilterableTableView

from src.ui.ui_main_window import Ui_MainWindow

# from src.ui.filtro_tabla import (
#     ModeloFiltradoCambios,
#     CabeceraFiltrable,
# )

from src.excel.lector import (
    obtener_hojas,
    leer_excel,
)

from src.excel.analizador import (
    obtener_columnas_comunes,
    obtener_columnas_nuevas,
    obtener_columnas_eliminadas,
)

from src.ui.modelo_cambios import ModeloCambios

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._crear_tabla_filtrable()

        self.modelo_cambios = ModeloCambios()

        self.ui.tableViewCambios.setModel(
            self.modelo_cambios
        )

        # self.modelo_cambios = ModeloCambios()

        # self.modelo_filtrado = ModeloFiltradoCambios()

        # self.modelo_filtrado.setSourceModel(
        #     self.modelo_cambios
        # )

        # self.ui.tableViewCambios.setModel(
        #     self.modelo_filtrado
        # )

        # self.ui.tableViewCambios.setSortingEnabled(True)

        # Cabecera con filtros
        # cabecera = CabeceraFiltrable(
        #     Qt.Orientation.Horizontal,
        #     self.ui.tableViewCambios,
        # )

        # self.ui.tableViewCambios.setHorizontalHeader(
        #     cabecera
        # )

        self.ui.lineEditBuscarClave.textChanged.connect(
            lambda texto: self._filtrar_lista(
                self.ui.listaColumnasClave,
                texto,
            )
        )

        self.ui.lineEditBuscarComparar.textChanged.connect(
            lambda texto: self._filtrar_lista(
                self.ui.listaColumnasComparar,
                texto,
            )
        )

        # DataFrames actualmente cargados
        self.df_1 = None
        self.df_2 = None

        self._conectar_eventos()

        self._inicializar_interfaz()

    # =========================================================
    # INICIALIZACIÓN
    # =========================================================

    def _inicializar_interfaz(self):
        """
        Configuración inicial de la interfaz.
        """

        self.ui.listaColumnasClave.clear()
        self.ui.listaColumnasComparar.clear()

        self.ui.labelResumen.setText(
            "0 cambios encontrados"
        )

    # =========================================================
    # EVENTOS
    # =========================================================

    def _conectar_eventos(self):
        """
        Conecta los controles de la interfaz con sus funciones.
        """

        self.ui.pushButtonArchivo1.clicked.connect(
            self.seleccionar_archivo_1
        )

        self.ui.pushButtonArchivo2.clicked.connect(
            self.seleccionar_archivo_nuevo
        )

        self.ui.comboBoxHoja1.currentTextChanged.connect(
            self.cargar_hoja_1
        )

        self.ui.comboBoxHoja2.currentTextChanged.connect(
            self.cargar_hoja_2
        )

        self.ui.pushButtonComparar.clicked.connect(
            self.comparar
        )

        self.ui.tableViewCambios.clicked.connect(
            self.mostrar_detalle_cambio
        )

    def _filtrar_lista(
        self,
        lista,
        texto: str,
    ):
        texto = texto.strip().lower()

        for i in range(lista.count()):

            item = lista.item(i)

            visible = (
                texto == ""
                or texto in item.text().lower()
            )

            item.setHidden(
                not visible
            )

    def _texto_con_diferencias(
        self,
        texto_anterior: str,
        texto_nuevo: str,
        mostrar_anterior: bool,
    ) -> str:
        """
        Genera HTML resaltando con fondo amarillo suave las partes
        diferentes entre el valor anterior y el nuevo.

        El color se adapta al tema claro/oscuro de Qt.
        """

        # ---------------------------------------------------------
        # Color de resaltado según el tema
        # ---------------------------------------------------------

        from PySide6.QtWidgets import QApplication
        from PySide6.QtGui import QPalette

        paleta = QApplication.palette()

        fondo = paleta.color(
            QPalette.ColorRole.Base
        )

        # Amarillo de referencia
        amarillo = (220, 180, 40)

        # En función del fondo actual hacemos una mezcla
        porcentaje = 0.35

        rojo = int(
            fondo.red() * (1 - porcentaje)
            + amarillo[0] * porcentaje
        )

        verde = int(
            fondo.green() * (1 - porcentaje)
            + amarillo[1] * porcentaje
        )

        azul = int(
            fondo.blue() * (1 - porcentaje)
            + amarillo[2] * porcentaje
        )

        color_resaltado = (
            f"rgb({rojo},{verde},{azul})"
        )

        # ---------------------------------------------------------
        # Comparar textos
        # ---------------------------------------------------------

        matcher = SequenceMatcher(
            None,
            texto_anterior,
            texto_nuevo,
        )

        resultado = []

        for etiqueta, i1, i2, j1, j2 in matcher.get_opcodes():

            if mostrar_anterior:
                texto = texto_anterior[i1:i2]
            else:
                texto = texto_nuevo[j1:j2]

            if not texto:
                continue

            # -----------------------------------------------------
            # Escapar HTML
            # -----------------------------------------------------

            texto = (
                texto
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br>")
            )

            # -----------------------------------------------------
            # Resaltar diferencia
            # -----------------------------------------------------

            if etiqueta != "equal":

                texto = (
                    f'<span style="background-color: {color_resaltado};">'
                    f"{texto}"
                    "</span>"
                )

            resultado.append(texto)

        return "".join(resultado)

    def _mostrar_valores_con_diferencias(
        self,
        valor_1,
        valor_2,
    ):
        """
        Muestra los valores anterior y nuevo resaltando
        las diferencias.
        """

        texto_anterior = (
            ""
            if valor_1 is None
            else str(valor_1)
        )

        texto_nuevo = (
            ""
            if valor_2 is None
            else str(valor_2)
        )

        # Si ambos valores son iguales, no hay nada que resaltar.
        if texto_anterior == texto_nuevo:

            self.ui.textEditValor1.setPlainText(
                texto_anterior
            )

            self.ui.textEditValor2.setPlainText(
                texto_nuevo
            )

            return

        html_anterior = self._texto_con_diferencias(
            texto_anterior,
            texto_nuevo,
            True,
        )

        html_nuevo = self._texto_con_diferencias(
            texto_anterior,
            texto_nuevo,
            False,
        )

        self.ui.textEditValor1.setHtml(
            html_anterior
        )

        self.ui.textEditValor2.setHtml(
            html_nuevo
        )

    def _crear_tabla_filtrable(self):
        """
        Sustituye el QTableView definido en Qt Designer
        por QFilterableTableView.

        El widget original se conserva hasta comprobar
        que el nuevo funciona correctamente.
        """

        tabla_original = self.ui.tableViewCambios

        tabla_filtrable = QFilterableTableView(
            tabla_original.parent()
        )

        tabla_filtrable.setObjectName(
            "tableViewCambios"
        )

        # Mantener algunas propiedades visuales
        tabla_filtrable.setMinimumSize(
            tabla_original.minimumSize()
        )

        tabla_filtrable.setSizePolicy(
            tabla_original.sizePolicy()
        )

        tabla_filtrable.setAlternatingRowColors(
            tabla_original.alternatingRowColors()
        )

        # Sustituir el widget dentro del layout
        layout = tabla_original.parentWidget().layout()

        if layout is not None:
            layout.replaceWidget(
                tabla_original,
                tabla_filtrable
            )

        tabla_original.deleteLater()

        # Actualizamos la referencia generada por Qt Designer
        self.ui.tableViewCambios = tabla_filtrable

    # =========================================================
    # ARCHIVO 1
    # =========================================================

    def seleccionar_archivo_1(self):
        """
        Permite seleccionar el Excel 1.
        """

        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Excel 1",
            "",
            "Archivos Excel (*.xlsx *.xls)",
        )

        if not ruta:
            return

        self.ui.lineEditArchivo1.setText(ruta)

        self.df_1 = None

        self._cargar_hojas(
            ruta,
            self.ui.comboBoxHoja1,
        )

        self._actualizar_columnas()

    # =========================================================
    # ARCHIVO NUEVO
    # =========================================================

    def seleccionar_archivo_nuevo(self):
        """
        Permite seleccionar el Excel nuevo.
        """

        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Excel nuevo",
            "",
            "Archivos Excel (*.xlsx *.xls)",
        )

        if not ruta:
            return

        self.ui.lineEditArchivo2.setText(ruta)

        self.df_2 = None

        self._cargar_hojas(
            ruta,
            self.ui.comboBoxHoja2,
        )

        self._actualizar_columnas()

    # =========================================================
    # CARGAR HOJAS
    # =========================================================

    def _cargar_hojas(
        self,
        ruta: str,
        combo_box,
    ):
        """
        Carga las hojas del Excel seleccionado.
        """

        try:

            hojas = obtener_hojas(ruta)

            combo_box.blockSignals(True)

            combo_box.clear()
            combo_box.addItems(hojas)

            combo_box.blockSignals(False)

            # Si hay hojas, cargamos la primera
            if hojas:
                self._cargar_hoja_seleccionada(
                    combo_box
                )

        except Exception as error:

            combo_box.blockSignals(False)

            QMessageBox.critical(
                self,
                "Error al leer Excel",
                f"No se ha podido leer el archivo:\n\n{error}",
            )

    # =========================================================
    # HOJA 1
    # =========================================================

    def cargar_hoja_1(
        self,
        nombre_hoja: str,
    ):
        """
        Carga la hoja seleccionada del Excel 1.
        """

        if not nombre_hoja:
            self.df_1 = None
            self._actualizar_columnas()
            return

        ruta = self.ui.lineEditArchivo1.text()

        if not ruta:
            return

        try:

            self.df_1 = leer_excel(
                ruta,
                nombre_hoja,
            )

            self._actualizar_columnas()

        except Exception as error:

            self.df_1 = None

            QMessageBox.critical(
                self,
                "Error al leer hoja",
                f"No se ha podido leer la hoja:\n\n{error}",
            )

    # =========================================================
    # HOJA 2
    # =========================================================

    def cargar_hoja_2(
        self,
        nombre_hoja: str,
    ):
        """
        Carga la hoja seleccionada del Excel nuevo.
        """

        if not nombre_hoja:
            self.df_2 = None
            self._actualizar_columnas()
            return

        ruta = self.ui.lineEditArchivo2.text()

        if not ruta:
            return

        try:

            self.df_2 = leer_excel(
                ruta,
                nombre_hoja,
            )

            self._actualizar_columnas()

        except Exception as error:

            self.df_2 = None

            QMessageBox.critical(
                self,
                "Error al leer hoja",
                f"No se ha podido leer la hoja:\n\n{error}",
            )

    # =========================================================
    # CARGAR HOJA SELECCIONADA
    # =========================================================

    def _cargar_hoja_seleccionada(
        self,
        combo_box,
    ):
        """
        Fuerza la carga de la hoja actualmente seleccionada.
        """

        nombre_hoja = combo_box.currentText()

        if combo_box is self.ui.comboBoxHoja1:
            self.cargar_hoja_1(nombre_hoja)

        elif combo_box is self.ui.comboBoxHoja2:
            self.cargar_hoja_2(nombre_hoja)

    # =========================================================
    # ACTUALIZAR COLUMNAS
    # =========================================================

    def _actualizar_columnas(self):
        """
        Actualiza las columnas disponibles para seleccionar.

        Sólo se muestran las columnas presentes en ambos Excel.
        """

        # Todavía no tenemos ambos DataFrames
        if (
            self.df_1 is None
            or self.df_2 is None
        ):
            self.ui.listaColumnasClave.clear()
            self.ui.listaColumnasComparar.clear()
            return

        columnas_comunes = obtener_columnas_comunes(
            self.df_1,
            self.df_2,
        )

        columnas_2 = obtener_columnas_nuevas(
            self.df_1,
            self.df_2,
        )

        columnas_eliminadas = obtener_columnas_eliminadas(
            self.df_1,
            self.df_2,
        )

        self.ui.listaColumnasClave.clear()
        self.ui.listaColumnasComparar.clear()

        self.ui.listaColumnasClave.addItems(
            columnas_comunes
        )

        self.ui.listaColumnasComparar.addItems(
            columnas_comunes
        )

        # Mostrar información de estructura
        self._mostrar_informacion_columnas(
            columnas_2,
            columnas_eliminadas,
        )

    # =========================================================
    # INFORMACIÓN DE COLUMNAS
    # =========================================================

    def _mostrar_informacion_columnas(
        self,
        columnas_2: list[str],
        columnas_eliminadas: list[str],
    ):
        """
        Muestra información sobre diferencias estructurales.
        """

        mensajes = []

        if columnas_2:

            mensajes.append(
                "Columnas 2: "
                + ", ".join(columnas_2)
            )

        if columnas_eliminadas:

            mensajes.append(
                "Columnas eliminadas: "
                + ", ".join(columnas_eliminadas)
            )

        if mensajes:

            self.ui.statusbar.showMessage(
                " | ".join(mensajes)
            )

        else:

            self.ui.statusbar.showMessage(
                "Las estructuras de ambos Excel coinciden."
            )

    # =========================================================
    # COMPARAR
    # =========================================================

    def comparar(self):
        """
        Ejecuta la comparación de los dos Excel.
        """

        # ---------------------------------------------------------
        # Comprobar que tenemos los dos archivos
        # ---------------------------------------------------------

        if self.df_1 is None:

            QMessageBox.warning(
                self,
                "Falta el Excel anterior",
                "Selecciona el Excel anterior.",
            )

            return

        if self.df_2 is None:

            QMessageBox.warning(
                self,
                "Falta el Excel nuevo",
                "Selecciona el Excel nuevo.",
            )

            return

        # ---------------------------------------------------------
        # Obtener columnas seleccionadas
        # ---------------------------------------------------------

        columnas_clave = [
            item.text()
            for item in self.ui.listaColumnasClave.selectedItems()
        ]

        columnas_comparar = [
            item.text()
            for item in self.ui.listaColumnasComparar.selectedItems()
        ]

        # ---------------------------------------------------------
        # Validar clave
        # ---------------------------------------------------------

        if not columnas_clave:

            QMessageBox.warning(
                self,
                "Falta la clave",
                "Selecciona al menos una columna clave.",
            )

            return

        # ---------------------------------------------------------
        # Validar columnas a comparar
        # ---------------------------------------------------------

        if not columnas_comparar:

            QMessageBox.warning(
                self,
                "Faltan columnas",
                "Selecciona al menos una columna a comparar.",
            )

            return

        # ---------------------------------------------------------
        # Ejecutar comparación
        # ---------------------------------------------------------

        try:

            from src.excel.comparador import comparar_dataframes

            cambios = comparar_dataframes(
                self.df_1,
                self.df_2,
                columnas_clave=columnas_clave,
                columnas_comparar=columnas_comparar,
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error durante la comparación",
                f"No se ha podido comparar los archivos:\n\n{error}",
            )

            return

        # ---------------------------------------------------------
        # Mostrar resultados
        # ---------------------------------------------------------

        self.modelo_cambios.actualizar(cambios)

        self.ui.labelResumen.setText(
            f"{len(cambios)} cambios encontrados"
        )

        # Ajustar columnas
        self.ui.tableViewCambios.resizeColumnsToContents()

        self.ui.statusbar.showMessage(
            "Comparación completada correctamente."
        )

    def _obtener_fila_modelo_origen(self, index):
        """
        Obtiene la fila correspondiente al ModeloCambios
        partiendo del índice de la tabla filtrable.
        """

        indice = index

        while indice.isValid():

            modelo = indice.model()

            if modelo is self.modelo_cambios:
                return indice.row()

            if hasattr(modelo, "mapToSource"):

                indice = modelo.mapToSource(indice)

            else:
                break

        return -1

    def mostrar_detalle_cambio(self, index):

        if not index.isValid():
            return

        fila = self._obtener_fila_modelo_origen(index)

        if fila < 0:
            return

        cambio = self.modelo_cambios.obtener_cambio(fila)

        if cambio is None:
            return

        self._mostrar_valores_con_diferencias(
            cambio.valor_1,
            cambio.valor_2,
        )