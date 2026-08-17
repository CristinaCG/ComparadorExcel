import pandas as pd
import pytest

from src.excel.comparador import (
    ClaveDuplicadaError,
    comparar_dataframes,
)


def test_comparar_registros():

    anterior = pd.DataFrame({
        "Codigo": ["A001", "A002", "A003"],
        "Descripcion": [
            "Cable A",
            "Cable B",
            "Cable C",
        ],
        "Peso": [10, 20, 30],
    })

    nuevo = pd.DataFrame({
        "Codigo": ["A001", "A002", "A004"],
        "Descripcion": [
            "Cable A",
            "Cable B",
            "Cable D",
        ],
        "Peso": [12, 20, 40],
    })

    cambios = comparar_dataframes(
        anterior,
        nuevo,
        columnas_clave=["Codigo"],
        columnas_comparar=[
            "Descripcion",
            "Peso",
        ],
    )

    assert len(cambios) == 5

    # ---------------------------------------------------------
    # A004 -> NUEVO
    # ---------------------------------------------------------

    cambios_a004 = [
        cambio
        for cambio in cambios
        if cambio.clave == "A004"
    ]

    assert len(cambios_a004) == 2

    assert all(
        cambio.tipo == "NUEVO"
        for cambio in cambios_a004
    )

    # ---------------------------------------------------------
    # A003 -> ELIMINADO
    # ---------------------------------------------------------

    cambios_a003 = [
        cambio
        for cambio in cambios
        if cambio.clave == "A003"
    ]

    assert len(cambios_a003) == 2

    assert all(
        cambio.tipo == "ELIMINADO"
        for cambio in cambios_a003
    )

    # ---------------------------------------------------------
    # A001 -> MODIFICADO
    # ---------------------------------------------------------

    cambios_a001 = [
        cambio
        for cambio in cambios
        if cambio.clave == "A001"
    ]

    assert len(cambios_a001) == 1

    cambio = cambios_a001[0]

    assert cambio.tipo == "MODIFICADO"
    assert cambio.columna == "Peso"
    assert cambio.valor_anterior == 10
    assert cambio.valor_nuevo == 12

    # ---------------------------------------------------------
    # A002 -> SIN CAMBIOS
    # ---------------------------------------------------------

    cambios_a002 = [
        cambio
        for cambio in cambios
        if cambio.clave == "A002"
    ]

    assert len(cambios_a002) == 0


def test_detectar_clave_duplicada():

    anterior = pd.DataFrame({
        "Codigo": [
            "A001",
            "A001",
        ],
        "Descripcion": [
            "Cable A",
            "Cable A duplicado",
        ],
    })

    nuevo = pd.DataFrame({
        "Codigo": ["A001"],
        "Descripcion": ["Cable A"],
    })

    with pytest.raises(ClaveDuplicadaError):

        comparar_dataframes(
            anterior,
            nuevo,
            columnas_clave=["Codigo"],
            columnas_comparar=["Descripcion"],
        )