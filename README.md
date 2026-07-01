# api-fastapi

> **API CRUD con FastAPI** – Personajes de **Kimetsu no Yaiba (鬼滅の刃)**

Proyecto educativo que muestra cómo construir una **API REST** completa siguiendo una arquitectura por capas (Domain, Application, Infrastructure) y aplicando **TDD (Test-Driven Development)**.

---

## Índice

1. [Introducción](#1-introducción)
2. [Arquitectura del Proyecto](#2-arquitectura-del-proyecto)
3. [Configuración del entorno](#3-configuración-del-entorno)
4. [Guion por commits](#4-guion-por-commits)
5. [Resumen final del proyecto](#5-resumen-final-del-proyecto)
6. [Recursos Adicionales](#6-recursos-adicionales)

---

## 1. Introducción

**FastAPI** es un framework moderno para construir APIs con Python. Se basa en:

- **Starlette** → manejo web (rutas, middleware)
- **Pydantic** → validación de datos

Es rápido, tiene documentación automática (Swagger / ReDoc) y soporta tipado estático.

### 🎯 ¿Qué vamos a construir?

Una **API CRUD de personajes de Kimetsu no Yaiba** donde podrás:

- Crear un personaje (Tanjiro, Nezuko, Zenitsu…)
- Listarlos todos
- Ver uno por id
- Actualizar su información
- Eliminarlos

Cada personaje tiene:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `name` | Nombre del personaje | "Tanjiro Kamado" |
| `state` | Estado (alive / dead) | "alive" |
| `img` | URL de su imagen | "https://example.com/tanjiro.jpg" |

---

## 2. Arquitectura del Proyecto

```
api-fastapi/
│
├── conftest.py                    # Configuración de pytest
├── main.py                        # Punto de entrada + CORS
├── requirements.txt
├── characters.db                  # BD SQLite (se genera al ejecutar)
│
├── src/
│   ├── __init__.py
│   ├── characters/                # ⭐ Módulo de personajes (CRUD)
│   │   ├── __init__.py
│   │   ├── domain/                # Reglas de negocio puras
│   │   │   ├── __init__.py
│   │   │   ├── models.py          # Entidad Character
│   │   │   ├── value_objects.py   # CharacterImg (inmutable + validación)
│   │   │   ├── exception.py       # CharacterImgNotValid
│   │   │   └── repositories.py    # Interfaz abstracta
│   │   ├── application/           # Casos de uso
│   │   │   ├── __init__.py
│   │   │   ├── create_character.py
│   │   │   ├── get_all_character.py
│   │   │   ├── get_character_by_id.py
│   │   │   ├── update_character.py
│   │   │   └── delete_character.py
│   │   ├── infraestructure/       # Detalles técnicos
│   │   │   ├── __init__.py
│   │   │   ├── api.py             # Endpoints FastAPI
│   │   │   └── repositories.py    # SQLModelCharacterRepository
│   │   └── test/                  # Tests organizados por capa
│   │       ├── application/
│   │       │   ├── test_create_character.py
│   │       │   ├── test_get_all_character.py
│   │       │   ├── test_update_character.py
│   │       │   └── test_delete_character.py
│   │       └── infraestructure/
│   │           ├── api/test_create_character.py
│   │           └── repositories/test_sql_model_character_repository.py
│   │
│   └── shared/                    # Endpoints genéricos
│       ├── __init__.py
│       ├── domain/__init__.py
│       ├── application/__init__.py
│       ├── infraestructure/
│       │   ├── __init__.py
│       │   └── api.py             # GET /
│       └── test/infraestructure/test_help.py
│
└── venv/
```

### ¿Por qué `__init__.py` y `__pycache__/`?

**`__init__.py`** convierte un directorio en un **paquete Python**. Sin él, no puedes hacer `from src.characters.domain import models`.

**`__pycache__/`** lo genera Python al importar módulos. Guarda bytecode (`.pyc`) para acelerar futuras importaciones. **No debe versionarse** → va al `.gitignore`.

```gitignore
# .gitignore (resumen)
__pycache__/
*.py[cod]
venv/
*.db
.pytest_cache/
```

Para crear los `__init__.py` del proyecto:

```bash
touch src/__init__.py
touch src/characters/__init__.py
touch src/characters/domain/__init__.py
touch src/characters/application/__init__.py
touch src/characters/infraestructure/__init__.py
touch src/shared/__init__.py
touch src/shared/domain/__init__.py
touch src/shared/application/__init__.py
touch src/shared/infraestructure/__init__.py
```

---

## 3. Configuración del entorno

```bash
cd /Users/bcnmac020/Documents/projects/cambra/api-fastapi

# Entorno virtual
python3 -m venv venv
source venv/bin/activate

# Dependencias
pip install "fastapi[standard]" pytest validators sqlmodel httpx
```

`requirements.txt`:

```text
#API
fastapi==0.128.8
validators==0.35.0

#Database
sqlmodel==0.0.38

# Testing
httpx==0.28.1
pytest==8.4.2
```

---

## 4. Guion por commits

Aquí seguimos el **orden real de los commits** del proyecto. Cada uno incluye:

- 📌 **Qué se hizo**
- 💻 **El código que se añadió**
- 💬 **Explicación**

---

### Commit 1 – `feat: initial commit`

📌 Se creó el repositorio con un `.gitignore` mínimo.

`.gitignore`:

```gitignore
__pycache__/
venv/
```

> 💬 Todo proyecto Python empieza ignorando `__pycache__/` y el `venv/`.

---

### Commit 2 – `feat: add readme`

📌 Esqueleto mínimo de la app.

**`main.py`:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "HelloWorld"}
```

**`src/__init__.py`:** (vacío)

> 💬 `src/__init__.py` convierte `src` en un **paquete Python**, lo que nos permite hacer imports del estilo `from src.characters.domain.models import Character`.

---

### Commit 3 – `feat: add create resoucer and test`

📌 Estructura por capas y caso de uso `CreateCharacter` con su test (TDD – primer Green).

#### 📁 `conftest.py`

```python
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
```

> 💬 pytest necesita que la raíz esté en `sys.path` para poder hacer `from main import app`.

#### 📁 `src/characters/domain/models.py`

```python
class Character:
    def __init__(self, name: str, state: str, img: str):
        self._name = name
        self._state = state
        self._img = img
```

> 💬 La **entidad de dominio**. Representa un personaje.

#### 📁 `src/characters/domain/repositories.py`

```python
from abc import ABC, abstractmethod
from src.characters.domain.models import Character

class CharacterRepository(ABC):
    @abstractmethod
    def all(self) -> list[Character]: ...
    
    @abstractmethod
    def save(self, character: Character) -> None: ...
```

> 💬 La **interfaz** del repositorio. Define el *contrato* sin importar cómo se persiste.

#### 📁 `src/characters/application/create_character.py`

```python
from dataclasses import dataclass
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository

@dataclass
class CreateCharacterCommand:
    name: str
    state: str
    img: str

class CreateCharacter:
    def __init__(self, character_repository: CharacterRepository):
        self._character_repository = character_repository

    def execute(self, command: CreateCharacterCommand) -> Character:
        character = Character(
            name=command.name,
            state=command.state,
            img=command.img
        )
        self._character_repository.save(character)
        return character
```

> 💬 El **caso de uso**. Recibe el repositorio por **inyección de dependencias**. El `Command` es un DTO con los datos de entrada.

#### 📁 `src/characters/infraestructure/repositories.py`

```python
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository

class InMemoryCharacterRepository(CharacterRepository):
    def __init__(self):
        self._characters = []
    
    def all(self) -> list[Character]:
        return list(self._characters)
    
    def save(self, character: Character) -> None:
        self._characters.append(character)
```

> 💬 Primera implementación **en memoria** (sin BD), para poder hacer tests sin SQL.

#### 📁 `src/shared/infraestructure/api.py`

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"msg": "HelloWorld"}
```

#### 📁 `src/characters/test/application/test_create_character.py` (TEST)

```python
import pytest
from src.characters.application.create_character import CreateCharacter, CreateCharacterCommand
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository

class FakeCharacterRepository(CharacterRepository):
    def __init__(self):
        self._characters = []
    def save(self, character: Character) -> None:
        self._characters.append(character)
    def all(self) -> list[Character]:
        return list(self._characters)


class TestCreateCharacter:
    def test_create_character(self) -> None:
        character_repository = FakeCharacterRepository()
        
        CreateCharacter(character_repository).execute(
            CreateCharacterCommand(
                name="Tanjiro Kamado",
                state="alive",
                img="https://example.com/tanjiro.jpg"
            )
        )
        characters = character_repository.all()
        assert len(characters) == 1
```

> 💬 El `FakeCharacterRepository` sustituye al real. Esto es **inyección de dependencias en acción**: test rápido, sin BD, 100% determinista.

---

### Commit 4 – `test: red test for url`

📌 Test que falla (🔴 RED) porque aún no validamos imágenes.

```python
    def test_create_character_fails_with_invalid_img(self) -> None:
        character_repository = FakeCharacterRepository()
        with pytest.raises(Exception):  # falla: no se lanza nada aún
            CreateCharacter(character_repository).execute(
                CreateCharacterCommand(
                    name="Tanjiro Kamado",
                    state="alive",
                    img="invalid_img"
                )
            )
```

> 💬 TDD: primero el test, luego el código de producción.

---

### Commit 5 – `test: add green test and add url functionality`

📌 Añadimos el factory method `create`. 🟢 GREEN.

```python
# src/characters/domain/models.py
class Character:
    def __init__(self, name: str, state: str, img: CharacterImg, id: int | None = None):
        self._id = id
        self._name = name
        self._state = state
        self._img = img
    
    @classmethod
    def create(cls, name: str, state: str, img: str) -> "Character":
        return cls(name, state, img)
    
     def name(self) -> str:
        return self._name

    def state(self) -> str:
        return self._state

    def img(self) -> "CharacterImg":
        return self._img
    
    def id(self) -> int | None:
        return self._id
```

> 💬 El `classmethod` `create` centraliza la construcción. Es la puerta de entrada para meter aquí luego la validación.

---

### Commit 6 – `test: red test for exception for url`

📌 Test que pide lanzar una **excepción concreta** cuando la imagen no es válida.

```python
# src/characters/domain/exception.py
class CharacterImgNotValid(Exception):
    pass
```

---

### Commit 7 – `feat: add validators for Resource url`

📌 Implementamos la validación con un **Value Object**. 🟢 GREEN.

```python
# src/characters/domain/value_objects.py
from dataclasses import dataclass
import validators
from src.characters.domain.exception import CharacterImgNotValid

@dataclass(frozen=True, kw_only=True)
class CharacterImg:
    value: str
    
    def __post_init__(self) -> None:
        if not validators.url(self.value):
            raise CharacterImgNotValid
```

> 💬 **Value Object**: inmutable (`frozen=True`) y se valida en su construcción. Si la URL no es válida, la `CharacterImg` **no puede existir**.

---

### Commit 8 – `test: red test for respository sql`

📌 Test que requiere **SQLModel** y una BD SQLite real. 🔴 RED.

```python
# src/characters/test/infraestructure/repositories/test_sql_model_character_repository.py
import pytest
from sqlmodel import SQLModel, select, Session
from src.characters.domain.models import Character
from src.characters.domain.value_objects import CharacterImg
from src.characters.infraestructure.repositories import SQLModelCharacterRepository, engine, CharacterModel


class TestSQLModelCharacterRepository:
    def test_saves_character_to_database(self) -> None:
        repository = SQLModelCharacterRepository()
        repository.save(Character(
            name="Tanjiro Kamado",
            state="alive",
            img=CharacterImg(value="https://example.com/tanjiro.jpg")
        ))
```

---

### Commit 9 – `feat: add model to resource and pass to green test`

📌 Implementamos `SQLModelCharacterRepository` con SQLModel + SQLite. 🟢 GREEN.

```python
# src/characters/infraestructure/repositories.py
from sqlmodel import SQLModel, Field, create_engine, Session, select
from src.characters.domain.value_objects import CharacterImg
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository


class CharacterModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    name: str
    state: str
    img: str

engine = create_engine("sqlite:///characters.db")
SQLModel.metadata.create_all(engine)


class SQLModelCharacterRepository(CharacterRepository):
    def all(self) -> list[Character]:
        with Session(engine) as session:
            character_models = session.exec(select(CharacterModel)).all()
        return [
            Character(
                name=character_model.name,
                state=character_model.state,
                img=CharacterImg(value=character_model.img),
                id=character_model.id
            )
            for character_model in character_models
        ]

    def save(self, character: Character) -> None:
        character_model = CharacterModel(
            name=character.name(),
            state=character.state(),
            img=character.img().value
        )
        with Session(engine) as session:
            session.add(character_model)
            session.commit()
```

---

### Commit 10 – `test: delete the fake resourcer for test`

📌 Limpiamos el fake y añadimos un `fixture` que crea/borra las tablas en cada test.

```python
@pytest.fixture(autouse=True)
def cleanup_database(self):
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)
```

> 💬 El `fixture(autouse=True)` se ejecuta **antes y después de cada test** → los tests no se pisan entre sí.

---

### Commit 11 – `test: red test for resource all`

📌 Test que pide poder **leer varios** characters. 🔴 RED.

```python
# src/characters/test/application/test_get_all_character.py
class TestGetAllCharacters:
    def test_get_all_returns_all_characters(self) -> None:
        character_repository = FakeCharacterRepository()

        character1 = Character(
            name="Tanjiro Kamado",
            state="alive",
            img=CharacterImg(value="https://example.com/tanjiro.jpg")
        )
        character2 = Character(
            name="Nezuko Kamado",
            state="alive",
            img=CharacterImg(value="https://example.com/nezuko.jpg")
        )
        character_repository.save(character1)
        character_repository.save(character2)

        result = GetAllCharacters(character_repository).execute()

        assert len(result) == 2
        assert result[0].name() == "Tanjiro Kamado"
        assert result[1].name() == "Nezuko Kamado"

    def test_get_all_returns_empty_list(self) -> None:
        character_repository = FakeCharacterRepository()

        result = GetAllCharacters(character_repository).execute()

        assert len(result) == 0
```

> 💬 Cubrimos dos escenarios: lista con datos y lista vacía. La forma vacía evita falsos positivos (`return []` accidental).

---

### Commit 12 – `feat: add get all resource`

📌 Implementamos el caso de uso `GetAllCharacters` delegando en el repositorio. 🟢 GREEN.

```python
# src/characters/application/get_all_character.py
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository

class GetAllCharacters:
    def __init__(self, character_repository: CharacterRepository):
        self._character_repository = character_repository

    def execute(self) -> list[Character]:
        return self._character_repository.all()
```

> 💬 El caso de uso es **finísimo**: solo orquesta. La lógica de cómo se recuperan los datos vive en el repositorio. Esto mantiene la aplicación independiente de SQLite/SQLModel.

---

### Commit 13 – `test: integration test for create resource`

📌 **Test de integración** del endpoint HTTP con `TestClient`. 🔴 RED.

```python
# src/characters/test/infraestructure/api/test_create_character.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_character_and_returns_200():
    response = client.post(
        "/characters/",
        json={
            "name": "Tanjiro Kamado",
            "state": "alive",
            "img": "https://example.com/tanjiro.jpg"
        }
    )
    assert response.status_code == 200
```

> 💬 `TestClient` simula un cliente HTTP real. Permite probar la API completa **sin servidor**, sin red.

---

### Commit 14 – `feat: add routes to app`

📌 Creamos el router de characters, lo añadimos a `main.py`.

```python
# main.py
from src.characters.infraestructure.api import router as characters_router
# ...
app.include_router(characters_router)
```

---

```python
# src/characters/infraestructure/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from src.characters.domain.models import Character
from src.characters.application.create_character import CreateCharacter, CreateCharacterCommand
from src.characters.infraestructure.repositories import SQLModelCharacterRepository

router = APIRouter()

class CharacterPayload(BaseModel):
    name: str
    state: str
    img: str

class CharacterResponse(BaseModel):
    name: str
    state: str
    img: str
    
    @classmethod
    def from_domain(cls, character: Character) -> "CharacterResponse":
        return cls(
            name=character.name(),
            state=character.state(),
            img=character.img().value
        )

@router.post("/characters/")
def create_character(payload: CharacterPayload) -> CharacterResponse:
    character = CreateCharacter(SQLModelCharacterRepository()).execute(
        CreateCharacterCommand(
            name=payload.name,
            state=payload.state,
            img=payload.img
        )
    )
    return CharacterResponse.from_domain(character)
```

> 💬 **Flujo completo:**
> 1. FastAPI recibe JSON, lo valida con `CharacterPayload` (Pydantic)
> 2. Se instancia `CreateCharacter` con el repo SQL
> 3. El caso de uso crea `CharacterImg` (valida) y `Character`
> 4. El repo guarda en SQLite
> 5. Devolvemos un `CharacterResponse` (Pydantic) → JSON

---

### Commit 16 – `feat: add create resource`

📌 Se refinó el endpoint para que `save` **retorne el `Character` con el id generado**.

```python
# src/characters/infraestructure/repositories.py
    def save(self, character: Character) -> Character:
        character_model = CharacterModel(
            name=character.name(),
            state=character.state(),
            img=character.img().value
        )
        with Session(engine) as session:
            session.add(character_model)
            session.commit()
            session.refresh(character_model)   # ← necesario para obtener el id
            return Character(
                name=character_model.name,
                state=character_model.state,
                img=CharacterImg(value=character_model.img),
                id=character_model.id
            )
```

> 💬 Sin `session.refresh(character_model)`, el `id` queda en `None` hasta cerrar la sesión.

---

### Commit 17 – `feat: add cors`

📌 Añadimos **CORS** para que un frontend pueda llamar a la API.

```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

> 💬 Los navegadores **bloquean** por defecto las peticiones cross-origin. `CORSMiddleware` añade las cabeceras necesarias.

Para que el front se conecte desde otra máquina:

```bash
fastapi dev --host 0.0.0.0 --port 8000
```

---

### Commit 18 – `feat: add all crud and test`

📌 Añadimos los casos de uso y endpoints: `get_by_id`, `update`, `delete`, y sus tests separados.

#### Contrato del repositorio

Primero ampliamos la interfaz `CharacterRepository` para reflejar todas las operaciones:

```python
# src/characters/domain/repositories.py
from abc import ABC, abstractmethod
from src.characters.domain.models import Character

class CharacterRepository(ABC):
    @abstractmethod
    def all(self) -> list[Character]: ...

    @abstractmethod
    def get_by_id(self, id: int) -> Character | None: ...

    @abstractmethod
    def save(self, character: Character) -> Character: ...

    @abstractmethod
    def update(self, id: int, character: Character) -> Character | None: ...

    @abstractmethod
    def delete(self, id: int) -> bool: ...
```

> 💬 `get_by_id` y `update` devuelven `Character | None` para distinguir "no existe" (404) de "existe pero vacío". `delete` devuelve `bool` por la misma razón: no es lo mismo borrar que no encontrar.

#### Métodos del repositorio SQL

```python
# src/characters/infraestructure/repositories.py
def get_by_id(self, id: int) -> Character | None:
    with Session(engine) as session:
        character_model = session.get(CharacterModel, id)
        if character_model is None:
            return None
        return Character(
            name=character_model.name,
            state=character_model.state,
            img=CharacterImg(value=character_model.img),
            id=character_model.id
        )

def update(self, id: int, character: Character) -> Character | None:
    with Session(engine) as session:
        character_model = session.get(CharacterModel, id)
        if character_model is None:
            return None
        character_model.name = character.name()
        character_model.state = character.state()
        character_model.img = character.img().value
        session.add(character_model)
        session.commit()
        return Character(
            name=character_model.name,
            state=character_model.state,
            img=CharacterImg(value=character_model.img),
            id=character_model.id
        )

def delete(self, id: int) -> bool:
    with Session(engine) as session:
        character_model = session.get(CharacterModel, id)
        if character_model is None:
            return False
        session.delete(character_model)
        session.commit()
        return True
```

> 💬 En `update` no usamos `session.refresh` porque los campos que tocamos (`name`, `state`, `img`) ya están en memoria. Solo el `id` se necesita, y viene del propio `CharacterModel` que ya lo tenía.

#### Casos de uso

```python
# get_character_by_id.py
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository

class GetCharacterById:
    def __init__(self, character_repository: CharacterRepository):
        self._character_repository = character_repository

    def execute(self, id: int) -> Character | None:
        return self._character_repository.get_by_id(id)
```

```python
# update_character.py
from dataclasses import dataclass
from src.characters.domain.value_objects import CharacterImg
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository

@dataclass
class UpdateCharacterCommand:
    id: int
    name: str
    state: str
    img: str

class UpdateCharacter:
    def __init__(self, character_repository: CharacterRepository):
        self._character_repository = character_repository

    def execute(self, command: UpdateCharacterCommand) -> Character | None:
        character_img = CharacterImg(value=command.img)
        character = Character(
            name=command.name,
            state=command.state,
            img=character_img
        )
        return self._character_repository.update(command.id, character)
```

```python
# delete_character.py
from dataclasses import dataclass
from src.characters.domain.repositories import CharacterRepository

@dataclass
class DeleteCharacterCommand:
    id: int

class DeleteCharacter:
    def __init__(self, character_repository: CharacterRepository):
        self._character_repository = character_repository

    def execute(self, command: DeleteCharacterCommand) -> bool:
        return self._character_repository.delete(command.id)
```

> 💬 El caso de uso de update **vuelve a pasar por la validación de `CharacterImg`**: si alguien manda una URL inválida al `PUT`, también se rechaza. Las reglas de dominio se respetan en cada entrada de datos.

#### Endpoints

```python
# src/characters/infraestructure/api.py
@router.get("/characters/")
def get_all_characters() -> list[CharacterResponse]:
    characters = GetAllCharacters(SQLModelCharacterRepository()).execute()
    return [CharacterResponse.from_domain(c) for c in characters]

@router.get("/characters/{id}")
def get_character_by_id(id: int) -> CharacterResponse:
    character = GetCharacterById(SQLModelCharacterRepository()).execute(id)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return CharacterResponse.from_domain(character)

@router.put("/characters/{id}")
def update_character(id: int, payload: CharacterPayload) -> CharacterResponse:
    character = UpdateCharacter(SQLModelCharacterRepository()).execute(
        UpdateCharacterCommand(
            id=id,
            name=payload.name,
            state=payload.state,
            img=payload.img
        )
    )
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return CharacterResponse.from_domain(character)

class DeleteResponse(BaseModel):
    message: str

@router.delete("/characters/{id}")
def delete_character(id: int) -> DeleteResponse:
    deleted = DeleteCharacter(SQLModelCharacterRepository()).execute(
        DeleteCharacterCommand(id=id)
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Character not found")
    return DeleteResponse(message="Character deleted successfully")
```

> 💬 El patrón se repite: **caso de uso devuelve `None`/`False` → FastAPI lanza 404**. Mantener este mapeo en una sola línea hace que la API sea predecible.

#### Tests de aplicación

Cada caso de uso tiene su propio test con un `FakeCharacterRepository` aislado:

```python
# test_update_character.py
def test_update_character_success(self) -> None:
    character_repository = FakeCharacterRepository()
    original = Character(
        name="Tanjiro Kamado",
        state="alive",
        img=CharacterImg(value="https://example.com/tanjiro.jpg")
    )
    character_repository.save(original)

    result = UpdateCharacter(character_repository).execute(
        UpdateCharacterCommand(
            id=1, name="Tanjiro Kamado", state="dead",
            img="https://example.com/tanjiro-v2.jpg"
        )
    )

    assert result is not None
    assert result.state() == "dead"

def test_update_character_not_found(self) -> None:
    result = UpdateCharacter(FakeCharacterRepository()).execute(
        UpdateCharacterCommand(id=999, name="X", state="alive", img="https://example.com/x.jpg")
    )
    assert result is None
```

```python
# test_delete_character.py
def test_delete_character_success(self) -> None:
    character_repository = FakeCharacterRepository()
    character_repository.save(Character(
        name="Tanjiro Kamado", state="alive",
        img=CharacterImg(value="https://example.com/tanjiro.jpg")
    ))
    result = DeleteCharacter(character_repository).execute(DeleteCharacterCommand(id=1))
    assert result is True

def test_delete_character_not_found(self) -> None:
    result = DeleteCharacter(FakeCharacterRepository()).execute(DeleteCharacterCommand(id=999))
    assert result is False
```

#### Tests de integración (HTTP)

```python
# test_character_endpoints.py
def test_get_character_by_id_returns_200():
    create = client.post("/characters/", json={
        "name": "Tanjiro Kamado", "state": "alive",
        "img": "https://example.com/tanjiro.jpg"
    })
    character_id = create.json()["id"]
    response = client.get(f"/characters/{character_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Tanjiro Kamado"

def test_get_character_by_id_not_found():
    response = client.get("/characters/999999")
    assert response.status_code == 404

def test_update_character_returns_200():
    create = client.post("/characters/", json={
        "name": "Tanjiro Kamado", "state": "alive",
        "img": "https://example.com/tanjiro.jpg"
    })
    character_id = create.json()["id"]
    response = client.put(f"/characters/{character_id}", json={
        "name": "Tanjiro Kamado", "state": "dead",
        "img": "https://example.com/tanjiro-v2.jpg"
    })
    assert response.status_code == 200
    assert response.json()["state"] == "dead"

def test_update_character_not_found():
    response = client.put("/characters/999999", json={
        "name": "Tanjiro Kamado", "state": "alive",
        "img": "https://example.com/tanjiro.jpg"
    })
    assert response.status_code == 404

def test_delete_character_returns_200():
    create = client.post("/characters/", json={
        "name": "Tanjiro Kamado", "state": "alive",
        "img": "https://example.com/tanjiro.jpg"
    })
    character_id = create.json()["id"]
    response = client.delete(f"/characters/{character_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Character deleted successfully"

def test_delete_character_not_found():
    response = client.delete("/characters/999999")
    assert response.status_code == 404
```

> 💬 Cada endpoint tiene un test **happy path** y otro **not found**. Es la matriz mínima que cubre tanto el éxito como el 404.

Resultado final:

```bash
pytest -v
# 19 passed
```

---

## 5. Resumen final del proyecto

### 5.1 Endpoints disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET    | `/` | Endpoint raíz de prueba |
| GET    | `/characters/` | Listar todos los personajes |
| GET    | `/characters/{id}` | Obtener un personaje por id |
| POST   | `/characters/` | Crear un personaje |
| PUT    | `/characters/{id}` | Actualizar un personaje |
| DELETE | `/characters/{id}` | Eliminar un personaje |

### 5.2 Ejemplo de uso

**Crear un personaje (Tanjiro):**

```bash
curl -X POST http://127.0.0.1:8000/characters/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tanjiro Kamado",
    "state": "alive",
    "img": "https://example.com/tanjiro.jpg"
  }'
```

Respuesta:

```json
{
  "id": 1,
  "name": "Tanjiro Kamado",
  "state": "alive",
  "img": "https://example.com/tanjiro.jpg"
}
```

**Otros personajes de ejemplo:**

```json
{
  "name": "Nezuko Kamado",
  "state": "alive",
  "img": "https://example.com/nezuko.jpg"
}
```

```json
{
  "name": "Zenitsu Agatsuma",
  "state": "alive",
  "img": "https://example.com/zenitsu.jpg"
}
```

```json
{
  "name": "Rengoku Kyojuro",
  "state": "dead",
  "img": "https://example.com/rengoku.jpg"
}
```

**Listar todos los personajes:**

```bash
curl -X GET http://127.0.0.1:8000/characters/
```

Respuesta:

```json
[
  {
    "id": 1,
    "name": "Tanjiro Kamado",
    "state": "alive",
    "img": "https://example.com/tanjiro.jpg"
  }
]
```

**Obtener un personaje por id:**

```bash
curl -X GET http://127.0.0.1:8000/characters/1
```

Respuesta:

```json
{
  "id": 1,
  "name": "Tanjiro Kamado",
  "state": "alive",
  "img": "https://example.com/tanjiro.jpg"
}
```

Si el id no existe, devuelve `404 Not Found`:

```json
{ "detail": "Character not found" }
```

**Actualizar un personaje:**

```bash
curl -X PUT http://127.0.0.1:8000/characters/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tanjiro Kamado",
    "state": "dead",
    "img": "https://example.com/tanjiro-v2.jpg"
  }'
```

Respuesta:

```json
{
  "id": 1,
  "name": "Tanjiro Kamado",
  "state": "dead",
  "img": "https://example.com/tanjiro-v2.jpg"
}
```

> 💬 `PUT` reemplaza el recurso completo: hay que mandar **todos** los campos, no solo los que cambian.

**Eliminar un personaje:**

```bash
curl -X DELETE http://127.0.0.1:8000/characters/1
```

Respuesta:

```json
{ "message": "Character deleted successfully" }
```

### 5.3 Comandos útiles

```bash
# Arrancar el servidor
fastapi dev
fastapi dev --host 0.0.0.0 --port 8000

# Tests
pytest -v           # 19 tests
pytest -q           # modo silencioso

# Borrar la BD para empezar de cero
rm characters.db
```

### 5.4 Flujo de una petición (POST /characters/)

```
Cliente (curl / frontend)
        │
        ▼
  FastAPI Router  (api.py)
        │  JSON → Pydantic (CharacterPayload)
        ▼
  Caso de uso  (create_character.py)
        │  crea CharacterImg (valida) + Character
        ▼
  Repositorio  (SQLModelCharacterRepository)
        │  traduce a CharacterModel y hace INSERT
        ▼
   Base de datos  (characters.db)
        │
        ▼
  Response JSON
```

### 5.5 Las 4 capas en una imagen mental

| Capa | Pregunta que responde | Ejemplo |
|------|----------------------|---------|
| **Domain** | ¿Qué reglas de negocio tengo? | `Character`, `CharacterImg`, `CharacterImgNotValid` |
| **Application** | ¿Qué operaciones puedo hacer? | `CreateCharacter`, `GetAllCharacters` |
| **Infrastructure (repo)** | ¿Cómo lo guardo? | `SQLModelCharacterRepository` (SQLite) |
| **Infrastructure (api)** | ¿Cómo lo expongo? | `POST /characters/`, `GET /characters/{id}` |

---

## 6. Recursos Adicionales

- [Documentación oficial de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de SQLModel](https://sqlmodel.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [pytest](https://docs.pytest.org/)
- [Test-Driven Development (Kent Beck)](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Kimetsu no Yaiba – Wiki](https://kimetsu-no-yaiba.fandom.com/)

---

> 🗡️ *「心を込めて」* — Hecho con ❤️ para aprender FastAPI.
