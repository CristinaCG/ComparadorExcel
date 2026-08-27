import sqlite3
from pathlib import Path


def conectar(ruta: str | Path) -> sqlite3.Connection:
    """
    Crea una conexión a una base de datos SQLite.

    Si el archivo no existe, SQLite lo crea automáticamente.
    """

    ruta = Path(ruta)

    ruta.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    conexion = sqlite3.connect(ruta)

    conexion.row_factory = sqlite3.Row

    conexion.execute("PRAGMA foreign_keys = ON;")
    conexion.execute("PRAGMA journal_mode = WAL;")
    conexion.execute("PRAGMA synchronous = NORMAL;")
    conexion.execute("PRAGMA cache_size = -64000;")
    conexion.execute("PRAGMA temp_store = MEMORY;")

    return conexion