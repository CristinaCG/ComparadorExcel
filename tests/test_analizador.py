import pandas as pd

from src.excel.analizador import analizar_excel


def test_analizar_excel(tmp_path):

    ruta = tmp_path / "prueba.xlsx"

    datos = pd.DataFrame({
        "Codigo": [
            "A001",
            "A002",
            "A003",
            "A003",
        ],
        "Descripcion": [
            "Cable 1",
            "Cable 2",
            "Cable 3",
            "Cable 3 duplicado",
        ],
        "Peso": [
            10.5,
            20.2,
            15.7,
            15.7,
        ],
    })

    with pd.ExcelWriter(ruta) as writer:
        datos.to_excel(
            writer,
            sheet_name="Datos",
            index=False,
        )

    resultado = analizar_excel(str(ruta))

    assert len(resultado) == 1

    hoja = resultado[0]

    assert hoja.nombre == "Datos"
    assert hoja.filas == 4
    assert len(hoja.columnas) == 3

    codigo = hoja.columnas[0]

    assert codigo.nombre == "Codigo"
    assert codigo.valores == 4
    assert codigo.nulos == 0
    assert codigo.unicos == 3
    assert codigo.duplicados == 1