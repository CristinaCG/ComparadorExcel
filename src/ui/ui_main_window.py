# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QTableView, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(807, 737)
        MainWindow.setMinimumSize(QSize(800, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_10 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_comparar = QWidget()
        self.tab_comparar.setObjectName(u"tab_comparar")
        self.verticalLayout_2 = QVBoxLayout(self.tab_comparar)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBoxArchivos = QGroupBox(self.tab_comparar)
        self.groupBoxArchivos.setObjectName(u"groupBoxArchivos")
        self.groupBoxArchivos.setMinimumSize(QSize(0, 0))
        self.gridLayout = QGridLayout(self.groupBoxArchivos)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelEditArchivo1 = QLabel(self.groupBoxArchivos)
        self.labelEditArchivo1.setObjectName(u"labelEditArchivo1")

        self.horizontalLayout_2.addWidget(self.labelEditArchivo1)

        self.lineEditArchivo1 = QLineEdit(self.groupBoxArchivos)
        self.lineEditArchivo1.setObjectName(u"lineEditArchivo1")

        self.horizontalLayout_2.addWidget(self.lineEditArchivo1)

        self.pushButtonArchivo1 = QPushButton(self.groupBoxArchivos)
        self.pushButtonArchivo1.setObjectName(u"pushButtonArchivo1")

        self.horizontalLayout_2.addWidget(self.pushButtonArchivo1)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelHoja1 = QLabel(self.groupBoxArchivos)
        self.labelHoja1.setObjectName(u"labelHoja1")

        self.horizontalLayout_4.addWidget(self.labelHoja1)

        self.comboBoxHoja1 = QComboBox(self.groupBoxArchivos)
        self.comboBoxHoja1.setObjectName(u"comboBoxHoja1")

        self.horizontalLayout_4.addWidget(self.comboBoxHoja1)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelEditArchivo2 = QLabel(self.groupBoxArchivos)
        self.labelEditArchivo2.setObjectName(u"labelEditArchivo2")

        self.horizontalLayout.addWidget(self.labelEditArchivo2)

        self.lineEditArchivo2 = QLineEdit(self.groupBoxArchivos)
        self.lineEditArchivo2.setObjectName(u"lineEditArchivo2")

        self.horizontalLayout.addWidget(self.lineEditArchivo2)

        self.pushButtonArchivo2 = QPushButton(self.groupBoxArchivos)
        self.pushButtonArchivo2.setObjectName(u"pushButtonArchivo2")

        self.horizontalLayout.addWidget(self.pushButtonArchivo2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelHoja2 = QLabel(self.groupBoxArchivos)
        self.labelHoja2.setObjectName(u"labelHoja2")

        self.horizontalLayout_5.addWidget(self.labelHoja2)

        self.comboBoxHoja2 = QComboBox(self.groupBoxArchivos)
        self.comboBoxHoja2.setObjectName(u"comboBoxHoja2")

        self.horizontalLayout_5.addWidget(self.comboBoxHoja2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBoxArchivos)

        self.groupBoxConfiguracion = QGroupBox(self.tab_comparar)
        self.groupBoxConfiguracion.setObjectName(u"groupBoxConfiguracion")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBoxConfiguracion)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.groupBoxClave = QGroupBox(self.groupBoxConfiguracion)
        self.groupBoxClave.setObjectName(u"groupBoxClave")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBoxClave)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lineEditBuscarClave = QLineEdit(self.groupBoxClave)
        self.lineEditBuscarClave.setObjectName(u"lineEditBuscarClave")

        self.verticalLayout_5.addWidget(self.lineEditBuscarClave)

        self.listaColumnasClave = QListWidget(self.groupBoxClave)
        self.listaColumnasClave.setObjectName(u"listaColumnasClave")
        self.listaColumnasClave.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        self.verticalLayout_5.addWidget(self.listaColumnasClave)


        self.horizontalLayout_7.addLayout(self.verticalLayout_5)


        self.horizontalLayout_6.addWidget(self.groupBoxClave)

        self.groupBoxColumnasComparar = QGroupBox(self.groupBoxConfiguracion)
        self.groupBoxColumnasComparar.setObjectName(u"groupBoxColumnasComparar")
        self.horizontalLayout_8 = QHBoxLayout(self.groupBoxColumnasComparar)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.lineEditBuscarComparar = QLineEdit(self.groupBoxColumnasComparar)
        self.lineEditBuscarComparar.setObjectName(u"lineEditBuscarComparar")

        self.verticalLayout_6.addWidget(self.lineEditBuscarComparar)

        self.listaColumnasComparar = QListWidget(self.groupBoxColumnasComparar)
        self.listaColumnasComparar.setObjectName(u"listaColumnasComparar")
        self.listaColumnasComparar.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        self.verticalLayout_6.addWidget(self.listaColumnasComparar)


        self.horizontalLayout_8.addLayout(self.verticalLayout_6)


        self.horizontalLayout_6.addWidget(self.groupBoxColumnasComparar)


        self.verticalLayout_2.addWidget(self.groupBoxConfiguracion)

        self.pushButtonComparar = QPushButton(self.tab_comparar)
        self.pushButtonComparar.setObjectName(u"pushButtonComparar")

        self.verticalLayout_2.addWidget(self.pushButtonComparar)

        self.tabWidget.addTab(self.tab_comparar, "")
        self.tab_resultados = QWidget()
        self.tab_resultados.setObjectName(u"tab_resultados")
        self.verticalLayout_3 = QVBoxLayout(self.tab_resultados)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonGuardarComparacion = QPushButton(self.tab_resultados)
        self.pushButtonGuardarComparacion.setObjectName(u"pushButtonGuardarComparacion")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonGuardarComparacion.sizePolicy().hasHeightForWidth())
        self.pushButtonGuardarComparacion.setSizePolicy(sizePolicy)
        self.pushButtonGuardarComparacion.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_3.addWidget(self.pushButtonGuardarComparacion)

        self.labelResumen = QLabel(self.tab_resultados)
        self.labelResumen.setObjectName(u"labelResumen")
        self.labelResumen.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelResumen)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.tableViewCambios = QTableView(self.tab_resultados)
        self.tableViewCambios.setObjectName(u"tableViewCambios")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableViewCambios.sizePolicy().hasHeightForWidth())
        self.tableViewCambios.setSizePolicy(sizePolicy1)
        self.tableViewCambios.setMinimumSize(QSize(0, 100))
        self.tableViewCambios.horizontalHeader().setStretchLastSection(True)
        self.tableViewCambios.verticalHeader().setStretchLastSection(True)

        self.verticalLayout_4.addWidget(self.tableViewCambios)


        self.verticalLayout_7.addLayout(self.verticalLayout_4)

        self.groupBoxDetalle = QGroupBox(self.tab_resultados)
        self.groupBoxDetalle.setObjectName(u"groupBoxDetalle")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBoxDetalle.sizePolicy().hasHeightForWidth())
        self.groupBoxDetalle.setSizePolicy(sizePolicy2)
        self.groupBoxDetalle.setMinimumSize(QSize(0, 100))
        self.horizontalLayout_9 = QHBoxLayout(self.groupBoxDetalle)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout_Valor1 = QVBoxLayout()
        self.verticalLayout_Valor1.setObjectName(u"verticalLayout_Valor1")
        self.labelValor1 = QLabel(self.groupBoxDetalle)
        self.labelValor1.setObjectName(u"labelValor1")

        self.verticalLayout_Valor1.addWidget(self.labelValor1)

        self.textEditValor1 = QTextEdit(self.groupBoxDetalle)
        self.textEditValor1.setObjectName(u"textEditValor1")
        self.textEditValor1.setMinimumSize(QSize(0, 100))
        self.textEditValor1.setReadOnly(True)

        self.verticalLayout_Valor1.addWidget(self.textEditValor1)


        self.horizontalLayout_9.addLayout(self.verticalLayout_Valor1)

        self.verticalLayout_Valor2 = QVBoxLayout()
        self.verticalLayout_Valor2.setObjectName(u"verticalLayout_Valor2")
        self.labelValor2 = QLabel(self.groupBoxDetalle)
        self.labelValor2.setObjectName(u"labelValor2")

        self.verticalLayout_Valor2.addWidget(self.labelValor2)

        self.textEditValor2 = QTextEdit(self.groupBoxDetalle)
        self.textEditValor2.setObjectName(u"textEditValor2")
        self.textEditValor2.setMinimumSize(QSize(0, 100))
        self.textEditValor2.setReadOnly(True)

        self.verticalLayout_Valor2.addWidget(self.textEditValor2)


        self.horizontalLayout_9.addLayout(self.verticalLayout_Valor2)

        self.horizontalLayout_9.setStretch(0, 2)
        self.horizontalLayout_9.setStretch(1, 2)

        self.verticalLayout_7.addWidget(self.groupBoxDetalle)


        self.verticalLayout_3.addLayout(self.verticalLayout_7)

        self.tabWidget.addTab(self.tab_resultados, "")
        self.tab_historico = QWidget()
        self.tab_historico.setObjectName(u"tab_historico")
        self.verticalLayout_8 = QVBoxLayout(self.tab_historico)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.labelBaseHistorico = QLabel(self.tab_historico)
        self.labelBaseHistorico.setObjectName(u"labelBaseHistorico")

        self.horizontalLayout_11.addWidget(self.labelBaseHistorico)

        self.lineEditBaseHistorico = QLineEdit(self.tab_historico)
        self.lineEditBaseHistorico.setObjectName(u"lineEditBaseHistorico")

        self.horizontalLayout_11.addWidget(self.lineEditBaseHistorico)

        self.pushButtonAbrirHistorico = QPushButton(self.tab_historico)
        self.pushButtonAbrirHistorico.setObjectName(u"pushButtonAbrirHistorico")

        self.horizontalLayout_11.addWidget(self.pushButtonAbrirHistorico)


        self.verticalLayout_8.addLayout(self.horizontalLayout_11)

        self.horizontalLayoutIdentificador = QHBoxLayout()
        self.horizontalLayoutIdentificador.setObjectName(u"horizontalLayoutIdentificador")
        self.labelBuscarClaveHistorico = QLabel(self.tab_historico)
        self.labelBuscarClaveHistorico.setObjectName(u"labelBuscarClaveHistorico")

        self.horizontalLayoutIdentificador.addWidget(self.labelBuscarClaveHistorico)

        self.lineEditBuscarClaveHistorico = QLineEdit(self.tab_historico)
        self.lineEditBuscarClaveHistorico.setObjectName(u"lineEditBuscarClaveHistorico")

        self.horizontalLayoutIdentificador.addWidget(self.lineEditBuscarClaveHistorico)

        self.labelBuscarIdentificadorHistorico = QLabel(self.tab_historico)
        self.labelBuscarIdentificadorHistorico.setObjectName(u"labelBuscarIdentificadorHistorico")

        self.horizontalLayoutIdentificador.addWidget(self.labelBuscarIdentificadorHistorico)

        self.comboBoxIdentificadorHistorico = QComboBox(self.tab_historico)
        self.comboBoxIdentificadorHistorico.setObjectName(u"comboBoxIdentificadorHistorico")

        self.horizontalLayoutIdentificador.addWidget(self.comboBoxIdentificadorHistorico)

        self.pushButtonEliminarComparacion = QPushButton(self.tab_historico)
        self.pushButtonEliminarComparacion.setObjectName(u"pushButtonEliminarComparacion")

        self.horizontalLayoutIdentificador.addWidget(self.pushButtonEliminarComparacion)

        self.horizontalLayoutIdentificador.setStretch(0, 1)
        self.horizontalLayoutIdentificador.setStretch(1, 2)
        self.horizontalLayoutIdentificador.setStretch(2, 1)
        self.horizontalLayoutIdentificador.setStretch(3, 2)
        self.horizontalLayoutIdentificador.setStretch(4, 2)

        self.verticalLayout_8.addLayout(self.horizontalLayoutIdentificador)

        self.tableViewHistorico = QTableView(self.tab_historico)
        self.tableViewHistorico.setObjectName(u"tableViewHistorico")

        self.verticalLayout_8.addWidget(self.tableViewHistorico)

        self.groupBoxDetalleHistorico = QGroupBox(self.tab_historico)
        self.groupBoxDetalleHistorico.setObjectName(u"groupBoxDetalleHistorico")
        sizePolicy2.setHeightForWidth(self.groupBoxDetalleHistorico.sizePolicy().hasHeightForWidth())
        self.groupBoxDetalleHistorico.setSizePolicy(sizePolicy2)
        self.groupBoxDetalleHistorico.setMinimumSize(QSize(0, 100))
        self.horizontalLayout_14 = QHBoxLayout(self.groupBoxDetalleHistorico)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.labelResumenHistorico = QLabel(self.groupBoxDetalleHistorico)
        self.labelResumenHistorico.setObjectName(u"labelResumenHistorico")
        self.labelResumenHistorico.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_11.addWidget(self.labelResumenHistorico)

        self.horizontalLayout_DetalleHistorico = QHBoxLayout()
        self.horizontalLayout_DetalleHistorico.setObjectName(u"horizontalLayout_DetalleHistorico")
        self.verticalLayout_Valor1Historico = QVBoxLayout()
        self.verticalLayout_Valor1Historico.setObjectName(u"verticalLayout_Valor1Historico")
        self.labelValor1Historico = QLabel(self.groupBoxDetalleHistorico)
        self.labelValor1Historico.setObjectName(u"labelValor1Historico")

        self.verticalLayout_Valor1Historico.addWidget(self.labelValor1Historico)

        self.textEditValor1Historico = QTextEdit(self.groupBoxDetalleHistorico)
        self.textEditValor1Historico.setObjectName(u"textEditValor1Historico")
        self.textEditValor1Historico.setMinimumSize(QSize(0, 100))
        self.textEditValor1Historico.setReadOnly(True)

        self.verticalLayout_Valor1Historico.addWidget(self.textEditValor1Historico)


        self.horizontalLayout_DetalleHistorico.addLayout(self.verticalLayout_Valor1Historico)

        self.verticalLayout_Valor2Historico = QVBoxLayout()
        self.verticalLayout_Valor2Historico.setObjectName(u"verticalLayout_Valor2Historico")
        self.labelValor2Historico = QLabel(self.groupBoxDetalleHistorico)
        self.labelValor2Historico.setObjectName(u"labelValor2Historico")

        self.verticalLayout_Valor2Historico.addWidget(self.labelValor2Historico)

        self.textEditValor2Historico = QTextEdit(self.groupBoxDetalleHistorico)
        self.textEditValor2Historico.setObjectName(u"textEditValor2Historico")
        self.textEditValor2Historico.setMinimumSize(QSize(0, 100))
        self.textEditValor2Historico.setReadOnly(True)

        self.verticalLayout_Valor2Historico.addWidget(self.textEditValor2Historico)


        self.horizontalLayout_DetalleHistorico.addLayout(self.verticalLayout_Valor2Historico)

        self.horizontalLayout_DetalleHistorico.setStretch(0, 1)
        self.horizontalLayout_DetalleHistorico.setStretch(1, 1)

        self.verticalLayout_11.addLayout(self.horizontalLayout_DetalleHistorico)


        self.horizontalLayout_14.addLayout(self.verticalLayout_11)


        self.verticalLayout_8.addWidget(self.groupBoxDetalleHistorico)

        self.tabWidget.addTab(self.tab_historico, "")

        self.horizontalLayout_10.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Comparador de Excel", None))
        self.groupBoxArchivos.setTitle(QCoreApplication.translate("MainWindow", u"Archivos", None))
        self.labelEditArchivo1.setText(QCoreApplication.translate("MainWindow", u"Excel 1:", None))
        self.pushButtonArchivo1.setText(QCoreApplication.translate("MainWindow", u"Seleccionar", None))
        self.labelHoja1.setText(QCoreApplication.translate("MainWindow", u"Hoja:", None))
        self.labelEditArchivo2.setText(QCoreApplication.translate("MainWindow", u"Excel 2:", None))
        self.pushButtonArchivo2.setText(QCoreApplication.translate("MainWindow", u"Seleccionar", None))
        self.labelHoja2.setText(QCoreApplication.translate("MainWindow", u"Hoja:", None))
        self.groupBoxConfiguracion.setTitle(QCoreApplication.translate("MainWindow", u"Configuraci\u00f3n de comparaci\u00f3n", None))
        self.groupBoxClave.setTitle(QCoreApplication.translate("MainWindow", u"Columnas clave", None))
        self.lineEditBuscarClave.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Buscar columna...", None))
        self.groupBoxColumnasComparar.setTitle(QCoreApplication.translate("MainWindow", u"Columnas a comparar", None))
        self.lineEditBuscarComparar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Buscar columna...", None))
        self.pushButtonComparar.setText(QCoreApplication.translate("MainWindow", u"Comparar archivos", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_comparar), QCoreApplication.translate("MainWindow", u"Comparar", None))
        self.pushButtonGuardarComparacion.setText(QCoreApplication.translate("MainWindow", u"Guardar comparaci\u00f3n", None))
        self.labelResumen.setText(QCoreApplication.translate("MainWindow", u"0 cambios encontrados", None))
        self.groupBoxDetalle.setTitle(QCoreApplication.translate("MainWindow", u"Detalle del cambio", None))
        self.labelValor1.setText(QCoreApplication.translate("MainWindow", u"Valor 1", None))
        self.labelValor2.setText(QCoreApplication.translate("MainWindow", u"Valor 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_resultados), QCoreApplication.translate("MainWindow", u"Resultados", None))
        self.labelBaseHistorico.setText(QCoreApplication.translate("MainWindow", u"Base de datos:", None))
        self.pushButtonAbrirHistorico.setText(QCoreApplication.translate("MainWindow", u"Abrir", None))
        self.labelBuscarClaveHistorico.setText(QCoreApplication.translate("MainWindow", u"Buscar clave:", None))
        self.labelBuscarIdentificadorHistorico.setText(QCoreApplication.translate("MainWindow", u"Identificador:", None))
        self.pushButtonEliminarComparacion.setText(QCoreApplication.translate("MainWindow", u"Eliminar comparaci\u00f3n", None))
        self.groupBoxDetalleHistorico.setTitle(QCoreApplication.translate("MainWindow", u"Detalle del cambio", None))
        self.labelResumenHistorico.setText("")
        self.labelValor1Historico.setText(QCoreApplication.translate("MainWindow", u"Valor 1", None))
        self.labelValor2Historico.setText(QCoreApplication.translate("MainWindow", u"Valor 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_historico), QCoreApplication.translate("MainWindow", u"Hist\u00f3rico", None))
    # retranslateUi

