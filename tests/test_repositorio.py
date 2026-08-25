from pathlib import Path

from src.database.repositorio import RepositorioSQLite
from src.excel.comparador import Cambio


def test_guardar_y_recuperar_comparacion(tmp_path: Path):

    ruta = tmp_path / "comparaciones.sqlite"

    repositorio = RepositorioSQLite(ruta)

    cambios = [
        Cambio(
            clave="A001",
            tipo="MODIFICADO",
            columna="Peso",
            valor_1=10,
            valor_2=12,
        ),
        Cambio(
            clave="A002",
            tipo="NUEVO",
            columna=None,
            valor_1=None,
            valor_2=None,
        ),
    ]

    comparacion_id = repositorio.guardar_comparacion(
        identificador="20260724/20260813",
        archivo_anterior="anterior.xlsx",
        archivo_nuevo="nuevo.xlsx",
        hoja_anterior="Hoja1",
        hoja_nueva="Hoja1",
        columnas_clave=["Codigo"],
        columnas_comparadas=["Descripcion", "Peso"],
        cambios=cambios,
    )

    assert comparacion_id == 1

    comparacion = repositorio.obtener_comparacion(
        comparacion_id
    )

    assert comparacion is not None
    assert comparacion["identificador"] == "20260724/20260813"
    assert comparacion["archivo_anterior"] == "anterior.xlsx"
    assert comparacion["archivo_nuevo"] == "nuevo.xlsx"

    cambios_guardados = repositorio.obtener_cambios(
        comparacion_id
    )

    assert len(cambios_guardados) == 2

    assert cambios_guardados[0]["clave"] == "A001"
    assert cambios_guardados[0]["tipo"] == "MODIFICADO"
    assert cambios_guardados[0]["columna"] == "Peso"
    assert cambios_guardados[0]["valor_1"] == "10"
    assert cambios_guardados[0]["valor_2"] == "12"


def test_obtener_comparaciones(tmp_path: Path):

    ruta = tmp_path / "comparaciones.sqlite"

    repositorio = RepositorioSQLite(ruta)

    repositorio.guardar_comparacion(
        identificador="20260724/20260813",
        archivo_anterior="a.xlsx",
        archivo_nuevo="b.xlsx",
        hoja_anterior="Hoja1",
        hoja_nueva="Hoja1",
        columnas_clave=["Codigo"],
        columnas_comparadas=["Peso"],
        cambios=[],
    )

    repositorio.guardar_comparacion(
        identificador="20260813/20260819",
        archivo_anterior="b.xlsx",
        archivo_nuevo="c.xlsx",
        hoja_anterior="Hoja1",
        hoja_nueva="Hoja1",
        columnas_clave=["Codigo"],
        columnas_comparadas=["Peso"],
        cambios=[],
    )

    comparaciones = repositorio.obtener_comparaciones()

    assert len(comparaciones) == 2

    identificadores = [
        comparacion["identificador"]
        for comparacion in comparaciones
    ]

    assert "20260724/20260813" in identificadores
    assert "20260813/20260819" in identificadores


def test_eliminar_comparacion(tmp_path: Path):

    ruta = tmp_path / "comparaciones.sqlite"

    repositorio = RepositorioSQLite(ruta)

    comparacion_id = repositorio.guardar_comparacion(
        identificador="20260724/20260813",
        archivo_anterior="a.xlsx",
        archivo_nuevo="b.xlsx",
        hoja_anterior="Hoja1",
        hoja_nueva="Hoja1",
        columnas_clave=["Codigo"],
        columnas_comparadas=["Peso"],
        cambios=[
            Cambio(
                clave="A001",
                tipo="MODIFICADO",
                columna="Peso",
                valor_1=10,
                valor_2=12,
            )
        ],
    )

    repositorio.eliminar_comparacion(comparacion_id)

    assert repositorio.obtener_comparacion(
        comparacion_id
    ) is None

    assert repositorio.obtener_cambios(
        comparacion_id
    ) == []