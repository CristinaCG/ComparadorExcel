from dataclasses import dataclass

import pandas as pd


@dataclass
class InformacionColumna:
    nombre: str
    tipo: str
    valores: int
    nulos: int
    unicos: int
    duplicados: int


@dataclass
class InformacionHoja:
    nombre: str
    filas: int
    columnas: list[InformacionColumna]


def analizar_columna(
    serie: pd.Series,
) -> InformacionColumna:
    """
    Analiza una columna de un DataFrame.
    """

    valores = serie.notna().sum()
    nulos = serie.isna().sum()
    unicos = serie.nunique(dropna=True)

    duplicados = valores - unicos

    return InformacionColumna(
        nombre=str(serie.name),
        tipo=str(serie.dtype),
        valores=int(valores),
        nulos=int(nulos),
        unicos=int(unicos),
        duplicados=int(duplicados),
    )


def analizar_hoja(
    df: pd.DataFrame,
    nombre: str,
) -> InformacionHoja:
    """
    Analiza una hoja completa de Excel.
    """

    columnas = [
        analizar_columna(df[columna])
        for columna in df.columns
    ]

    return InformacionHoja(
        nombre=nombre,
        filas=len(df),
        columnas=columnas,
    )


def analizar_excel(
    ruta: str,
) -> list[InformacionHoja]:
    """
    Analiza todas las hojas de un archivo Excel.
    """

    hojas = pd.read_excel(
        ruta,
        sheet_name=None,
    )

    return [
        analizar_hoja(df, nombre)
        for nombre, df in hojas.items()
    ]


def obtener_columnas_comunes(
    anterior: pd.DataFrame,
    nuevo: pd.DataFrame,
) -> list[str]:
    """
    Devuelve las columnas presentes en ambos DataFrames.
    """

    return [
        columna
        for columna in anterior.columns
        if columna in nuevo.columns
    ]


def obtener_columnas_nuevas(
    anterior: pd.DataFrame,
    nuevo: pd.DataFrame,
) -> list[str]:
    """
    Devuelve las columnas que existen en el nuevo
    pero no en el anterior.
    """

    return [
        columna
        for columna in nuevo.columns
        if columna not in anterior.columns
    ]


def obtener_columnas_eliminadas(
    anterior: pd.DataFrame,
    nuevo: pd.DataFrame,
) -> list[str]:
    """
    Devuelve las columnas que existían en el anterior
    pero ya no están en el nuevo.
    """

    return [
        columna
        for columna in anterior.columns
        if columna not in nuevo.columns
    ]