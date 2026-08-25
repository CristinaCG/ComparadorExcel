from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font

from difflib import SequenceMatcher

from PySide6.QtCore import (
    Qt,
    QSortFilterProxyModel,
)

from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QInputDialog,
)

from src.database.repositorio import RepositorioSQLite

from qextrawidgets.widgets.views import QFilterableTableView

from src.ui.ui_main_window import Ui_MainWindow

from src.ui.modelo_historico import ModeloHistorico

from src.database.repositorio_configuracion import (
    RepositorioConfiguracion,
    obtener_ruta_configuracion,
)

from src.excel.firma import generar_firma_excel

from src.excel.lector import (
    obtener_hojas,
    leer_excel,
)

from src.excel.nombres import (
    obtener_nombre_bd,
    obtener_identificador_propuesto,
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

        # =========================================================
        # TABLAS FILTRABLES
        # =========================================================

        self._crear_tabla_filtrable(
            "tableViewCambios"
        )

        self._crear_tabla_filtrable(
            "tableViewHistorico"
        )

        # =========================================================
        # MODELOS
        # =========================================================

        self.modelo_cambios = ModeloCambios()

        self.ui.tableViewCambios.setModel(
            self.modelo_cambios
        )

        self.modelo_historico = ModeloHistorico()

        self.ui.tableViewHistorico.setModel(
            self.modelo_historico
        )

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

        # =========================================================
        # CONFIGURACIÓN EN CACHÉ
        # =========================================================

        self.repositorio_configuracion = (
            RepositorioConfiguracion(
                obtener_ruta_configuracion()
            )
        )

        self.firma_configuracion_actual = None
    
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

        self.ui.tableViewHistorico.clicked.connect(
            self.mostrar_detalle_historico
        )

        self.ui.pushButtonGuardarComparacion.clicked.connect(
            self.guardar_comparacion
        )

        self.ui.pushButtonAbrirHistorico.clicked.connect(
            self.abrir_historico
        )

        self.ui.pushButtonEliminarComparacion.clicked.connect(
            self.eliminar_comparacion_historico
        )

        self.ui.lineEditBuscarClaveHistorico.textChanged.connect(
            lambda _: self.filtrar_historico()
        )

        self.ui.comboBoxIdentificadorHistorico.currentTextChanged.connect(
            lambda _: self.filtrar_historico()
        )

        self.ui.pushButtonExportarHistorico.clicked.connect(
            self.exportar_historico_excel
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
        edit1,
        edit2
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
            edit1.setPlainText(texto_anterior)
            edit2.setPlainText(texto_nuevo)

            return

        html_anterior = self._texto_con_diferencias(
            texto_anterior,
            texto_nuevo,
            True,
        )

        html_nuevo = self._texto_con_diferencias(
            texto_anterior,
            texto_nuevo,
            True,
        )

        edit1.setHtml(html_anterior)
        edit2.setHtml(html_nuevo)

    def _crear_tabla_filtrable(
        self,
        nombre_tabla,
    ):
        """
        Sustituye un QTableView por QFilterableTableView.
        """

        tabla_original = getattr(
            self.ui,
            nombre_tabla,
        )

        tabla_filtrable = QFilterableTableView(
            tabla_original.parentWidget()
        )

        tabla_filtrable.setObjectName(
            nombre_tabla
        )

        # ---------------------------------------------------------
        # Copiar propiedades visuales
        # ---------------------------------------------------------

        tabla_filtrable.setMinimumSize(
            tabla_original.minimumSize()
        )

        tabla_filtrable.setSizePolicy(
            tabla_original.sizePolicy()
        )

        tabla_filtrable.setAlternatingRowColors(
            tabla_original.alternatingRowColors()
        )

        tabla_filtrable.setSortingEnabled(
            True
        )

        # ---------------------------------------------------------
        # Sustituir dentro del layout
        # ---------------------------------------------------------

        layout = tabla_original.parentWidget().layout()

        if layout is None:
            raise RuntimeError(
                f"No se ha encontrado el layout de {nombre_tabla}"
            )

        layout.replaceWidget(
            tabla_original,
            tabla_filtrable,
        )

        tabla_original.hide()
        tabla_original.deleteLater()

        # ---------------------------------------------------------
        # Actualizar referencia de Ui_MainWindow
        # ---------------------------------------------------------

        setattr(
            self.ui,
            nombre_tabla,
            tabla_filtrable,
        )

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
        
        self.firma_configuracion_actual = (
            generar_firma_excel(
                self.df_1,
                self.df_2,
            )
        )
            
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

        self._cargar_configuracion_cacheada()

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

            self.ui.statusBar.showMessage(
                " | ".join(mensajes)
            )

        else:

            self.ui.statusBar.showMessage(
                "Las estructuras de ambos Excel coinciden."
            )

    def _cargar_configuracion_cacheada(self):
        """
        Busca una configuración guardada para la estructura
        actual de los dos Excel y la aplica si existe.
        """

        if not self.firma_configuracion_actual:
            return False

        configuracion = (
            self.repositorio_configuracion
            .obtener_configuracion(
                self.firma_configuracion_actual
            )
        )

        if configuracion is None:
            return False

        # ---------------------------------------------------------
        # Seleccionar columnas clave
        # ---------------------------------------------------------

        self._seleccionar_items_lista(
            self.ui.listaColumnasClave,
            configuracion["columnas_clave"],
        )

        # ---------------------------------------------------------
        # Seleccionar columnas a comparar
        # ---------------------------------------------------------

        self._seleccionar_items_lista(
            self.ui.listaColumnasComparar,
            configuracion["columnas_comparadas"],
        )

        self.ui.statusBar.showMessage(
            "Configuración anterior recuperada automáticamente."
        )

        return True

    def _seleccionar_items_lista(
        self,
        lista,
        valores: list[str],
    ):
        """
        Selecciona en una QListWidget los elementos indicados.
        """

        valores = set(valores)

        for i in range(lista.count()):

            item = lista.item(i)

            item.setSelected(
                item.text() in valores
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

        self.repositorio_configuracion.guardar_configuracion(
            firma=self.firma_configuracion_actual,
            hoja_anterior=self.ui.comboBoxHoja1.currentText(),
            hoja_nueva=self.ui.comboBoxHoja2.currentText(),
            columnas_clave=columnas_clave,
            columnas_comparadas=columnas_comparar,
        )

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

        self.ui.tabWidget.setCurrentWidget(
            self.ui.tab_resultados
        )
        self.ui.labelResumen.setText(
            f"{len(cambios)} cambios encontrados"
        )

        # Ajustar columnas
        self.ui.tableViewCambios.resizeColumnsToContents()

        self.ui.statusBar.showMessage(
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

            if modelo is self.modelo_historico:
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
            self.ui.textEditValor1,
            self.ui.textEditValor2
        )

    def guardar_comparacion(self):
        """
        Guarda la comparación actual en una base de datos SQLite.

        El usuario puede:
        - Crear una nueva base de datos.
        - Añadir la comparación a una base de datos existente.
        """

        # =========================================================
        # COMPROBAR QUE EXISTE UNA COMPARACIÓN
        # =========================================================

        if not self.modelo_cambios.cambios:

            QMessageBox.warning(
                self,
                "Sin comparación",
                "Primero debes realizar una comparación.",
            )

            return

        # =========================================================
        # OBTENER ARCHIVOS ACTUALES
        # =========================================================

        archivo_anterior = self.ui.lineEditArchivo1.text().strip()
        archivo_nuevo = self.ui.lineEditArchivo2.text().strip()

        if not archivo_anterior or not archivo_nuevo:

            QMessageBox.warning(
                self,
                "Archivos no seleccionados",
                "Debes seleccionar los dos archivos Excel antes de guardar.",
            )

            return

        # =========================================================
        # ELEGIR DESTINO
        # =========================================================

        respuesta = QMessageBox.question(
            self,
            "Guardar comparación",
            "¿Quieres crear una nueva base de datos?\n\n"
            "Sí → Crear una nueva base de datos\n"
            "No → Utilizar una base de datos existente",
            buttons=(
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
                | QMessageBox.StandardButton.Cancel
            ),
            defaultButton=QMessageBox.StandardButton.Yes,
        )

        if respuesta == QMessageBox.StandardButton.Cancel:
            return

        # =========================================================
        # CREAR NUEVA SQLITE
        # =========================================================

        if respuesta == QMessageBox.StandardButton.Yes:

            nombre_bd = obtener_nombre_bd(
                archivo_anterior,
                archivo_nuevo,
            )

            ruta, _ = QFileDialog.getSaveFileName(
                self,
                "Crear base de datos SQLite",
                nombre_bd,
                "Base de datos SQLite (*.sqlite *.db)",
            )

            if not ruta:
                return

        # =========================================================
        # UTILIZAR SQLITE EXISTENTE
        # =========================================================

        else:

            ruta, _ = QFileDialog.getOpenFileName(
                self,
                "Seleccionar base de datos SQLite",
                "",
                "Base de datos SQLite (*.sqlite *.db)",
            )

            if not ruta:
                return

        # =========================================================
        # PROPONER IDENTIFICADOR
        # =========================================================

        identificador_propuesto = obtener_identificador_propuesto(
            archivo_anterior,
            archivo_nuevo,
        )

        identificador, aceptado = QInputDialog.getText(
            self,
            "Identificador de comparación",
            "Introduce el identificador de esta comparación:",
            text=identificador_propuesto,
        )

        if not aceptado:
            return

        identificador = identificador.strip()

        if not identificador:

            QMessageBox.warning(
                self,
                "Identificador vacío",
                "Debes introducir un identificador.",
            )

            return

        # =========================================================
        # OBTENER CONFIGURACIÓN ACTUAL
        # =========================================================

        columnas_clave = [
            item.text()
            for item in self.ui.listaColumnasClave.selectedItems()
        ]

        columnas_comparar = [
            item.text()
            for item in self.ui.listaColumnasComparar.selectedItems()
        ]

        hoja_anterior = self.ui.comboBoxHoja1.currentText()
        hoja_nueva = self.ui.comboBoxHoja2.currentText()

        # =========================================================
        # GUARDAR
        # =========================================================

        try:

            repositorio = RepositorioSQLite(ruta)

            comparacion_id = repositorio.guardar_comparacion(
                identificador=identificador,
                archivo_anterior=archivo_anterior,
                archivo_nuevo=archivo_nuevo,
                hoja_anterior=hoja_anterior,
                hoja_nueva=hoja_nueva,
                columnas_clave=columnas_clave,
                columnas_comparadas=columnas_comparar,
                cambios=self.modelo_cambios.cambios,
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error al guardar",
                "No se ha podido guardar la comparación:\n\n"
                f"{error}",
            )

            return

        # =========================================================
        # CONFIRMACIÓN
        # =========================================================

        QMessageBox.information(
            self,
            "Comparación guardada",
            "La comparación se ha guardado correctamente.\n\n"
            f"Identificador: {identificador}\n"
            f"Cambios guardados: "
            f"{len(self.modelo_cambios.cambios)}\n\n"
            f"Base de datos:\n{ruta}",
        )

        self.ui.statusBar.showMessage(
            f"Comparación guardada: {identificador}"
        )

    def _actualizar_identificadores_historico(self, cambios):
        combo = self.ui.comboBoxIdentificadorHistorico

        combo.blockSignals(True)

        combo.clear()
        combo.addItem("Todos")

        identificadores = sorted(
            {
                str(cambio["identificador"])
                for cambio in cambios
                if cambio["identificador"] is not None
            }
        )

        combo.addItems(identificadores)

        combo.blockSignals(False)

    def _obtener_modelo_visible_historico(self):
        """
        Obtiene el modelo que está utilizando actualmente
        la tabla del histórico.

        Si QFilterableTableView utiliza un modelo proxy
        para filtrar/ordenar, devuelve dicho modelo.
        """

        modelo = self.ui.tableViewHistorico.model()

        if modelo is None:
            return None

        return modelo

    def abrir_historico(self):

        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar base de datos SQLite",
            "",
            "Base de datos SQLite (*.sqlite *.db)",
        )

        if not ruta:
            return

        try:

            from src.database.repositorio import (
                RepositorioSQLite,
            )

            repositorio = RepositorioSQLite(ruta)

            cambios = (
                repositorio.obtener_historico_cambios()
            )

            self.ruta_historico = ruta
            self.repositorio_historico = repositorio

            self._actualizar_identificadores_historico(
                cambios
            )
                        
            self.modelo_historico.actualizar(
                cambios
            )

            self.limpiar_detalle_historico()

            self.ui.lineEditBaseHistorico.setText(
                ruta
            )

            self.ui.tableViewHistorico.resizeColumnsToContents()

            self.ui.statusBar.showMessage(
                "Histórico cargado correctamente."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"No se ha podido abrir la base de datos:\n\n{error}",
            )

    def exportar_historico_excel(self):
        """
        Exporta a Excel exactamente los registros que se están
        mostrando actualmente en la tabla del histórico.

        Respeta:
        - filtros aplicados
        - orden de las filas
        - columnas visibles
        """

        tabla = self.ui.tableViewHistorico

        # =========================================================
        # OBTENER EL PROXY REAL DE FILTRADO
        # =========================================================

        modelo = tabla._filter_proxy

        if modelo is None:

            QMessageBox.warning(
                self,
                "Sin datos",
                "No hay datos para exportar.",
            )

            return

        # =========================================================
        # COMPROBAR FILAS
        # =========================================================

        numero_filas = modelo.rowCount()

        if numero_filas == 0:

            QMessageBox.warning(
                self,
                "Sin datos",
                "No hay registros visibles para exportar.",
            )

            return

        # =========================================================
        # ELEGIR ARCHIVO
        # =========================================================

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar histórico a Excel",
            "Historico.xlsx",
            "Archivos Excel (*.xlsx)",
        )

        if not ruta:
            return

        try:

            libro = Workbook()

            hoja = libro.active

            hoja.title = "Histórico"

            # =====================================================
            # COLUMNAS
            # =====================================================

            columnas = modelo.columnCount()

            columnas_exportar = []

            for columna in range(columnas):

                # Comprobar si la columna está visible
                if tabla.isColumnHidden(columna):
                    continue

                encabezado = modelo.headerData(
                    columna,
                    Qt.Orientation.Horizontal,
                    Qt.ItemDataRole.DisplayRole,
                )

                columnas_exportar.append(
                    (
                        columna,
                        encabezado,
                    )
                )

            # =====================================================
            # CABECERAS
            # =====================================================

            for numero_columna, (_, encabezado) in enumerate(
                columnas_exportar,
                start=1,
            ):

                celda = hoja.cell(
                    row=1,
                    column=numero_columna,
                    value=encabezado,
                )

                celda.font = Font(
                    bold=True
                )

            # =====================================================
            # FILAS FILTRADAS
            # =====================================================

            for fila in range(numero_filas):

                for numero_columna, (
                    columna,
                    _,
                ) in enumerate(
                    columnas_exportar,
                    start=1,
                ):

                    indice = modelo.index(
                        fila,
                        columna,
                    )

                    valor = modelo.data(
                        indice,
                        Qt.ItemDataRole.DisplayRole,
                    )

                    hoja.cell(
                        row=fila + 2,
                        column=numero_columna,
                        value=valor,
                    )

            # =====================================================
            # FORMATO
            # =====================================================

            hoja.freeze_panes = "A2"

            hoja.auto_filter.ref = hoja.dimensions

            # Ajustar ancho de columnas
            for columna in hoja.columns:

                longitud = 0

                for celda in columna:

                    if celda.value is not None:

                        longitud = max(
                            longitud,
                            len(str(celda.value)),
                        )

                hoja.column_dimensions[
                    columna[0].column_letter
                ].width = min(
                    longitud + 2,
                    50,
                )

            # =====================================================
            # GUARDAR
            # =====================================================

            libro.save(ruta)

            # =====================================================
            # CONFIRMACIÓN
            # =====================================================

            QMessageBox.information(
                self,
                "Exportación completada",
                (
                    "El histórico se ha exportado correctamente.\n\n"
                    f"Registros exportados: {numero_filas}\n"
                    f"Archivo:\n{ruta}"
                ),
            )

            self.ui.statusBar.showMessage(
                f"Histórico exportado: "
                f"{numero_filas} registros."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error al exportar",
                (
                    "No se ha podido exportar el histórico:\n\n"
                    f"{error}"
                ),
            )
        
    def filtrar_historico(self):

        if self.repositorio_historico is None:
            return

        texto_clave = (
            self.ui.lineEditBuscarClaveHistorico
            .text()
            .strip()
            .lower()
        )

        identificador_seleccionado = (
            self.ui.comboBoxIdentificadorHistorico
            .currentText()
            .strip()
        )

        cambios = (
            self.repositorio_historico
            .obtener_historico_cambios()
        )

        cambios_filtrados = []

        for cambio in cambios:

            clave = str(
                cambio["clave"]
            ).lower()

            identificador = str(
                cambio["identificador"]
            )

            coincide_clave = (
                not texto_clave
                or texto_clave in clave
            )

            if identificador_seleccionado == "Todos":
                coincide_identificador = True
            else:
                coincide_identificador = (
                    identificador
                    == identificador_seleccionado
                )

            if (
                coincide_clave
                and coincide_identificador
            ):
                cambios_filtrados.append(cambio)

        self.modelo_historico.actualizar(
            cambios_filtrados
        )

        self.limpiar_detalle_historico()

    def eliminar_comparacion_historico(self):

        index = (
            self.ui.tableViewHistorico
            .currentIndex()
        )

        if not index.isValid():

            QMessageBox.warning(
                self,
                "Sin selección",
                "Selecciona una comparación.",
            )

            return

        cambio = (
            self.modelo_historico
            .obtener_cambio(index.row())
        )

        if cambio is None:
            return

        comparacion_id = cambio["comparacion_id"]

        identificador = cambio["identificador"]
        if comparacion_id is None:

            QMessageBox.critical(
                self,
                "Error",
                "No se ha podido identificar la comparación.",
            )

            return

        respuesta = QMessageBox.question(
            self,
            "Eliminar comparación",
            (
                "¿Deseas eliminar la comparación completa?\n\n"
                f"Identificador: {identificador}\n\n"
                "Se eliminarán todos los cambios asociados "
                "a esta comparación."
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if respuesta != QMessageBox.StandardButton.Yes:
            return

        try:

            self.repositorio_historico.eliminar_comparacion(
                comparacion_id
            )

            cambios = (
                self.repositorio_historico
                .obtener_historico_cambios()
            )

            self.modelo_historico.actualizar(
                cambios
            )

            self.limpiar_detalle_historico()

            self.ui.statusBar.showMessage(
                f"Comparación '{identificador}' eliminada."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                (
                    "No se ha podido eliminar la comparación:\n\n"
                    f"{error}"
                ),
            )

    def mostrar_detalle_historico(self, index):
        if not index.isValid():
            return

        fila = self._obtener_fila_modelo_origen(index)

        if fila < 0:
            return

        cambio = self.modelo_historico.obtener_cambio(fila)

        if cambio is None:
            return

        self._mostrar_valores_con_diferencias(
            cambio["valor_1"],
            cambio["valor_2"],
            self.ui.textEditValor1Historico,
            self.ui.textEditValor2Historico
        )

        self.ui.labelResumenHistorico.setText(
            cambio["fecha"]
        )

    def limpiar_detalle_historico(self):

        self.ui.labelResumenHistorico.setText(
            "Selecciona un cambio"
        )

        self.ui.textEditValor1Historico.clear()
        self.ui.textEditValor2Historico.clear()

