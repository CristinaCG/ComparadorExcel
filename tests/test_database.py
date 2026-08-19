from src.database.repositorio import RepositorioSQLite


def test_crear_base_de_datos(tmp_path):

    ruta = tmp_path / "prueba.sqlite"

    repositorio = RepositorioSQLite(ruta)

    repositorio.inicializar()

    assert ruta.exists()


def test_crear_tablas(tmp_path):

    ruta = tmp_path / "prueba.sqlite"

    repositorio = RepositorioSQLite(ruta)

    repositorio.inicializar()

    import sqlite3

    conexion = sqlite3.connect(ruta)

    tablas = conexion.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()

    nombres = {
        tabla[0]
        for tabla in tablas
    }

    conexion.close()

    assert "comparaciones" in nombres
    assert "cambios" in nombres