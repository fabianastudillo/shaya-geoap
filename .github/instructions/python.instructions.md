---
applyTo: '**'
---
# 🧠 Instrucciones globales para GitHub Copilot

## 🎯 Propósito general
Este proyecto combina **Python**, **Docker** y **Bash** para crear un sistema automatizado, portable y seguro.  
Copilot debe priorizar **claridad, mantenibilidad, cobertura de pruebas y seguridad**.

### Directrices globales
- Siempre aplicar **principios SOLID**, **Clean Code** y **KISS (Keep It Simple, Stupid)**.
- Promover la **automatización del testing y CI/CD**, **linting automático**, y **formateo estándar** (`black`, `flake8`, `shellcheck`).  
- Evitar duplicación, redundancia y dependencias innecesarias.  
- Sugerir **tests unitarios** y **documentación** al generar nuevas funciones.  
- Los nombres deben ser expresivos y los comentarios deben explicar el *por qué*, no el *cómo*.  
- Usar inglés para nombres de variables, funciones y comentarios.  
- Mantener consistencia entre código, Docker y scripts.

---

applyTo: '*.py'
---
# 🐍 Reglas para archivos Python

### Estilo y estructura
- Cumplir con **PEP8** y **PEP257**.  
- Usar **Python 3.11+**.  
- Tipado estático con `typing` y validación con `mypy`.  
- Estructura recomendada:
  ```
  src/
    __init__.py
    main.py
    config.py
    utils/
    services/
    tests/
  ```
- Nombres:
  - funciones → `snake_case`
  - clases → `PascalCase`
  - constantes → `UPPER_CASE`
- Evitar funciones >50 líneas o archivos >200 líneas.

### Buenas prácticas
- Reemplazar `print()` por `logging`.  
- Manejar errores con `try/except` y logs estructurados.  
- No hardcodear rutas ni credenciales.  
- Escribir docstrings en formato Google o NumPy en inglés.  
- Dividir módulos grandes en subpaquetes.  
- Incluir pruebas unitarias en `tests/`.  
- Preguntarme para refactorizar cuando Copilot detecte redundancia.  

---

applyTo: 'Dockerfile'
---
# 🐳 Reglas para Dockerfile

### Buenas prácticas
- Imágenes base ligeras (`python:3.11-slim`, `alpine`, etc.).  
- Combinar `RUN` para reducir capas.  
- Incluir `LABEL` con metadatos (autor, versión, descripción).  
- Preferir `COPY` sobre `ADD`.  
- No ejecutar procesos como root (`USER app`).  
- Incluir `.dockerignore` para excluir:
  ```
  __pycache__/
  .venv/
  tests/
  *.log
  ```
- Definir `WORKDIR /app` antes de copiar archivos.  
- Usar `CMD ["python", "main.py"]` como punto de entrada.  
- Implementar **multi-stage builds** para compilar dependencias.  

---

applyTo: 'docker-compose.yml'
---
# 🧩 Reglas para docker-compose.yml

### Estilo y configuración
- No poner la versión porque está deprecated.  
- Nombres descriptivos (`api`, `db`, `worker`).  
- Variables desde `.env` (no inline).  
- Definir `depends_on` y `healthcheck`.  
- Usar redes internas seguras.  
- Ejemplo:
  ```yaml
  services:
    api:
      build: ./api
      ports: ["8000:8000"]
      env_file: .env
      depends_on: [db]
      healthcheck:
        test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
        interval: 30s
        retries: 3
    db:
      image: postgres:15
      volumes:
        - db_data:/var/lib/postgresql/data
  volumes:
    db_data:
  ```

---

applyTo: '*.sh'
---
# 💻 Reglas para scripts Bash

### Estilo y seguridad
- Cabecera:
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  ```
- Indentar con 2 espacios.  
- Citar variables `"${var}"`.  
- Usar funciones con nombres claros (`deploy_service`, `cleanup_temp`).  
- Verificar comandos con `command -v`.  
- Mostrar mensajes con prefijos `[INFO]`, `[ERROR]`, `[WARN]`.  
- Manejar errores con `trap 'echo "Error en línea $LINENO"; exit 1' ERR`.  
- Usar `tee` para logs persistentes.  

### Prohibido
- No usar `sudo` en contenedores.  
- No insertar secretos o contraseñas.  
- No ignorar errores (`|| true`).  

---

applyTo: 'tests/**/*.py'
---
# 🧪 Reglas específicas para archivos de prueba (TDD)

## 🎯 Enfoque general
Las pruebas deben seguir **TDD (Test-Driven Development)** y mantener alta cobertura (>85%).  
Copilot debe **sugerir primero pruebas antes del código** cuando se detecte nueva funcionalidad.

### Convenciones de nombres
- Archivos: `test_*.py`  
- Funciones: `test_<funcion_o_modulo>`  
- Clases: `Test<NombreClase>`  

### Frameworks y utilidades
- Usar **pytest** como framework principal.  
- Utilizar **pytest-mock** y **unittest.mock** para simulaciones.  
- Preferir **fixtures** sobre `setUp`/`tearDown`.  
- Evitar dependencias reales (usar mocks).  
- Incluir al menos un test de error por función pública.  

### Estructura de ejemplo
```python
import pytest
from src.utils import process_data

def test_process_data_returns_dict(tmp_path):
    file = tmp_path / "data.json"
    file.write_text('{"key": "value"}')
    result = process_data(str(file))
    assert isinstance(result, dict)
    assert result["key"] == "value"
