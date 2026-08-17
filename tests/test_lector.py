import pandas as pd
import pytest

from src.excel.lector import leer_excel


def test_leer_excel(tmp_path):
    ruta = tmp_path / "prueba.xlsx"

    datos = pd.DataFrame(
        {
            "CODIGO": ["C001", "C002"],
            "COMPOSICION": ["2 x 0.75", "4 x 1.5"],
            "DIAMETRO": [8.2, 12.1],
        }
    )

    datos.to_excel(ruta, index=False)

    resultado = leer_excel(str(ruta))

    assert len(resultado) == 2
    assert list(resultado.columns) == [
        "CODIGO",
        "COMPOSICION",
        "DIAMETRO",
    ]

def test_excel_no_existe():
    with pytest.raises(FileNotFoundError):
        leer_excel("/ruta/que/no/existe.xlsx")