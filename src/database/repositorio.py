import json
from pathlib import Path

from src.database.conexion import conectar


class RepositorioSQLite:

    def __init__(self, ruta: str | Path):
        self.ruta = Path(ruta)

    def inicializar(self) -> None:
        with conectar(self.ruta) as conexion:
            conexion.executescript(
                """
                CREATE TABLE IF NOT EXISTS comparaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    identificador TEXT NOT NULL,
                    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    archivo_anterior TEXT NOT NULL,
                    archivo_nuevo TEXT NOT NULL,
                    hoja_anterior TEXT NOT NULL,
                    hoja_nueva TEXT NOT NULL,
                    columnas_clave TEXT NOT NULL,
                    columnas_comparadas TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS cambios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    comparacion_id INTEGER NOT NULL,
                    clave TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    columna TEXT,
                    valor_1 TEXT,
                    valor_2 TEXT,

                    FOREIGN KEY (comparacion_id)
                    REFERENCES comparaciones(id)
                    ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_cambios_comparacion
                ON cambios(comparacion_id);

                CREATE INDEX IF NOT EXISTS idx_cambios_clave
                ON cambios(clave);

                CREATE INDEX IF NOT EXISTS idx_cambios_columna
                ON cambios(columna);
                """
            )

    def guardar_comparacion(
        self,
        identificador: str,
        archivo_anterior: str,
        archivo_nuevo: str,
        hoja_anterior: str,
        hoja_nueva: str,
        columnas_clave: list[str],
        columnas_comparadas: list[str],
        cambios,
    ) -> int:

        self.inicializar()

        with conectar(self.ruta) as conexion:

            # =========================================================
            # COMPROBAR SI YA EXISTE EL IDENTIFICADOR
            # =========================================================

            comparacion_existente = conexion.execute(
                """
                SELECT id
                FROM comparaciones
                WHERE identificador = ?
                LIMIT 1
                """,
                (identificador,),
            ).fetchone()

            # =========================================================
            # SI NO EXISTE, CREAR LA COMPARACIÓN
            # =========================================================

            if comparacion_existente is None:

                cursor = conexion.execute(
                    """
                    INSERT INTO comparaciones (
                        identificador,
                        archivo_anterior,
                        archivo_nuevo,
                        hoja_anterior,
                        hoja_nueva,
                        columnas_clave,
                        columnas_comparadas
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        identificador,
                        archivo_anterior,
                        archivo_nuevo,
                        hoja_anterior,
                        hoja_nueva,
                        json.dumps(
                            columnas_clave,
                            ensure_ascii=False,
                        ),
                        json.dumps(
                            columnas_comparadas,
                            ensure_ascii=False,
                        ),
                    ),
                )

                comparacion_id = cursor.lastrowid

            # =========================================================
            # SI YA EXISTE, UTILIZAR ESA COMPARACIÓN
            # =========================================================

            else:

                comparacion_id = comparacion_existente["id"]

            # =========================================================
            # INSERTAR SOLO CAMBIOS QUE NO EXISTAN
            # =========================================================

            for cambio in cambios:

                existe = conexion.execute(
                    """
                    SELECT 1
                    FROM cambios
                    WHERE comparacion_id = ?
                    AND clave = ?
                    AND tipo = ?
                    AND columna = ?
                    LIMIT 1
                    """,
                    (
                        comparacion_id,
                        cambio.clave,
                        cambio.tipo,
                        cambio.columna,
                    ),
                ).fetchone()

                # Ya existe → no hacemos nada
                if existe is not None:
                    continue

                # No existe → insertar
                conexion.execute(
                    """
                    INSERT INTO cambios (
                        comparacion_id,
                        clave,
                        tipo,
                        columna,
                        valor_1,
                        valor_2
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        comparacion_id,
                        cambio.clave,
                        cambio.tipo,
                        cambio.columna,
                        _convertir_valor(cambio.valor_1),
                        _convertir_valor(cambio.valor_2),
                    ),
                )

            return comparacion_id

    def obtener_comparaciones(self):
        self.inicializar()

        with conectar(self.ruta) as conexion:
            cursor = conexion.execute(
                """
                SELECT
                    c.id,
                    c.identificador,
                    c.fecha,
                    c.archivo_anterior,
                    c.archivo_nuevo,
                    c.hoja_anterior,
                    c.hoja_nueva,
                    COUNT(ch.id) AS num_cambios
                FROM comparaciones c
                LEFT JOIN cambios ch
                    ON ch.comparacion_id = c.id
                GROUP BY c.id
                ORDER BY c.fecha DESC
                """
            )

            registros = cursor.fetchall()
            return [
                {
                    "id": reg[0],
                    "identificador": reg[1],
                    "fecha": reg[2],
                    "archivo_anterior": reg[3],
                    "archivo_nuevo": reg[4],
                    "hoja_anterior": reg[5],
                    "hoja_nueva": reg[6],
                    "num_cambios": reg[7],
                }
                for reg in registros
            ]

    def obtener_comparacion(self, comparacion_id: int):
        self.inicializar()

        with conectar(self.ruta) as conexion:

            comparacion = conexion.execute(
                """
                SELECT
                    id,
                    identificador,
                    fecha,
                    archivo_anterior,
                    archivo_nuevo,
                    hoja_anterior,
                    hoja_nueva,
                    columnas_clave,
                    columnas_comparadas
                FROM comparaciones
                WHERE id = ?
                """,
                (comparacion_id,),
            ).fetchone()

            if comparacion is None:
                return None

            return {
                "id": comparacion[0],
                "identificador": comparacion[1],
                "fecha": comparacion[2],
                "archivo_anterior": comparacion[3],
                "archivo_nuevo": comparacion[4],
                "hoja_anterior": comparacion[5],
                "hoja_nueva": comparacion[6],
                "columnas_clave": json.loads(comparacion[7]),
                "columnas_comparadas": json.loads(comparacion[8]),
                "cambios": self.obtener_cambios(comparacion_id),
            }

    def eliminar_comparacion(self, comparacion_id: int) -> None:
        self.inicializar()

        with conectar(self.ruta) as conexion:
            conexion.execute(
                """
                DELETE FROM comparaciones
                WHERE id = ?
                """,
                (comparacion_id,),
            )

    def obtener_cambios(self, comparacion_id: int):
        self.inicializar()
        with conectar(self.ruta) as conexion:
            cambios = conexion.execute(
                """
                SELECT
                    id,
                    clave,
                    tipo,
                    columna,
                    valor_1,
                    valor_2
                FROM cambios
                WHERE comparacion_id = ?
                ORDER BY id
                """,
                (comparacion_id,),
            ).fetchall()

            return cambios

    def obtener_historico_cambios(self):
        self.inicializar()

        with conectar(self.ruta) as conexion:

            cambios = conexion.execute(
                """
                SELECT
                    comparaciones.id AS comparacion_id,
                    comparaciones.fecha,
                    comparaciones.identificador,
                    cambios.id AS cambio_id,
                    cambios.clave,
                    cambios.tipo,
                    cambios.columna,
                    cambios.valor_1,
                    cambios.valor_2
                FROM cambios

                INNER JOIN comparaciones
                    ON cambios.comparacion_id = comparaciones.id

                ORDER BY
                    comparaciones.fecha DESC,
                    cambios.id
                """
            ).fetchall()
            return cambios

def _convertir_valor(valor):
    if valor is None:
        return None

    return str(valor)