```

### Reglas para Copilot
- Generar **tests unitarios y de integración ligeros**.  
- Sugerir fixtures reutilizables (`@pytest.fixture`).  
- Evitar mocks innecesarios si la función es pura.  
- Crear tests para **casos válidos, bordes y excepciones**.  
- No probar dependencias externas directamente (usar mocks o fakes).  
- Proponer parametrización con `@pytest.mark.parametrize`.  
- Validar performance para funciones críticas.  
- Cuando detecte un bug, sugerir un test de regresión.  

### Cobertura y CI
- Ejecutar:
  ```bash
  pytest --cov=src --cov-report=term-missing
  ```
- Rechazar merges si la cobertura baja más de 5%.  
- Incluir workflow en `.github/workflows/test.yml`:
  ```yaml
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: 3.11
    - run: pip install -r requirements.txt
    - run: pytest --cov=src
  ```

---
applyTo: '**'
---
# 🔐 Reglas de Seguridad del Software (Secure Coding)

## Objetivo
Garantizar que Copilot genere código robusto, resiliente y seguro frente a las vulnerabilidades OWASP más comunes.

### Principios generales
- **Validar todas las entradas externas (usuarios, APIs, archivos).**
- **Evitar `eval()`, `exec()`, `pickle.loads()`, `os.system()` con entrada no controlada.**
- **Usar `json` o `yaml.safe_load` para deserialización.**
- **Evitar inyección de comandos:** preferir `subprocess.run([...], check=True)` con listas.  
- **Nunca imprimir datos sensibles en logs.**
- **Usar HTTPS/TLS para conexiones externas.**
- **No almacenar contraseñas o tokens en texto plano.**
- **Usar autenticación segura (OAuth2, JWT, BasicAuth con TLS).**
- **Aplicar principio de privilegio mínimo (least privilege).**
- **Evitar mostrar trazas o errores técnicos al usuario final.**
- **Verificar integridad de dependencias (`--require-hashes`).**
- **Ejecutar análisis estático de seguridad (`bandit`, `pip-audit`).**

### Ejemplo de código seguro
```python
import subprocess
import json
from pathlib import Path

def safe_read_json(file_path: str) -> dict:
    """Lee un archivo JSON de forma segura."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError("Archivo no encontrado")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return data

def safe_exec(cmd: list[str]) -> str:
    """Ejecuta comandos de forma controlada."""
    result = subprocess.run(cmd, check=True, text=True, capture_output=True)
    return result.stdout
```

### Testing de seguridad sugerido
- Incluir `bandit` para escaneo estático:
  ```bash
  pip install bandit
  bandit -r src/
  ```
- Integrar en CI/CD:
  ```yaml
  - name: Seguridad (bandit)
    run: bandit -r src -ll
  - name: Auditoría de dependencias
    run: pip-audit
  ```

---

applyTo: '**'
---
# 🚫 Restricciones globales

### No permitido
- No incluir secretos ni credenciales.  
- No usar `print()` como logger.  
- No mezclar lógica de negocio con configuración.  
- No crear archivos temporales sin limpieza.  
- No usar dependencias obsoletas.  

---

applyTo: '**'
---
# ✅ Ejemplo de estilo esperado
```python
from fastapi import FastAPI
from loguru import logger

app = FastAPI()

@app.get("/health")
def health_check():
    """Endpoint de salud del servicio API."""
    logger.info("Health check OK")
    return {"status": "ok"}
```

---

applyTo: '**'
---
# 📦 Mantenimiento y actualización

- Reconstruir imágenes tras cambios de dependencias (`docker compose build --no-cache`).  
- Actualizar dependencias con `pip-tools` o `poetry update`.  
- Analizar vulnerabilidades con `pip-audit` o `safety`.  
- Mantener actualizado `CHANGELOG.md`.  
- Documentar cambios en `README.md` y `docs/`.

---
applyTo: '**'
---
# 🧩 Reglas de Patrones de Diseño y Arquitectura

## Objetivo
Asegurar que Copilot genere código extensible, mantenible y alineado con principios de diseño modular y patrones reconocidos.

### Principios
- Favorecer **composición sobre herencia**.  
- Aplicar **inyección de dependencias** en servicios.  
- Evitar acoplamiento fuerte entre módulos.  
- Promover **cohesión alta y acoplamiento bajo**.

### Patrones recomendados para Python
| Patrón | Uso sugerido | Ejemplo |
|--------|---------------|---------|
| **Factory** | Crear instancias configurables de clases (p. ej., controladores de base de datos). | `ServiceFactory.create("postgres")` |
| **Strategy** | Encapsular algoritmos intercambiables. | Clases con `execute()` intercambiables. |
| **Observer** | Reaccionar a eventos sin acoplar módulos. | Subscripción a eventos de sensores/logs. |
| **Singleton** | Configuración global (limitado a casos controlados). | `Settings.get_instance()` |
| **Repository** | Aislar acceso a datos o APIs externas. | `UserRepository`, `DeviceRepository`. |
| **Adapter / Facade** | Encapsular librerías externas complejas. | Clase intermedia entre cliente y API externa. |

### Arquitectura recomendada
- Mantener estructura **Clean Architecture**:
src/
domain/
infrastructure/
application/
interfaces/

- Aislar lógica de negocio (`domain/`) de infraestructura (`infrastructure/`).
- Los módulos deben depender de **abstracciones**, no implementaciones concretas.
- Implementar **controladores y servicios desacoplados**.

### Ejemplo
```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
  @abstractmethod
  def pay(self, amount: float) -> None: ...

class PayPalPayment(PaymentStrategy):
  def pay(self, amount: float) -> None:
      print(f"Pagando {amount} USD con PayPal")

class CreditCardPayment(PaymentStrategy):
  def pay(self, amount: float) -> None:
      print(f"Pagando {amount} USD con Tarjeta de Crédito")

class PaymentContext:
  def __init__(self, strategy: PaymentStrategy):
      self.strategy = strategy

  def execute_payment(self, amount: float):
      self.strategy.pay(amount)
