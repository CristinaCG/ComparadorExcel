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

    hojas = pd.read_excel(
        ruta,
        sheet_name=None,
    )

    return [
        analizar_hoja(df, nombre)
        for nombre, df in hojas.items()
    ]