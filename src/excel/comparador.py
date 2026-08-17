from dataclasses import dataclass

import pandas as pd

from src.excel.claves import crear_clave


class ClaveDuplicadaError(ValueError):
    """Se produce cuando la clave seleccionada no es única."""

    pass


class ColumnaNoEncontradaError(ValueError):
    """Se produce cuando una columna solicitada no existe."""

    pass


@dataclass
class Cambio:
    """
    Representa un cambio detectado entre dos versiones de un Excel.

    Attributes
    ----------
    clave:
        Identificador del registro.
    tipo:
        NUEVO, ELIMINADO o MODIFICADO.
    columna:
        Columna donde se produce el cambio.
    valor_anterior:
        Valor existente en el Excel anterior.
    valor_nuevo:
        Valor existente en el Excel nuevo.
    """

    clave: str
    tipo: str
    columna: str
    valor_anterior: object
    valor_nuevo: object


def comparar_dataframes(
    anterior: pd.DataFrame,
    nuevo: pd.DataFrame,
    columnas_clave: list[str],
    columnas_comparar: list[str],
) -> list[Cambio]:
    """
    Compara dos DataFrames utilizando una o varias columnas como clave.

    Parameters
    ----------
    anterior:
        DataFrame correspondiente a la versión anterior.

    nuevo:
        DataFrame correspondiente a la versión nueva.

    columnas_clave:
        Columnas que identifican un registro.

    columnas_comparar:
        Columnas cuyos valores se quieren comparar.

    Returns
    -------
    list[Cambio]
        Lista de cambios detectados.

    Raises
    ------
    ValueError
        Si no se especifica ninguna columna clave.

    ClaveDuplicadaError
        Si la combinación de columnas clave no es única.

    ColumnaNoEncontradaError
        Si alguna columna especificada no existe.
    """

    # ---------------------------------------------------------
    # VALIDACIÓN DE COLUMNAS
    # ---------------------------------------------------------

    if not columnas_clave:
        raise ValueError(
            "Debe seleccionarse al menos una columna clave."
        )

    columnas_faltantes_anterior = (
        _buscar_columnas_faltantes(
            anterior,
            columnas_clave,
        )
    )

    columnas_faltantes_nuevo = (
        _buscar_columnas_faltantes(
            nuevo,
            columnas_clave,
        )
    )

    if columnas_faltantes_anterior:
        raise ColumnaNoEncontradaError(
            "Columnas clave inexistentes en el Excel anterior: "
            f"{columnas_faltantes_anterior}"
        )

    if columnas_faltantes_nuevo:
        raise ColumnaNoEncontradaError(
            "Columnas clave inexistentes en el Excel nuevo: "
            f"{columnas_faltantes_nuevo}"
        )

    columnas_faltantes_comparar_anterior = (
        _buscar_columnas_faltantes(
            anterior,
            columnas_comparar,
        )
    )

    columnas_faltantes_comparar_nuevo = (
        _buscar_columnas_faltantes(
            nuevo,
            columnas_comparar,
        )
    )

    if columnas_faltantes_comparar_anterior:
        raise ColumnaNoEncontradaError(
            "Columnas a comparar inexistentes en el Excel anterior: "
            f"{columnas_faltantes_comparar_anterior}"
        )

    if columnas_faltantes_comparar_nuevo:
        raise ColumnaNoEncontradaError(
            "Columnas a comparar inexistentes en el Excel nuevo: "
            f"{columnas_faltantes_comparar_nuevo}"
        )

    # ---------------------------------------------------------
    # COPIAS
    # ---------------------------------------------------------

    anterior = anterior.copy()
    nuevo = nuevo.copy()

    # ---------------------------------------------------------
    # CREAR CLAVES
    # ---------------------------------------------------------

    clave_anterior = crear_clave(
        anterior,
        columnas_clave,
    )

    clave_nuevo = crear_clave(
        nuevo,
        columnas_clave,
    )

    # ---------------------------------------------------------
    # COMPROBAR CLAVES DUPLICADAS
    # ---------------------------------------------------------

    _validar_claves_unicas(
        clave_anterior,
        "Excel anterior",
    )

    _validar_claves_unicas(
        clave_nuevo,
        "Excel nuevo",
    )

    anterior["_clave_comparacion"] = clave_anterior
    nuevo["_clave_comparacion"] = clave_nuevo

    # ---------------------------------------------------------
    # OBTENER CONJUNTOS DE CLAVES
    # ---------------------------------------------------------

    claves_anterior = set(
        anterior["_clave_comparacion"]
    )

    claves_nuevo = set(
        nuevo["_clave_comparacion"]
    )

    claves_nuevas = claves_nuevo - claves_anterior
    claves_eliminadas = claves_anterior - claves_nuevo
    claves_comunes = claves_anterior & claves_nuevo

    cambios: list[Cambio] = []

    # ---------------------------------------------------------
    # REGISTROS NUEVOS
    # ---------------------------------------------------------

    nuevo_indexado = nuevo.set_index(
        "_clave_comparacion"
    )

    for clave in sorted(claves_nuevas):

        fila_nueva = nuevo_indexado.loc[clave]

        for columna in columnas_comparar:

            cambios.append(
                Cambio(
                    clave=clave,
                    tipo="NUEVO",
                    columna=columna,
                    valor_anterior=None,
                    valor_nuevo=fila_nueva[columna],
                )
            )

    # ---------------------------------------------------------
    # REGISTROS ELIMINADOS
    # ---------------------------------------------------------

    anterior_indexado = anterior.set_index(
        "_clave_comparacion"
    )

    for clave in sorted(claves_eliminadas):

        fila_anterior = anterior_indexado.loc[clave]

        for columna in columnas_comparar:

            cambios.append(
                Cambio(
                    clave=clave,
                    tipo="ELIMINADO",
                    columna=columna,
                    valor_anterior=fila_anterior[columna],
                    valor_nuevo=None,
                )
            )

    # ---------------------------------------------------------
    # REGISTROS EXISTENTES
    # ---------------------------------------------------------

    for clave in sorted(claves_comunes):

        fila_anterior = anterior_indexado.loc[clave]
        fila_nueva = nuevo_indexado.loc[clave]

        for columna in columnas_comparar:

            valor_anterior = fila_anterior[columna]
            valor_nuevo = fila_nueva[columna]

            if not _valores_iguales(
                valor_anterior,
                valor_nuevo,
            ):
                cambios.append(
                    Cambio(
                        clave=clave,
                        tipo="MODIFICADO",
                        columna=columna,
                        valor_anterior=valor_anterior,
                        valor_nuevo=valor_nuevo,
                    )
                )

    return cambios


