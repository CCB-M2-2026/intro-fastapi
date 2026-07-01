from sqlmodel import SQLModel, Field, create_engine, Session,select
from src.characters.domain.value_objects import CharacterImg
from src.characters.domain.models import Character
from src.characters.domain.repositories import CharacterRepository

class CharacterModel(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
        name: str
        state: str
        img: str

# el create_engine es una función que crea un motor de base de datos que se utiliza para conectarse a la base de datos. En este caso, se está creando un motor de base de datos SQLite que se conecta a un archivo llamado characters.db. Si el archivo no existe, se creará automáticamente.
engine = create_engine("sqlite:///characters.db")

SQLModel.metadata.create_all(engine)

class SQLModelCharacterRepository(CharacterRepository):
    # La diferencia que hay entre el repositorio de SQLModel y el repositorio de memoria es que el primero interactúa con una base de datos real, mientras que el segundo solo almacena los characters en memoria. Esto significa que el repositorio de SQLModel puede persistir los characters entre ejecuciones del programa, mientras que el repositorio de memoria no lo hace. Además, el repositorio de SQLModel puede manejar grandes cantidades de datos y realizar consultas complejas, mientras que el repositorio de memoria está limitado por la cantidad de memoria disponible y no puede realizar consultas complejas.
    def all(self)-> list[Character]:
        with Session(engine) as session:
            character_models= session.exec(select(CharacterModel)).all()
        return [
            Character(
                name=character_model.name,
                state=character_model.state,
                img=CharacterImg(value=character_model.img),
                id=character_model.id
            )
            for character_model in character_models
        ]

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

    def save(self, character: Character) -> Character:
        # el character_model es una instancia de la clase CharacterModel que se crea a partir del character que se está guardando en la base de datos. Se utiliza para mapear los atributos del character a los campos de la tabla de la base de datos. En este caso, se está creando un CharacterModel con los atributos name, state e img establecidos en los valores del character.
        character_model = CharacterModel(
            name=character.name(),
            state=character.state(),
            img=character.img().value
        )
        with Session(engine) as session:
            session.add(character_model)
            session.commit()
            session.refresh(character_model)
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
