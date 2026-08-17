from pathlib import Path

import pandas as pd

from src.excel.comparador import Cambio, comparar_dataframes


def cargar_hoja(
    ruta: str,
    nombre_hoja: str,
) -> pd.DataFrame:
    """
    Carga una hoja concreta de un Excel.
    """

    archivo = Path(ruta)

    if not archivo.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {archivo}"
        )

    return pd.read_excel(
        archivo,
        sheet_name=nombre_hoja,
    )


def comparar_archivos(
    ruta_anterior: str,
    hoja_anterior: str,
    ruta_nuevo: str,
    hoja_nuevo: str,
    columnas_clave: list[str],
    columnas_comparar: list[str],
) -> list[Cambio]:
    """
    Compara dos hojas de Excel.
    """

    anterior = cargar_hoja(
        ruta_anterior,
        hoja_anterior,
    )

    nuevo = cargar_hoja(
        ruta_nuevo,
        hoja_nuevo,
    )

    return comparar_dataframes(
        anterior=anterior,
        nuevo=nuevo,
        columnas_clave=columnas_clave,
        columnas_comparar=columnas_comparar,
    )