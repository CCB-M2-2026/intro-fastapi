import pytest
from sqlmodel import SQLModel, select, Session

from src.characters.domain.models import Character
from src.characters.domain.value_objects import CharacterImg
from src.characters.infraestructure.repositories import SQLModelCharacterRepository, engine, CharacterModel


class TestSQLModelCharacterRepository:
    #limpieza de la base de datos después de cada prueba para evitar que los datos de una prueba afecten a otra.
    #Este sistema de limpieza es propio de pytest
    @pytest.fixture(autouse=True)
    def cleanup_database(self):
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)
            
    def test_saves_character_to_database(self) -> None:
        #Arrange es el paso donde se preparan los datos y el entorno para las pruebas.
        repository = SQLModelCharacterRepository()
        #Act es el paso donde se ejecuta la funcionalidad que se está probando.
        saved = repository.save(Character(
            name="Tanjiro Kamado",
            state="alive",
            img=CharacterImg(value="https://example.com/tanjiro.jpg")
        ))
        #Assert es el paso donde se verifican los resultados de la prueba y se comparan con los resultados esperados.
        assert saved.id() is not None
        with Session(engine) as session:
            character = session.get(CharacterModel, saved.id())
            assert character is not None
            assert character.name == "Tanjiro Kamado"
            assert character.state == "alive"
            assert character.img == "https://example.com/tanjiro.jpg"

    def test_all_returns_all_characters(self) -> None:
        with Session(engine) as session:
            session.add(CharacterModel(
                name="Tanjiro Kamado",
                state="alive",
                img="https://example.com/tanjiro.jpg"
            ))
            session.commit()

        characters = SQLModelCharacterRepository().all()

        assert len(characters) == 1
        assert characters[0].name() == "Tanjiro Kamado"
        assert characters[0].state() == "alive"
        assert characters[0].img() == CharacterImg(value="https://example.com/tanjiro.jpg")