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
    
def test_comparar_con_clave_compuesta():

    anterior = pd.DataFrame({
        "Codigo": [
            "A001",
            "A001",
            "A002",
        ],
        "Posicion": [
            1,
            2,
            1,
        ],
        "Descripcion": [
            "Cable 1",
            "Cable 2",
            "Cable 3",
        ],
    })

    nuevo = pd.DataFrame({
        "Codigo": [
            "A001",
            "A001",
            "A002",
        ],
        "Posicion": [
            1,
            2,
            1,
        ],
        "Descripcion": [
            "Cable 1",
            "Cable 2 modificado",
            "Cable 3",
        ],
    })

    cambios = comparar_dataframes(
        anterior,
        nuevo,
        columnas_clave=[
            "Codigo",
            "Posicion",
        ],
        columnas_comparar=[
            "Descripcion",
        ],
    )

    assert len(cambios) == 1

    cambio = cambios[0]

    assert cambio.clave == "A001|2"
    assert cambio.tipo == "MODIFICADO"
    assert cambio.columna == "Descripcion"
    assert cambio.valor_anterior == "Cable 2"
    assert cambio.valor_nuevo == "Cable 2 modificado"

def test_valores_nulos_no_generan_cambio():

    anterior = pd.DataFrame({
        "Codigo": ["A001"],
        "Peso": [None],
    })

    nuevo = pd.DataFrame({
        "Codigo": ["A001"],
        "Peso": [None],
    })

    cambios = comparar_dataframes(
        anterior,
        nuevo,
        columnas_clave=["Codigo"],
        columnas_comparar=["Peso"],
    )

    assert len(cambios) == 0

def test_valor_nulo_a_valor():

    anterior = pd.DataFrame({
        "Codigo": ["A001"],
        "Peso": [None],
    })

    nuevo = pd.DataFrame({
        "Codigo": ["A001"],
        "Peso": [25],
    })

    cambios = comparar_dataframes(
        anterior,
        nuevo,
        columnas_clave=["Codigo"],
        columnas_comparar=["Peso"],
    )

    assert len(cambios) == 1

    cambio = cambios[0]

    assert cambio.tipo == "MODIFICADO"
    assert cambio.columna == "Peso"
    assert pd.isna(cambio.valor_anterior)
    assert cambio.valor_nuevo == 25

def test_numeros_equivalentes_no_generan_cambio():

    anterior = pd.DataFrame({
        "Codigo": ["A001"],
        "Peso": [10],
    })

    nuevo = pd.DataFrame({
        "Codigo": ["A001"],
        "Peso": [10.0],
    })

    cambios = comparar_dataframes(
        anterior,
        nuevo,
        columnas_clave=["Codigo"],
        columnas_comparar=["Peso"],
    )

    assert len(cambios) == 0

def test_texto_y_numero_son_diferentes():

    anterior = pd.DataFrame({
        "Codigo": ["A001"],
        "Valor": ["10"],
    })

    nuevo = pd.DataFrame({
        "Codigo": ["A001"],
        "Valor": [10],
    })

    cambios = comparar_dataframes(
        anterior,
        nuevo,
        columnas_clave=["Codigo"],
        columnas_comparar=["Valor"],
    )

    assert len(cambios) == 1