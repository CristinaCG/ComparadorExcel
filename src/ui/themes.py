"""
Módulo de gestión de temas y hojas de estilo (QSS) para la aplicación.
"""

TEMA_PINE_CLARO = """
QMainWindow, QDialog {
    background-color: #F4F6F9;
    color: #1A2530;
}

QWidget {
    font-family: 'Segoe UI', 'SF Pro Display', Roboto, sans-serif;
    font-size: 13px;
    color: #2C3E50;
}

/* QTabWidget y QTabBar */
QTabWidget::pane {
    border: 1px solid #DCE3EC;
    border-radius: 8px;
    background-color: #FFFFFF;
    top: -1px;
}

QTabBar::tab {
    background-color: #EBF0F5;
    color: #5A6A75;
    padding: 8px 16px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
    font-weight: 600;
}

QTabBar::tab:selected {
    background-color: #106EBE;
    color: #FFFFFF;
}

QTabBar::tab:hover:!selected {
    background-color: #D9E3ED;
    color: #106EBE;
}

/* QGroupBox */
QGroupBox {
    font-weight: bold;
    border: 1px solid #D0D7DE;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    background-color: #FFFFFF;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    color: #0F4C81;
}

/* Push Buttons */
QPushButton {
    background-color: #106EBE;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 7px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #005A9E;
}

QPushButton:pressed {
    background-color: #004578;
}

QPushButton:disabled {
    background-color: #C8D1DA;
    color: #8A9BA8;
}

/* LineEdit, ComboBox, TextEdit */
QLineEdit, QComboBox, QTextEdit, QListWidget {
    background-color: #F8FAFC;
    border: 1px solid #C5D1DE;
    border-radius: 6px;
    padding: 5px 8px;
    color: #1A2530;
}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QListWidget:focus {
    border: 2px solid #106EBE;
    background-color: #FFFFFF;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

/* QTableView */
QTableView {
    background-color: #FFFFFF;
    alternate-background-color: #F4F7FA;
    gridline-color: #E2E8F0;
    border: 1px solid #DCE3EC;
    border-radius: 6px;
    selection-background-color: #D0E1F9;
    selection-color: #0F4C81;
}

QHeaderView::section {
    background-color: #E2E9F3;
    color: #0F4C81;
    font-weight: bold;
    padding: 6px;
    border: none;
    border-right: 1px solid #CBD5E1;
    border-bottom: 2px solid #106EBE;
}

/* QStatusBar */
QStatusBar {
    background-color: #E9ECEF;
    color: #334155;
    border-top: 1px solid #CBD5E1;
}
"""

TEMA_PINE_OSCURO = """
QMainWindow, QDialog {
    background-color: #0F172A;
    color: #F1F5F9;
}

QWidget {
    font-family: 'Segoe UI', 'SF Pro Display', Roboto, sans-serif;
    font-size: 13px;
    color: #E2E8F0;
}

/* QTabWidget y QTabBar */
QTabWidget::pane {
    border: 1px solid #1E293B;
    border-radius: 8px;
    background-color: #1E293B;
    top: -1px;
}

QTabBar::tab {
    background-color: #0F172A;
    color: #94A3B8;
    padding: 8px 16px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
    font-weight: 600;
}

QTabBar::tab:selected {
    background-color: #0284C7;
    color: #FFFFFF;
}

QTabBar::tab:hover:!selected {
    background-color: #1E293B;
    color: #38BDF8;
}

/* QGroupBox */
QGroupBox {
    font-weight: bold;
    border: 1px solid #334155;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    background-color: #1E293B;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    color: #38BDF8;
}

/* Push Buttons */
QPushButton {
    background-color: #0284C7;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 7px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #0369A1;
}

QPushButton:pressed {
    background-color: #075985;
}

QPushButton:disabled {
    background-color: #334155;
    color: #64748B;
}

/* LineEdit, ComboBox, TextEdit */
QLineEdit, QComboBox, QTextEdit, QListWidget {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5px 8px;
    color: #F8FAFC;
}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QListWidget:focus {
    border: 2px solid #38BDF8;
    background-color: #0F172A;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

/* QTableView */
QTableView {
    background-color: #0F172A;
    alternate-background-color: #1E293B;
    gridline-color: #334155;
    border: 1px solid #334155;
    border-radius: 6px;
    selection-background-color: #0369A1;
    selection-color: #F8FAFC;
}

QHeaderView::section {
    background-color: #1E293B;
    color: #38BDF8;
    font-weight: bold;
    padding: 6px;
    border: none;
    border-right: 1px solid #334155;
    border-bottom: 2px solid #0284C7;
}

/* QStatusBar */
QStatusBar {
    background-color: #0F172A;
    color: #94A3B8;
    border-top: 1px solid #1E293B;
}
"""

TEMA_JULES_MORADO = """
QMainWindow, QDialog {
    background-color: #130E26;
    color: #F3EFFE;
}

QWidget {
    font-family: 'Segoe UI', 'SF Pro Display', Roboto, sans-serif;
    font-size: 13px;
    color: #E2D9F3;
}

/* QTabWidget y QTabBar */
QTabWidget::pane {
    border: 1px solid #2A1E4A;
    border-radius: 8px;
    background-color: #1D153A;
    top: -1px;
}

QTabBar::tab {
    background-color: #130E26;
    color: #A792C9;
    padding: 8px 16px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
    font-weight: 600;
}

QTabBar::tab:selected {
    background-color: #8B5CF6;
    color: #FFFFFF;
}

QTabBar::tab:hover:!selected {
    background-color: #2A1E4A;
    color: #C4B5FD;
}

/* QGroupBox */
QGroupBox {
    font-weight: bold;
    border: 1px solid #3B2B63;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    background-color: #1D153A;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    color: #C4B5FD;
}

/* Push Buttons */
QPushButton {
    background-color: #8B5CF6;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 7px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #7C3AED;
}

QPushButton:pressed {
    background-color: #6D28D9;
}

QPushButton:disabled {
    background-color: #3B2B63;
    color: #6B5B93;
}

/* LineEdit, ComboBox, TextEdit */
QLineEdit, QComboBox, QTextEdit, QListWidget {
    background-color: #130E26;
    border: 1px solid #3B2B63;
    border-radius: 6px;
    padding: 5px 8px;
    color: #F3EFFE;
}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QListWidget:focus {
    border: 2px solid #A78BFA;
    background-color: #130E26;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

/* QTableView */
QTableView {
    background-color: #130E26;
    alternate-background-color: #1D153A;
    gridline-color: #3B2B63;
    border: 1px solid #3B2B63;
    border-radius: 6px;
    selection-background-color: #6D28D9;
    selection-color: #F3EFFE;
}

QHeaderView::section {
    background-color: #1D153A;
    color: #C4B5FD;
    font-weight: bold;
    padding: 6px;
    border: none;
    border-right: 1px solid #3B2B63;
    border-bottom: 2px solid #8B5CF6;
}

/* QStatusBar */
QStatusBar {
    background-color: #130E26;
    color: #A792C9;
    border-top: 1px solid #2A1E4A;
}
"""

TEMAS = {
    "Pine Azul (Claro)": TEMA_PINE_CLARO,
    "Pine Azul (Oscuro)": TEMA_PINE_OSCURO,
    "Jules Morado": TEMA_JULES_MORADO,
}
