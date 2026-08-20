## Desarrollo

### Entorno virtual

El proyecto utiliza un entorno virtual de Python ubicado en `.venv`.

En Windows, activar el entorno desde PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Una vez activado, la terminal debería mostrar:

```text
(.venv)
```

---

### Ejecutar la aplicación

Desde la raíz del proyecto:

```powershell
python -m src.main
```

También se puede utilizar directamente el Python del entorno virtual:

```powershell
.venv\Scripts\python -m src.main
```

---

### Tests

El proyecto utiliza `pytest`.

Para ejecutar todos los tests:

```powershell
python -m pytest -v
```

Para ejecutar los tests de un módulo concreto:

```powershell
python -m pytest tests\test_comparador.py -v
```

Por ejemplo, para los tests del lector de Excel:

```powershell
python -m pytest tests\test_lector.py -v
```

Para ejecutar un test concreto utilizando parte de su nombre:

```powershell
python -m pytest tests\test_comparador.py -v -k nombre_del_test
```

---

### Interfaz gráfica con Qt Designer

La interfaz gráfica se diseña utilizando **Qt Designer** y se guarda en archivos `.ui`.

El flujo de trabajo es:

```text
Qt Designer
     ↓
archivo .ui
     ↓
pyside6-uic
     ↓
archivo Python generado
     ↓
lógica de la aplicación
     ↓
src.main
```

Por ejemplo, si la interfaz está en:

```text
src/ui/main_window.ui
```

se genera el código Python mediante:

```powershell
pyside6-uic src\ui\main_window.ui -o src\ui\ui_main_window.py
```

El archivo `ui_main_window.py` es un archivo **generado automáticamente** y no debe modificarse manualmente.

Los cambios visuales deben realizarse en Qt Designer y posteriormente volver a generar el archivo Python con `pyside6-uic`.

La lógica de la aplicación debe mantenerse en:

```text
src/ui/main_window.py
```

De esta forma separamos el diseño de la interfaz de la lógica de Python.

---

### Flujo habitual al modificar la interfaz

Cuando se modifica la interfaz en Qt Designer:

1. Abrir el archivo `.ui` en Qt Designer.
2. Realizar los cambios visuales.
3. Guardar el archivo `.ui`.
4. Regenerar el archivo Python:

```powershell
pyside6-uic src\ui\main_window.ui -o src\ui\ui_main_window.py
```

5. Ejecutar los tests:

```powershell
python -m pytest -v
```

6. Ejecutar la aplicación:

```powershell
python -m src.main
```

---

### Estructura relacionada con la interfaz

```text
src/
├── main.py
│
└── ui/
    ├── main_window.ui
    ├── ui_main_window.py
    └── main_window.py
```

* `main_window.ui` → diseño creado con Qt Designer.
* `ui_main_window.py` → código generado automáticamente mediante `pyside6-uic`.
* `main_window.py` → lógica de la ventana.
* `main.py` → punto de entrada de la aplicación.

---

### Dependencias

Para consultar las versiones instaladas:

```powershell
python -m pip show PySide6
python -m pip show qextrawidgets
```

Para consultar todas las dependencias:

```powershell
python -m pip freeze
```

> **Nota:** `qextrawidgets` contiene widgets adicionales utilizados por la aplicación, entre ellos `QFilterableTableView`.

### Exportar la aplicación a `.exe`

Para generar el ejecutable de Windows se utiliza **PyInstaller** dentro del entorno virtual `.venv`.

Primero, activar el entorno virtual:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar PyInstaller si todavía no está instalado:

```powershell
python -m pip install pyinstaller
```

Desde la raíz del proyecto, generar el ejecutable:

```powershell
.venv\Scripts\pyinstaller.exe --name ComparadorExcel --windowed --onefile src\main.py
```

También se puede ejecutar mediante el módulo de Python:

```powershell
python -m PyInstaller --name ComparadorExcel --windowed --onefile src\main.py
```

Una vez finalizado el proceso, PyInstaller creará la carpeta:

```text
dist/
└── ComparadorExcel.exe
```

El archivo:

```text
dist\ComparadorExcel.exe
```

es la aplicación ejecutable y puede copiarse a otro equipo Windows.

Las carpetas y archivos `build/` y `ComparadorExcel.spec` son generados por PyInstaller durante el proceso.

> **Importante:** el `.exe` debe generarse en Windows. PyInstaller no permite generar directamente un ejecutable `.exe` de Windows desde macOS.

---

### Generar una nueva versión

El flujo recomendado antes de crear una nueva versión es:

1. Activar el entorno virtual.
2. Ejecutar los tests.
3. Probar la aplicación.
4. Generar el `.exe` con PyInstaller.

```powershell
.venv\Scripts\Activate.ps1
python -m pytest -v
python -m src.main
python -m PyInstaller --name ComparadorExcel --windowed --onefile src\main.py
```

El resultado estará en:

```text
dist\ComparadorExcel.exe
```
