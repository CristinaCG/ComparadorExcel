from pathlib import Path

import pandas as pd


EXTENSIONES_VALIDAS = {".xlsx", ".xls"}


def leer_excel(ruta: str) -> pd.DataFrame:
    """
    Lee un archivo Excel y devuelve su contenido como DataFrame.

    Parameters
    ----------
    ruta:
        Ruta completa del archivo Excel.

    Returns
    -------
    pd.DataFrame
        Datos del Excel.

    Raises
    ------
    FileNotFoundError
        Si el archivo no existe.
    ValueError
        Si la extensión no es compatible.
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

    return pd.read_excel(archivo)