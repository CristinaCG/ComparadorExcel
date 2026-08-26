import json
import sys
from datetime import datetime
from pathlib import Path

from src.database.conexion import conectar


def obtener_ruta_configuracion() -> Path:
    """
    Devuelve la ruta donde se almacenará la configuración
    de la aplicación para el usuario actual.
    """

    if sys.platform == "darwin":

        carpeta = (
            Path.home()
            / "Library"
            / "Application Support"
            / "ComparadorExcel"
        )

    elif sys.platform == "win32":

        carpeta = (
            Path.home()
            / "AppData"
            / "Local"
            / "ComparadorExcel"
        )

    else:

        carpeta = (
            Path.home()
            / ".config"
            / "ComparadorExcel"
        )

    carpeta.mkdir(
        parents=True,
        exist_ok=True,
    )

    return carpeta / "configuracion.sqlite"


class RepositorioConfiguracion:

    def __init__(self, ruta: str | Path):
        self.ruta = Path(ruta)

    def inicializar(self) -> None:

        self.ruta.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with conectar(self.ruta) as conexion:

            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS configuraciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firma TEXT NOT NULL UNIQUE,
                    hoja_anterior TEXT NOT NULL,
                    hoja_nueva TEXT NOT NULL,
                    columnas_clave TEXT NOT NULL,
                    columnas_comparadas TEXT NOT NULL,
                    ultimo_uso DATETIME NOT NULL
                )
                """
            )

            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS preferencias_globales (
                    clave TEXT PRIMARY KEY,
                    valor TEXT NOT NULL
                )
                """
            )

    def obtener_configuracion(self, firma: str):

        self.inicializar()

        with conectar(self.ruta) as conexion:

            configuracion = conexion.execute(
                """
                SELECT
                    id,
                    firma,
                    hoja_anterior,
                    hoja_nueva,
                    columnas_clave,
                    columnas_comparadas,
                    ultimo_uso
                FROM configuraciones
                WHERE firma = ?
                """,
                (firma,),
            ).fetchone()

            if configuracion is None:
                return None

            return {
                "id": configuracion[0],
                "firma": configuracion[1],
                "hoja_anterior": configuracion[2],
                "hoja_nueva": configuracion[3],
                "columnas_clave": json.loads(
                    configuracion[4]
                ),
                "columnas_comparadas": json.loads(
                    configuracion[5]
                ),
                "ultimo_uso": configuracion[6],
            }

    def guardar_configuracion(
        self,
        firma: str,
        hoja_anterior: str,
        hoja_nueva: str,
        columnas_clave: list[str],
        columnas_comparadas: list[str],
    ) -> None:

        self.inicializar()

        ahora = datetime.now().isoformat(
            timespec="seconds"
        )

        with conectar(self.ruta) as conexion:

            conexion.execute(
                """
                INSERT INTO configuraciones (
                    firma,
                    hoja_anterior,
                    hoja_nueva,
                    columnas_clave,
                    columnas_comparadas,
                    ultimo_uso
                )
                VALUES (?, ?, ?, ?, ?, ?)

                ON CONFLICT(firma)
                DO UPDATE SET
                    hoja_anterior = excluded.hoja_anterior,
                    hoja_nueva = excluded.hoja_nueva,
                    columnas_clave = excluded.columnas_clave,
                    columnas_comparadas = excluded.columnas_comparadas,
                    ultimo_uso = excluded.ultimo_uso
                """,
                (
                    firma,
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
                    ahora,
                ),
            )

    def obtener_preferencia(self, clave: str, valor_defecto: str | None = None) -> str | None:
        self.inicializar()

        with conectar(self.ruta) as conexion:
            registro = conexion.execute(
                """
                SELECT valor FROM preferencias_globales WHERE clave = ?
                """,
                (clave,),
            ).fetchone()

            if registro is None:
                return valor_defecto

            return registro[0]

    def guardar_preferencia(self, clave: str, valor: str) -> None:
        self.inicializar()

        with conectar(self.ruta) as conexion:
            conexion.execute(
                """
                INSERT INTO preferencias_globales (clave, valor)
                VALUES (?, ?)
                ON CONFLICT(clave)
                DO UPDATE SET valor = excluded.valor
                """,
                (clave, valor),
            )