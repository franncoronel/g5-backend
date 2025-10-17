"""
* Ejecutar con: python3 -m src.database.entidades
"""
from sqlalchemy import create_engine
from datetime import date
from enum import Enum
from typing import List
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session
)

motor = create_engine("sqlite+pysqlite:///:memory:", echo=True) # El motor de la base de datos se define programáticamente, en este caso es una instancia de mysqlite en memoria
class Base(DeclarativeBase): # Todas las tablas definidas como clases heredan de la clase Base
    pass

class TipoTitulo(Enum):
    PELICULA = "pelicula"

class Titulo(Base):
    __tablename__ = "titulo" # Para todas las tablas se define un nombre de tabla al cual referenciamos al, por ejemplo, definir claves foráneas

    id: Mapped[str] = mapped_column(primary_key=True) # El tipo Mapped[tipo] asocia un tipo de datos de Python con su análogo en el motor de base de datos, aunque no siempre se logra hacer un mapeo directo
    tipo: Mapped[TipoTitulo]
    titulo: Mapped[str]
    duracion: Mapped[int]
    sinopsis: Mapped[str]
    fecha_estreno: Mapped[date]

    puntajes: Mapped[List["Puntaje"]] = relationship( # Con relationship definimos la relación entre dos tablas, como es el caso de esta relación uno a muchos
        back_populates="pelicula",
        cascade="all,delete-orphan"
        )
    def __repr__(self):
        return f"Titulo(id={self.id}, tipo={self.tipo}, titulo={self.titulo!r}, duracion={self.duracion}, fecha_estreno={self.fecha_estreno})"

class Genero(Base):
    __tablename__ = "genero"

    id: Mapped[str] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    def __repr__(self):
        return f"Genero(id={self.id}, nombre={self.nombre!r})"

class Titulo_Genero(Base):
    __tablename__ = "titulo_genero"

    id_titulo: Mapped[str] = mapped_column(ForeignKey("titulo.id"), primary_key=True)
    id_genero: Mapped[str] = mapped_column(ForeignKey("genero.id"), primary_key=True)

    def __repr__(self):
        return f"Titulo_Genero(id_titulo={self.id_titulo}, id_genero={self.id_genero})"

class Puntaje(Base):
    __tablename__ = "puntaje"

    id: Mapped[str] = mapped_column(primary_key=True)
    id_titulo: Mapped[str] = mapped_column(ForeignKey("titulo.id")) # Al instanciar ForeignKey se pasa el nombre de la tabla, no de la clase, para relacionar las tablas.
    promedio: Mapped[float]
    cantidad_votos: Mapped[int]
    pelicula: Mapped["Titulo"] = relationship(back_populates="puntajes")

    def __repr__(self):
        return f"Puntaje(id={self.id}, id_titulo={self.id_titulo}, promedio={self.promedio}, cantidad_votos={self.cantidad_votos})"
class Persona(Base):
    __tablename__ = "persona"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre: Mapped[str]

    def __repr__(self):
        return f"Persona(id={self.id}, nombre={self.nombre!r})"

class Profesion_Titulo(Base): # También podría ser Director_Titulo, depende de las profesiones que conservemos
    __tablename__ = "profesion_titulo"

    id_titulo: Mapped[str] = mapped_column(ForeignKey("titulo.id"), primary_key=True)
    id_persona: Mapped[str] = mapped_column(ForeignKey("persona.id"), primary_key=True)
    id_profesion: Mapped[str] = mapped_column(ForeignKey("profesion.id"))

    def __repr__(self):
        return f"Profesion_Titulo(id_titulo={self.id_titulo}, id_persona={self.id_persona}, id_profesion={self.id_profesion})"

class Actor_Titulo(Base):
    __tablename__ = "actor_titulo"

    id_titulo: Mapped[str] = mapped_column(ForeignKey("titulo.id"), primary_key=True)
    id_actor: Mapped[str] = mapped_column(ForeignKey("persona.id"), primary_key=True)
    nombre_personaje: Mapped[str]

    def __repr__(self):
        return f"Actor_Titulo(id_titulo={self.id_titulo}, id_actor={self.id_actor}, nombre_personaje={self.nombre_personaje!r})"

class Profesion(Base):
    __tablename__ = "profesion"

    id: Mapped[str] = mapped_column(primary_key=True)

    def __repr__(self):
        return f"Profesion(id={self.id})"

def crear_tablas() -> None:
    Base.metadata.create_all(motor) # Con esta línea podemos crear TODAS las tablas que hereden de Base
    
    persona_nueva = Persona(nombre="John Cassavettes") # Agrego un registro para probar el insert
    
    """
        La Session establece una "conversación" con la base de datos. Dentro de una sesión podemos realizar distintas consultas y confirmarlas con session.commit().
        Es importante usar la sentencia with para que esta conexión con la base de datos se caiga al terminar de realizar operaciones
    """
    with Session(motor) as session: 
        session.add(persona_nueva)
        session.commit()
        print(session.scalars(select(Persona).all()))

if __name__ == "__main__":
    crear_tablas()