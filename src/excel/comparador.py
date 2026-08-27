from dataclasses import dataclass

import numpy as np
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
        Para NUEVO y ELIMINADO será None.

    valor_1:
        Valor existente en el Excel anterior.

    valor_2:
        Valor existente en el Excel nuevo.
    """

    clave: str
    tipo: str
    columna: str | None
    valor_1: object
    valor_2: object


def comparar_dataframes(
    anterior: pd.DataFrame,
    nuevo: pd.DataFrame,
    columnas_clave: list[str],
    columnas_comparar: list[str],
) -> list[Cambio]:
    """
    Compara dos DataFrames utilizando una o varias columnas como clave
    mediante operaciones vectorizadas con pandas para alto rendimiento.
    """

    # ---------------------------------------------------------
    # VALIDACIÓN DE COLUMNAS
    # ---------------------------------------------------------

    if columnas_clave:
        columnas_faltantes_anterior = _buscar_columnas_faltantes(
            anterior,
            columnas_clave,
        )

        columnas_faltantes_nuevo = _buscar_columnas_faltantes(
            nuevo,
            columnas_clave,
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

    columnas_faltantes_comparar_anterior = _buscar_columnas_faltantes(
        anterior,
        columnas_comparar,
    )

    columnas_faltantes_comparar_nuevo = _buscar_columnas_faltantes(
        nuevo,
        columnas_comparar,
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
    # CREAR CLAVES
    # ---------------------------------------------------------

    if columnas_clave:
        clave_anterior = crear_clave(
            anterior,
            columnas_clave,
        )

        clave_nuevo = crear_clave(
            nuevo,
            columnas_clave,
        )

        _validar_claves_unicas(
            clave_anterior,
            "Excel anterior",
        )

        _validar_claves_unicas(
            clave_nuevo,
            "Excel nuevo",
        )
    else:
        # Comparación línea a línea por posición de fila
        clave_anterior = pd.Series([f"Fila {i + 1}" for i in range(len(anterior))], index=anterior.index)
        clave_nuevo = pd.Series([f"Fila {i + 1}" for i in range(len(nuevo))], index=nuevo.index)

    # Indexar dataframes por la clave de comparación
    df_ant = anterior[columnas_comparar].copy()
    df_ant.index = clave_anterior

    df_nue = nuevo[columnas_comparar].copy()
    df_nue.index = clave_nuevo

    claves_anterior = set(df_ant.index)
    claves_nuevo = set(df_nue.index)

    claves_nuevas = claves_nuevo - claves_anterior
    claves_eliminadas = claves_anterior - claves_nuevo
    claves_comunes = sorted(list(claves_anterior & claves_nuevo))

    cambios: list[Cambio] = []

    # ---------------------------------------------------------
    # REGISTROS NUEVOS Y ELIMINADOS
    # ---------------------------------------------------------

    for clave in sorted(claves_nuevas):
        cambios.append(
            Cambio(
                clave=clave,
                tipo="NUEVO",
                columna=None,
                valor_1=None,
                valor_2=None,
            )
        )

    for clave in sorted(claves_eliminadas):
        cambios.append(
            Cambio(
                clave=clave,
                tipo="ELIMINADO",
                columna=None,
                valor_1=None,
                valor_2=None,
            )
        )

    if not claves_comunes:
        return cambios

    # ---------------------------------------------------------
    # COMPARACIÓN VECTORIZADA DE REGISTROS COMUNES
    # ---------------------------------------------------------

    sub_ant = df_ant.loc[claves_comunes]
    sub_nue = df_nue.loc[claves_comunes]

    for columna in columnas_comparar:
        s_ant = sub_ant[columna]
        s_nue = sub_nue[columna]

        # Máscara vectorizada de valores diferentes
        # Nulos equivalentes
        nulos_ant = s_ant.isna()
        nulos_nue = s_nue.isna()

        diferentes = ~((nulos_ant & nulos_nue) | (s_ant == s_nue))

        # Tratar comparaciones numéricas equivalentes (ej: 10 y 10.0)
        idx_evaluar = s_ant.index[diferentes]

        if len(idx_evaluar) == 0:
            continue

        v_ant = s_ant.loc[idx_evaluar]
        v_nue = s_nue.loc[idx_evaluar]

        for clave_idx, val1, val2 in zip(idx_evaluar, v_ant, v_nue):
            if not _valores_iguales(val1, val2):
                cambios.append(
                    Cambio(
                        clave=str(clave_idx),
                        tipo="MODIFICADO",
                        columna=columna,
                        valor_1=val1,
                        valor_2=val2,
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
    valor_1: object,
    valor_2: object,
) -> bool:
    """
    Compara dos valores teniendo en cuenta:
    - valores nulos
    - números enteros y decimales
    - fechas
    - textos
    """

    anterior_es_nulo = pd.isna(valor_1)
    nuevo_es_nulo = pd.isna(valor_2)

    if anterior_es_nulo and nuevo_es_nulo:
        return True

    if anterior_es_nulo or nuevo_es_nulo:
        return False

    if _es_numero(valor_1) and _es_numero(valor_2):
        return float(valor_1) == float(valor_2)

    if isinstance(
        valor_1,
        pd.Timestamp,
    ) and isinstance(
        valor_2,
        pd.Timestamp,
    ):
        return valor_1 == valor_2

    return valor_1 == valor_2


def _es_numero(valor: object) -> bool:
    """
    Determina si un valor es numérico.
    """

    return isinstance(
        valor,
        (int, float, complex, np.number),
    ) and not isinstance(
        valor,
        bool,
    )
