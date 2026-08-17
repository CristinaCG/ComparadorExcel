import pandas as pd


def crear_clave(
    df: pd.DataFrame,
    columnas: list[str],
) -> pd.Series:
    """
    Crea una clave única a partir de una o varias columnas.
    """

    if not columnas:
        raise ValueError(
            "Debe seleccionarse al menos una columna."
        )

    columnas_faltantes = [
        columna
        for columna in columnas
        if columna not in df.columns
    ]

    if columnas_faltantes:
        raise ValueError(
            f"Columnas no encontradas: {columnas_faltantes}"
        )

    return (
        df[columnas]
        .fillna("")
        .astype(str)
        .agg("|".join, axis=1)
    )