def _buscar_columnas_faltantes(
    df: pd.DataFrame,
    columnas: list[str],
) -> list[str]:
    """
    Devuelve las columnas solicitadas que no existen en el DataFrame.
    """

    return [
        columna
        for columna in columnas
        if columna not in df.columns
    ]


def _validar_claves_unicas(
    claves: pd.Series,
    nombre_excel: str,
) -> None:
    """
    Comprueba que todas las claves sean únicas.
    """

    duplicadas = claves[
        claves.duplicated(keep=False)
    ].unique()

    if len(duplicadas) > 0:
        raise ClaveDuplicadaError(
            f"Existen claves duplicadas en el {nombre_excel}: "
            f"{duplicadas.tolist()}"
        )


def _valores_iguales(
    valor_anterior: object,
    valor_nuevo: object,
) -> bool:
    """
    Compara dos valores teniendo en cuenta:

    - valores nulos
    - números enteros y decimales
    - fechas
    - textos
    """

    anterior_es_nulo = pd.isna(valor_anterior)
    nuevo_es_nulo = pd.isna(valor_nuevo)

    # Ambos están vacíos
    if anterior_es_nulo and nuevo_es_nulo:
        return True

    # Sólo uno está vacío
    if anterior_es_nulo or nuevo_es_nulo:
        return False

    # ---------------------------------------------------------
    # NÚMEROS
    # ---------------------------------------------------------

    if _es_numero(valor_anterior) and _es_numero(valor_nuevo):
        return float(valor_anterior) == float(valor_nuevo)

    # ---------------------------------------------------------
    # FECHAS
    # ---------------------------------------------------------

    if isinstance(
        valor_anterior,
        (pd.Timestamp,),
    ) and isinstance(
        valor_nuevo,
        (pd.Timestamp,),
    ):
        return valor_anterior == valor_nuevo

    # ---------------------------------------------------------
    # RESTO DE VALORES
    # ---------------------------------------------------------

    return valor_anterior == valor_nuevo


def _es_numero(valor: object) -> bool:
    """
    Determina si un valor es numérico.
    """

    return isinstance(
        valor,
        (int, float, complex),
    ) and not isinstance(
        valor,
        bool,
    )