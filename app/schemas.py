from pydantic import BaseModel
from typing import Optional

################################################################ Users ################################################################

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

################################################################ Manga ################################################################

class MangaBase(BaseModel):
    name: str
    image: str

class MangaCreate(MangaBase):
    pass

class MangaUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None

class MangaOut(MangaBase):
    id: int

    class Config:
        from_attributes = True

################################################################ Characters ################################################################

class CharacterBase(BaseModel):
    name: str
    strength: Optional[int]

class CharacterCreate(CharacterBase):
    devil_fruit_id: Optional[int]
    crew_id: Optional[int]
    haki_id: Optional[int]
    weapon_id: Optional[int]
    rank_id: Optional[int]
    island_id: Optional[int]
    region_id: Optional[int]

class CharacterOut(CharacterBase):
    id: int

    class Config:
        orm_mode = True

################################################################ Devil Fruits ################################################################

class DevilFruitBase(BaseModel):
    name: str

class DevilFruitCreate(DevilFruitBase):
    type_id: int

class DevilFruitOut(DevilFruitBase):
    id: int
    type: str

    class Config:
        orm_mode = True

class DevilFruitTypeBase(BaseModel):
    name: str

class DevilFruitTypeCreate(DevilFruitTypeBase):
    pass

class DevilFruitTypeOut(DevilFruitTypeBase):
    id: int

    class Config:
        orm_mode = True

################################################################ Weapons ################################################################

class WeaponBase(BaseModel):
    name: str

class WeaponCreate(WeaponBase):
    pass

class WeaponOut(WeaponBase):
    id: int

    class Config:
        orm_mode = True

################################################################ Haki ################################################################

class HakiBase(BaseModel):
    name: str
    type_id: int

class HakiCreate(HakiBase):
    pass

class HakiOut(HakiBase):
    id: int
    type: str

    class Config:
        orm_mode = True

class HakiTypeBase(BaseModel):
    name: str

class HakiTypeCreate(HakiTypeBase):
    pass

class HakiTypeOut(HakiTypeBase):
    id: int

    class Config:
        orm_mode = True

################################################################ Boats ################################################################

class BoatBase(BaseModel):
    name: str

class BoatCreate(BoatBase):
    crew_id: int

class BoatOut(BoatBase):
    id: int
    crew: str

    class Config:
        orm_mode = True

################################################################ Crews ################################################################

class CrewBase(BaseModel):
    name: str
    flag: Optional[str] = None

class CrewCreate(CrewBase):
    pass

class CrewOut(CrewBase):
    id: int
    boats: list[BoatOut] = []
    members: list[CharacterOut] = []

    class Config:
        orm_mode = True

################################################################ Island ################################################################

class IslandBase(BaseModel):
    name: str

class IslandCreate(IslandBase):
    region_id: int

class IslandOut(IslandBase):
    id: int
    region: str

    class Config:
        orm_mode = True

################################################################ Region ################################################################

class RegionBase(BaseModel):
    name: str

class RegionCreate(RegionBase):
    pass

class RegionOut(RegionBase):
    id: int
    islands: list[IslandOut] = []

    class Config:
        orm_mode = True

################################################################ Rank ################################################################

class RankBase(BaseModel):
    name: str

class RankCreate(RankBase):
    pass

class RankOut(RankBase):
    id: int

    class Config:
        orm_mode = True