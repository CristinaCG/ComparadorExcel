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
    QMenuBar, QPushButton, QSizePolicy, QTabWidget,
    QTableView, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
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
        self.listaColumnasClave.setSelectionMode(QAbstractItemView.MultiSelection)

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
        self.listaColumnasComparar.setSelectionMode(QAbstractItemView.MultiSelection)

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
        self.verticalLayout_8 = QVBoxLayout(self.tab_resultados)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.labelResumen = QLabel(self.tab_resultados)
        self.labelResumen.setObjectName(u"labelResumen")

        self.verticalLayout_8.addWidget(self.labelResumen)

        self.tableViewCambios = QTableView(self.tab_resultados)
        self.tableViewCambios.setObjectName(u"tableViewCambios")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableViewCambios.sizePolicy().hasHeightForWidth())
        self.tableViewCambios.setSizePolicy(sizePolicy)
        self.tableViewCambios.setMinimumSize(QSize(0, 100))
        self.tableViewCambios.horizontalHeader().setStretchLastSection(True)
        self.tableViewCambios.verticalHeader().setStretchLastSection(True)

        self.verticalLayout_8.addWidget(self.tableViewCambios)

        self.groupBoxDetalle = QGroupBox(self.tab_resultados)
        self.groupBoxDetalle.setObjectName(u"groupBoxDetalle")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBoxDetalle.sizePolicy().hasHeightForWidth())
        self.groupBoxDetalle.setSizePolicy(sizePolicy1)
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
        self.textEditValor2.setReadOnly(True)

        self.verticalLayout_Valor2.addWidget(self.textEditValor2)


        self.horizontalLayout_9.addLayout(self.verticalLayout_Valor2)


        self.verticalLayout_8.addWidget(self.groupBoxDetalle)

        self.verticalLayout_8.setStretch(1, 3)
        self.verticalLayout_8.setStretch(2, 1)
        self.tabWidget.addTab(self.tab_resultados, "")
        self.tab_historico = QWidget()
        self.tab_historico.setObjectName(u"tab_historico")
        self.tabWidget.addTab(self.tab_historico, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


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
        self.labelResumen.setText(QCoreApplication.translate("MainWindow", u"0 cambios encontrados", None))
        self.groupBoxDetalle.setTitle(QCoreApplication.translate("MainWindow", u"Detalle del cambio", None))
        self.labelValor1.setText(QCoreApplication.translate("MainWindow", u"Valor 1", None))
        self.labelValor2.setText(QCoreApplication.translate("MainWindow", u"Valor 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_resultados), QCoreApplication.translate("MainWindow", u"Resultados", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_historico), QCoreApplication.translate("MainWindow", u"Hist\u00f3rico", None))
    # retranslateUi

