# AGENTS.md — FastAPI + Poetry + Postgres (plantilla personal)

> Propósito: instrucciones orientadas a agentes de IA y mantenedores humanos para crear y mantener proyectos FastAPI + Poetry + Postgres. Minimalista y adaptable para proyectos personales.

---

## 0. Resumen del proyecto (Project Overview)

Ejemplo de `Project Overview` que debes incluir en el repo:

> **Project Overview**
>
> `taskflow-api` es una API REST construida con FastAPI y gestionada con Poetry. Usa PostgreSQL en producción. El código principal vive en `app/main.py`. El objetivo es servir como plantilla ligera para proyectos personales, con pruebas automatizadas, migraciones con Alembic y linteo con ruff.

> Incluye: endpoints REST, modelos Pydantic, servicios y repositorios simples, tests en `tests/`, y despliegue por Docker Compose.

---

## 1. Estructura de repositorio (sugerida)

```
.
├─ .github/
├─ alembic/
├─ docker/
├─ app/
│  └─ main.py
├─ tests/
├─ .env.example
├─ pyproject.toml
├─ poetry.lock
└─ AGENTS.md
```

> Nota: la app principal está en `app/main.py`. No se usa `src/`.

---

## 2. Comandos de setup y desarrollo

- Instalar dependencias: `poetry install`
- Entrar al virtualenv (opcional): `poetry shell`
- Levantar app en desarrollo (local):

  ```bash
  poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

- Docker Compose (si existe `docker-compose.yml`): `docker compose up --build`
- Variables de entorno: usar `.env`. Si `.env` no existe usar `.env.example` como referencia.

---

## 3. Variables de entorno

- Mantener `.env.example` con todas las variables necesarias y valores de ejemplo.
- Al ejecutar, si no existe `.env`, el agente y los scripts deben cargar valores desde `.env.example` y advertir que deben completarse antes de producción.
- Nunca commitear secretos reales.

---

## 4. Base de datos y migraciones

- Migraciones con Alembic.

  - Generar: `poetry run alembic revision --autogenerate -m "desc"`
  - Aplicar: `poetry run alembic upgrade head`

- Flujo al cambiar modelos:

  1. Actualizar modelos en `app/`.
  2. Generar y revisar migración.
  3. Aplicar migraciones localmente.
  4. Añadir/actualizar tests si aplica.

- En CI usar Postgres efímero o contenedor.

---

## 5. Pruebas

- Framework: `pytest`.
- Carpeta: `tests/`.
- Ejecutar: `poetry run pytest`
- Coverage: `poetry run pytest --cov=app --cov-report=term --cov-report=html`
- Meta mínima de coverage: 70% (para plantilla personal, ajustable).
- DB en tests: usar SQLite en memoria o fixtures que aíslen el estado. Documentar diferencias esperadas frente a Postgres.
- Reglas para el agente:

  - Corregir fallos de tests hasta que la suite pase.
  - Añadir/actualizar tests para cambios funcionales.
  - No eliminar tests sin justificación clara.

---

## 6. Estilo de código y linters

- Formateo y linteo con `ruff`.

  - Check: `poetry run ruff check .`
  - Fix: `poetry run ruff check . --fix`

- Type checking opcional: `poetry run mypy app` o `pyright` apuntando a `app/`.
- Docstrings: funciones públicas y clases deben tener docstring breves.
- Convenciones:

  - Funciones y variables: `snake_case`.
  - Clases: `PascalCase`.
  - Módulos: `snake_case`.

- Pydantic: usar `Field(..., description="...")` para documentación.

---

## 7. Endpoints y documentación

- Cada router/endpoint debe incluir `summary` y `description` para docs OpenAPI.
- Usar modelos de respuesta (Pydantic) siempre que sea posible.
- Centralizar manejo de errores y respuestas estándar.

---

## 8. Integración y contratos

- Tests unitarios para lógica. Tests de integración para flujos con DB.
- Para Postgres en CI usar contenedor efímero. Si se usa SQLite en tests, documentar limitaciones.

---

## 9. Seguridad

- No guardar credenciales en el repo.
- Leer secretos de `.env` o gestor externo.
- Usar ORM/queries parametrizadas.
- Recomendación: cuenta de DB con permisos mínimos en producción.

---

## 10. CI mínimo recomendado

1. `poetry install --no-root`
2. `poetry run ruff check .` (o con `--fix` localmente)
3. `poetry run mypy app` (si se usa)
4. `poetry run pytest --cov=app --cov-report=xml`

> Fallar el build si tests o checks fallan.

---

## 11. Comportamiento esperado del agente

- Objetivo prioritario: pasar tests y no romper CI.
- Antes de cambios relevantes:

  - Ejecutar tests locales.
  - Ejecutar `ruff`.
  - Añadir tests para cambios.
  - Proponer PR con descripción y pasos para reproducir.

- Si el agente necesita ejecutar comandos que afecten infra (DB, secretos), requerir autorización humana o PR revisión.

---

## 12. PR / commits (comentado para proyecto personal)

> Para ahora mantenerlo simple. En proyectos personales puedes usar commits directos. Si trabajas con PRs más adelante, aquí un comentario rápido:

- Title/Branch: describir brevemente el objetivo del cambio junto con el nombre del proyecto en el título del PR.
- Mensajes de commit útiles: `<tipo>(<scope>): breve descripción`.
- Checklist (local): `ruff`, `pytest`, actualizar `CHANGELOG.md` si aplica.

---

## 13. Snippets y comandos útiles

```bash
# install
poetry install

# dev server
poetry run uvicorn app.main:app --reload

# run tests
poetry run pytest

# coverage
poetry run pytest --cov=app --cov-report=html --cov-report=term

# lint & fix
poetry run ruff check . --fix

# type-check (opcional)
poetry run mypy app
```

---

## 14. Notas finales

- Mantener `AGENTS.md` cercano al código. Si hay submódulos con reglas distintas, añadir un `AGENTS.md` específico.
- El agente puede proponer cambios a este archivo si detecta inconsistencias.
- Si `.env` no existe, cargar `.env.example` como referencia y avisar que se deben completar variables.

---

## 15. Recursos

- FastAPI, Alembic, Poetry, Ruff, Pytest, SQLAlchemy / SQLModel.
