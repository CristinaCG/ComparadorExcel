from pathlib import Path


def obtener_partes_comunes(
    archivo_1: str,
    archivo_2: str,
) -> str:
    """
    Obtiene la parte común inicial de los nombres
    de dos archivos.

    La comparación se realiza por bloques separados
    mediante "_".
    """

    nombre_1 = Path(archivo_1).stem
    nombre_2 = Path(archivo_2).stem

    partes_1 = nombre_1.split("_")
    partes_2 = nombre_2.split("_")

    partes_comunes = []

    for parte_1, parte_2 in zip(
        partes_1,
        partes_2,
    ):

        if parte_1 != parte_2:
            break

        partes_comunes.append(parte_1)

    return "_".join(partes_comunes)


def obtener_partes_diferentes(
    archivo_1: str,
    archivo_2: str,
) -> tuple[str, str]:
    """
    Obtiene las partes diferentes de los nombres
    de dos archivos.

    Devuelve:

        (parte_archivo_1, parte_archivo_2)
    """

    nombre_1 = Path(archivo_1).stem
    nombre_2 = Path(archivo_2).stem

    partes_1 = nombre_1.split("_")
    partes_2 = nombre_2.split("_")

    indice = 0

    while (
        indice < len(partes_1)
        and indice < len(partes_2)
        and partes_1[indice] == partes_2[indice]
    ):
        indice += 1

    diferentes_1 = partes_1[indice:]
    diferentes_2 = partes_2[indice:]

    return (
        "_".join(diferentes_1),
        "_".join(diferentes_2),
    )


def obtener_nombre_bd(
    archivo_1: str,
    archivo_2: str,
) -> str:
    """
    Propone un nombre para la base de datos SQLite
    a partir de la parte común de los Excel.
    """

    parte_comun = obtener_partes_comunes(
        archivo_1,
        archivo_2,
    )

    if not parte_comun:
        return "comparacion.sqlite"

    return f"{parte_comun}.sqlite"


def obtener_identificador_propuesto(
    archivo_1: str,
    archivo_2: str,
) -> str:
    """
    Propone un identificador a partir de las partes
    diferentes de los nombres de los Excel.
    """

    diferente_1, diferente_2 = (
        obtener_partes_diferentes(
            archivo_1,
            archivo_2,
        )
    )

    if not diferente_1 and not diferente_2:
        return "Comparación"

    if diferente_1 and diferente_2:
        return f"{diferente_1} → {diferente_2}"

    if diferente_1:
        return diferente_1

    return diferente_2