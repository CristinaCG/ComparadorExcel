from pathlib import Path

import pandas as pd


EXTENSIONES_VALIDAS = {".xlsx", ".xls"}


def validar_archivo_excel(
    ruta: str,
) -> Path:
    """
    Valida que el archivo exista y tenga una extensión Excel válida.

    Returns
    -------
    Path
        Ruta validada del archivo.
    """

    archivo = Path(ruta)

    if not archivo.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {archivo}"
        )

    if archivo.suffix.lower() not in EXTENSIONES_VALIDAS:
        raise ValueError(
            f"Formato de archivo no soportado: {archivo.suffix}"
        )

    return archivo


def obtener_hojas(
    ruta: str,
) -> list[str]:
    """
    Devuelve los nombres de las hojas de un archivo Excel.
    """

    archivo = validar_archivo_excel(ruta)

    libro = pd.ExcelFile(archivo)

    return libro.sheet_names


def leer_excel(
    ruta: str,
    nombre_hoja: str | None = None,
) -> pd.DataFrame:
    """
    Lee una hoja de un archivo Excel.

    Si no se especifica nombre_hoja, se lee la primera hoja.

    Parameters
    ----------
    ruta:
        Ruta completa del archivo Excel.

    nombre_hoja:
        Nombre de la hoja que se quiere leer.
        Si es None, se lee la primera hoja.

    Returns
    -------
    pd.DataFrame
        Datos de la hoja.
    """

    archivo = validar_archivo_excel(ruta)

    if nombre_hoja is None:
        nombre_hoja = 0

    return pd.read_excel(
        archivo,
        sheet_name=nombre_hoja,
    )