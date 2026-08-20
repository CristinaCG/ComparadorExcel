from pathlib import Path

from src.database.repositorio_configuracion import (
    RepositorioConfiguracion,
)


def test_guardar_y_obtener_configuracion(tmp_path):
    ruta = tmp_path / "configuracion.sqlite"

    repositorio = RepositorioConfiguracion(ruta)

    repositorio.guardar_configuracion(
        firma="firma123",
        hoja_anterior="Hoja1",
        hoja_nueva="Hoja1",
        columnas_clave=["ID"],
        columnas_comparadas=[
            "Nombre",
            "Estado",
        ],
    )

    configuracion = repositorio.obtener_configuracion(
        "firma123"
    )

    assert configuracion is not None

    assert configuracion["firma"] == "firma123"
    assert configuracion["hoja_anterior"] == "Hoja1"
    assert configuracion["hoja_nueva"] == "Hoja1"

    assert configuracion["columnas_clave"] == [
        "ID"
    ]

    assert configuracion["columnas_comparadas"] == [
        "Nombre",
        "Estado",
    ]

    assert configuracion["ultimo_uso"] is not None


def test_obtener_configuracion_inexistente(tmp_path):
    ruta = tmp_path / "configuracion.sqlite"

    repositorio = RepositorioConfiguracion(ruta)

    configuracion = repositorio.obtener_configuracion(
        "no_existe"
    )

    assert configuracion is None


def test_actualizar_configuracion_existente(tmp_path):
    ruta = tmp_path / "configuracion.sqlite"

    repositorio = RepositorioConfiguracion(ruta)

    repositorio.guardar_configuracion(
        firma="firma123",
        hoja_anterior="Hoja1",
        hoja_nueva="Hoja1",
        columnas_clave=["ID"],
        columnas_comparadas=["Nombre"],
    )

    repositorio.guardar_configuracion(
        firma="firma123",
        hoja_anterior="Datos",
        hoja_nueva="Datos",
        columnas_clave=["Codigo"],
        columnas_comparadas=[
            "Descripcion",
            "Estado",
        ],
    )

    configuracion = repositorio.obtener_configuracion(
        "firma123"
    )

    assert configuracion is not None

    assert configuracion["hoja_anterior"] == "Datos"
    assert configuracion["hoja_nueva"] == "Datos"

    assert configuracion["columnas_clave"] == [
        "Codigo"
    ]

    assert configuracion["columnas_comparadas"] == [
        "Descripcion",
        "Estado",
    ]


def test_se_pueden_guardar_varias_configuraciones(tmp_path):
    ruta = tmp_path / "configuracion.sqlite"

    repositorio = RepositorioConfiguracion(ruta)

    repositorio.guardar_configuracion(
        firma="firma1",
        hoja_anterior="Hoja1",
        hoja_nueva="Hoja1",
        columnas_clave=["ID"],
        columnas_comparadas=["Nombre"],
    )

    repositorio.guardar_configuracion(
        firma="firma2",
        hoja_anterior="Datos",
        hoja_nueva="Datos",
        columnas_clave=["Codigo"],
        columnas_comparadas=["Estado"],
    )

    configuracion_1 = (
        repositorio.obtener_configuracion("firma1")
    )

    configuracion_2 = (
        repositorio.obtener_configuracion("firma2")
    )

    assert configuracion_1 is not None
    assert configuracion_2 is not None

    assert configuracion_1["columnas_clave"] == ["ID"]
    assert configuracion_2["columnas_clave"] == ["Codigo"]


def test_inicializar_crea_la_base_de_datos(tmp_path):
    ruta = tmp_path / "configuracion.sqlite"

    repositorio = RepositorioConfiguracion(ruta)

    repositorio.inicializar()

    assert ruta.exists()