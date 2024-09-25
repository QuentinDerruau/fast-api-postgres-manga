from sqlalchemy import Column, Integer, String, ForeignKey, Float
from database import Base
from auth import get_password_hash, verify_password
from sqlalchemy.orm import relationship

################################################################ Users ################################################################

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def set_password(self, password: str):
        self.hashed_password = get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)

################################################################ Manga ################################################################

class Manga(Base):
    __tablename__ = "manga"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    image = Column(String)

    characters = relationship("Character", back_populates="manga")
    devil_fruits = relationship("DevilFruit", back_populates="manga")
    weapons = relationship("Weapon", back_populates="manga")
    haki = relationship("Haki", back_populates="manga")
    boats = relationship("Boat", back_populates="manga")
    crews = relationship("Crew", back_populates="manga")
    islands = relationship("Island", back_populates="manga")
    regions = relationship("Region", back_populates="manga")
    ranks = relationship("Rank", back_populates="manga")

################################################################ Characters ################################################################

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    strength = Column(Float)
    devil_fruit_id = Column(Integer, ForeignKey('devil_fruits.id'))
    crew_id = Column(Integer, ForeignKey('crews.id'))
    haki_id = Column(Integer, ForeignKey('haki.id'))
    weapon_id = Column(Integer, ForeignKey('weapons.id'))
    rank_id = Column(Integer, ForeignKey('ranks.id'))
    island_id = Column(Integer, ForeignKey('islands.id'))
    region_id = Column(Integer, ForeignKey('regions.id'))
    manga_id = Column(Integer, ForeignKey('manga.id'))

    devil_fruit = relationship("DevilFruit", back_populates="characters")
    crew = relationship("Crew", back_populates="members")
    haki = relationship("Haki", back_populates="users")
    weapon = relationship("Weapon", back_populates="users")
    rank = relationship("Rank", back_populates="users")
    island = relationship("Island", back_populates="characters")
    region = relationship("Region", back_populates="characters")
    manga = relationship("Manga", back_populates="characters")

################################################################ Devil Fruits ################################################################

class DevilFruit(Base):
    __tablename__ = "devil_fruits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type_id = Column(Integer, ForeignKey('devil_fruit_types.id'))
    manga_id = Column(Integer, ForeignKey('manga.id'))

    type = relationship("DevilFruitType", back_populates="fruits")
    characters = relationship("Character", back_populates="devil_fruit")
    manga = relationship("Manga", back_populates="devil_fruits")

class DevilFruitType(Base):
    __tablename__ = "devil_fruit_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    fruits = relationship("DevilFruit", back_populates="type")

################################################################ Weapons ################################################################

class Weapon(Base):
    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    manga_id = Column(Integer, ForeignKey('manga.id'))

    users = relationship("Character", back_populates="weapon")
    manga = relationship("Manga", back_populates="weapons")

################################################################ Haki ################################################################

class Haki(Base):
    __tablename__ = "haki"

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey('haki_types.id'))
    name = Column(String, index=True)
    manga_id = Column(Integer, ForeignKey('manga.id'))

    type = relationship("HakiType", back_populates="haki")
    users = relationship("Character", back_populates="haki")
    manga = relationship("Manga", back_populates="haki")

class HakiType(Base):
    __tablename__ = "haki_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    haki = relationship("Haki", back_populates="type")

################################################################ Boats ################################################################

class Boat(Base):
    __tablename__ = "boats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    crew_id = Column(Integer, ForeignKey('crews.id'))
    manga_id = Column(Integer, ForeignKey('manga.id'))

    crew = relationship("Crew", back_populates="boats")
    manga = relationship("Manga", back_populates="boats")

################################################################ Crews ################################################################

class Crew(Base):
    __tablename__ = "crews"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    flag = Column(String)
    manga_id = Column(Integer, ForeignKey('manga.id'))

    boats = relationship("Boat", back_populates="crew")
    members = relationship("Character", back_populates="crew")
    manga = relationship("Manga", back_populates="crews")

################################################################ Islands ################################################################

class Island(Base):
    __tablename__ = "islands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    region_id = Column(Integer, ForeignKey('regions.id'))
    manga_id = Column(Integer, ForeignKey('manga.id'))

    region = relationship("Region", back_populates="islands")
    characters = relationship("Character", back_populates="island")
    manga = relationship("Manga", back_populates="islands")

################################################################ Regions ################################################################

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    manga_id = Column(Integer, ForeignKey('manga.id'))

    islands = relationship("Island", back_populates="region")
    characters = relationship("Character", back_populates="region")
    manga = relationship("Manga", back_populates="regions")

################################################################ Ranks ################################################################

class Rank(Base):
    __tablename__ = "ranks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    manga_id = Column(Integer, ForeignKey('manga.id'))

    users = relationship("Character", back_populates="rank")
    manga = relationship("Manga", back_populates="ranks")