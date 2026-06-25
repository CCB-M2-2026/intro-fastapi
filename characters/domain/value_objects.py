from dataclasses import dataclass
import validators

from src.characters.domain.exception import CharacterImgNotValid
# Lo que nos hace el frozen es que nos permite crear una clase inmutable, lo que significa que una vez que se crea una instancia de la clase, no se puede modificar. Esto es útil para garantizar la integridad de los datos y evitar errores accidentales en el código.
# Lo que nos hace el kw_only es que nos permite crear una clase con argumentos de palabra clave, lo que significa que los argumentos deben ser pasados como palabras clave en lugar de posiciones. El kw_only es útil para mejorar la legibilidad del código y evitar errores accidentales al pasar argumentos en el orden incorrecto. Y funciona de la siguiente manera: si tenemos una clase con varios atributos, podemos crear una instancia de la clase pasando los argumentos como palabras clave, lo que nos permite especificar qué atributo estamos estableciendo y en qué orden. Esto hace que el código sea más legible y fácil de entender, especialmente cuando se trabaja con clases complejas con muchos atributos. Funciona en Python 3.10 y versiones posteriores, y es una característica útil para mejorar la calidad del código y reducir los errores accidentales.

@dataclass(frozen=True,kw_only=True)
class CharacterImg:
    value: str
    
    # el metodo __post_init__ es un metodo especial que se llama automaticamente despues de que se inicializa la instancia de la clase. Esto nos permite realizar validaciones o transformaciones en los atributos de la clase despues de que se han establecido.
    def __post_init__(self)->None:
        if not validators.url(self.value):
            raise CharacterImgNotValid