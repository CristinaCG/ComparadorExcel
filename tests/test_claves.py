import pandas as pd
import pytest

from src.excel.claves import crear_clave


def test_crear_clave_simple():

    df = pd.DataFrame({
        "Codigo": ["A001", "A002", "A003"],
    })

    resultado = crear_clave(
        df,
        ["Codigo"],
    )

    assert resultado.tolist() == [
        "A001",
        "A002",
        "A003",
    ]


def test_crear_clave_compuesta():

    df = pd.DataFrame({
        "Codigo": ["A001", "A001", "A002"],
        "Posicion": [1, 2, 1],
    })

    resultado = crear_clave(
        df,
        ["Codigo", "Posicion"],
    )

    assert resultado.tolist() == [
        "A001|1",
        "A001|2",
        "A002|1",
    ]


def test_clave_sin_columnas():

    df = pd.DataFrame({
        "Codigo": ["A001"],
    })

    with pytest.raises(ValueError):
        crear_clave(df, [])


def test_columna_inexistente():

    df = pd.DataFrame({
        "Codigo": ["A001"],
    })

    with pytest.raises(ValueError):
        crear_clave(
            df,
            ["NoExiste"],
        )