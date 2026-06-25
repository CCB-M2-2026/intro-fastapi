from sqlmodel import SQLModel, Field, create_engine, Session, select
from src.characters.domain.valid_object import CharacterImg
from src.characters.domain.models import Character
from src.characters.domain.repository import CharacterRepository


class CharacterModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
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
