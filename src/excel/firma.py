import hashlib


def generar_firma_excel(
    df_1,
    df_2,
) -> str:
    """
    Genera una firma que identifica la estructura común
    de los dos DataFrames.

    La firma no depende de los datos de las filas,
    sino de las columnas existentes en ambos Excel.
    """

    columnas_1 = sorted(
        str(columna)
        for columna in df_1.columns
    )

    columnas_2 = sorted(
        str(columna)
        for columna in df_2.columns
    )

    estructura = (
        "EXCEL1:"
        + "|".join(columnas_1)
        + "\n"
        + "EXCEL2:"
        + "|".join(columnas_2)
    )

    return hashlib.sha256(
        estructura.encode("utf-8")
    ).hexdigest()