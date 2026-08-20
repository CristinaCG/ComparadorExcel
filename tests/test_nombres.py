from src.excel.nombres import (
    obtener_partes_comunes,
    obtener_nombre_bd,
    obtener_partes_diferentes,
    obtener_identificador_propuesto
)


def test_obtener_partes_comunes():
    resultado = obtener_partes_comunes(
        "F110_Cable list main data_20260818.xlsx",
        "F110_Cable list main data_20260820.xlsx",
    )

    assert resultado == (
        "F110_Cable list main data"
    )


def test_obtener_nombre_bd():
    resultado = obtener_nombre_bd(
        "F110_Cable list main data_20260818.xlsx",
        "F110_Cable list main data_20260820.xlsx",
    )

    assert resultado == (
        "F110_Cable list main data.sqlite"
    )


def test_no_hay_parte_comun():
    resultado = obtener_partes_comunes(
        "F110_archivo.xlsx",
        "F112_otro.xlsx",
    )

    assert resultado == ""


def test_nombres_completamente_diferentes():
    resultado = obtener_partes_comunes(
        "archivo1.xlsx",
        "archivo2.xlsx",
    )

    assert resultado == ""


def test_archivos_sin_extension():
    resultado = obtener_partes_comunes(
        "F110_datos_20260818",
        "F110_datos_20260820",
    )

    assert resultado == "F110_datos"


def test_nombre_bd_sin_parte_comun():
    resultado = obtener_nombre_bd(
        "archivo1.xlsx",
        "archivo2.xlsx",
    )

    assert resultado == "comparacion.sqlite"


def test_nombres_con_mas_de_dos_partes_comunes():
    resultado = obtener_partes_comunes(
        "F110_Cable_List_Main_20260818.xlsx",
        "F110_Cable_List_Main_20260820.xlsx",
    )

    assert resultado == (
        "F110_Cable_List_Main"
    )


def test_obtener_partes_diferentes():
    resultado = obtener_partes_diferentes(
        "F110_Cable list main data_20260818.xlsx",
        "F110_Cable list main data_20260820.xlsx",
    )

    assert resultado == (
        "20260818",
        "20260820",
    )


def test_identificador_propuesto():
    resultado = obtener_identificador_propuesto(
        "F110_Cable list main data_20260818.xlsx",
        "F110_Cable list main data_20260820.xlsx",
    )

    assert resultado == (
        "20260818 → 20260820"
    )


def test_partes_diferentes_multiples_bloques():
    resultado = obtener_partes_diferentes(
        "F110_Cable_2026_07_18.xlsx",
        "F110_Cable_2026_08_20.xlsx",
    )

    assert resultado == (
        "07_18",
        "08_20",
    )


def test_identificador_sin_diferencias():
    resultado = obtener_identificador_propuesto(
        "F110_Cable.xlsx",
        "F110_Cable.xlsx",
    )

    assert resultado == "Comparación"