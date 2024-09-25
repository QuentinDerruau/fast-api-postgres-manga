from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError
from datetime import timedelta
from schemas import *
from database import engine, Base, get_db
import models
from models import *
from auth import create_access_token, verify_token, Token
from typing import List

app = FastAPI()

api_router = APIRouter(prefix="/fastapi")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(
    docs_url="/fastapi/docs",
    redoc_url="/fastapi/redoc",
    openapi_url="/fastapi/openapi.json"
)

################################################################ Auth Token ################################################################

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        username: str = payload.username
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

@api_router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.name}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/protected/")
def read_protected(current_user: str = Depends(get_current_user)):
    return {"message": "This is a protected endpoint", "user": current_user}

################################################################ Users ################################################################

@api_router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_user = User(name=user.name, email=user.email)
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

################################################################ Manga ################################################################

@api_router.post("/mangas/", response_model=MangaOut)
def create_manga(manga: MangaCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_manga = Manga(name=manga.name, image=manga.image)
    db.add(db_manga)
    db.commit()
    db.refresh(db_manga)
    return db_manga

@api_router.get("/mangas/", response_model=List[MangaOut])
def get_all_mangas(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    mangas = db.query(Manga).all()
    return mangas

@api_router.get("/mangas/{manga_id}", response_model=MangaOut)
def get_manga(manga_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_manga = db.query(Manga).filter(Manga.id == manga_id).first()
    if db_manga is None:
        raise HTTPException(status_code=404, detail="Manga not found")
    return db_manga

@api_router.patch("/mangas/{manga_id}", response_model=MangaOut)
def update_manga(manga_id: int, manga_update: MangaUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_manga = db.query(Manga).filter(Manga.id == manga_id).first()
    if db_manga is None:
        raise HTTPException(status_code=404, detail="Manga not found")
    
    if manga_update.name is not None:
        db_manga.name = manga_update.name
    if manga_update.image is not None:
        db_manga.image = manga_update.image
    
    db.add(db_manga)
    db.commit()
    db.refresh(db_manga)
    return db_manga

################################################################ Characters ################################################################

@api_router.post("/characters/", response_model=CharacterOut)
def create_character(character: CharacterCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_character = Character(name=character.name, lastName=character.lastName, strength=character.strength, manga_id=character.manga_id)
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

@api_router.get("/characters/", response_model=List[CharacterOut])
def read_characters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    characters = db.query(Character).offset(skip).limit(limit).all()
    return characters

@api_router.get("/characters/{character_id}", response_model=CharacterOut)
def read_character(character_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_character = db.query(Character).filter(Character.id == character_id).first()
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character

@api_router.put("/characters/{character_id}", response_model=CharacterOut)
def update_character(character_id: int, character: CharacterCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_character = db.query(Character).filter(Character.id == character_id).first()
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    
    db_character.name = character.name
    db_character.lastName = character.lastName
    db_character.strength = character.strength
    db_character.manga_id = character.manga_id
    db.commit()
    db.refresh(db_character)
    return db_character

@api_router.delete("/characters/{character_id}")
def delete_character(character_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_character = db.query(Character).filter(Character.id == character_id).first()
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    
    db.delete(db_character)
    db.commit()
    return {"detail": "Character deleted"}

################################################################ Devil Fruits ################################################################

@api_router.post("/devilfruits/", response_model=DevilFruitOut)
def create_devil_fruit(devil_fruit: DevilFruitCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_devil_fruit = DevilFruit(name=devil_fruit.name, category=devil_fruit.category, manga_id=devil_fruit.manga_id)
    db.add(db_devil_fruit)
    db.commit()
    db.refresh(db_devil_fruit)
    return db_devil_fruit

@api_router.get("/devilfruits/", response_model=List[DevilFruitOut])
def read_devil_fruits(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    devil_fruits = db.query(DevilFruit).offset(skip).limit(limit).all()
    return devil_fruits

@api_router.get("/devilfruits/{devil_fruit_id}", response_model=DevilFruitOut)
def read_devil_fruit(devil_fruit_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_devil_fruit = db.query(DevilFruit).filter(DevilFruit.id == devil_fruit_id).first()
    if db_devil_fruit is None:
        raise HTTPException(status_code=404, detail="Devil Fruit not found")
    return db_devil_fruit

@api_router.put("/devilfruits/{devil_fruit_id}", response_model=DevilFruitOut)
def update_devil_fruit(devil_fruit_id: int, devil_fruit: DevilFruitCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_devil_fruit = db.query(DevilFruit).filter(DevilFruit.id == devil_fruit_id).first()
    if db_devil_fruit is None:
        raise HTTPException(status_code=404, detail="Devil Fruit not found")
    
    db_devil_fruit.name = devil_fruit.name
    db_devil_fruit.category = devil_fruit.category
    db_devil_fruit.manga_id = devil_fruit.manga_id
    db.commit()
    db.refresh(db_devil_fruit)
    return db_devil_fruit

@api_router.delete("/devilfruits/{devil_fruit_id}")
def delete_devil_fruit(devil_fruit_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_devil_fruit = db.query(DevilFruit).filter(DevilFruit.id == devil_fruit_id).first()
    if db_devil_fruit is None:
        raise HTTPException(status_code=404, detail="Devil Fruit not found")
    
    db.delete(db_devil_fruit)
    db.commit()
    return {"detail": "Devil Fruit deleted"}

################################################################ Weapons ################################################################

@api_router.post("/weapons/", response_model=WeaponOut)
def create_weapon(weapon: WeaponCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_weapon = Weapon(name=weapon.name, manga_id=weapon.manga_id)
    db.add(db_weapon)
    db.commit()
    db.refresh(db_weapon)
    return db_weapon

@api_router.get("/weapons/", response_model=List[WeaponOut])
def read_weapons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    weapons = db.query(Weapon).offset(skip).limit(limit).all()
    return weapons

@api_router.get("/weapons/{weapon_id}", response_model=WeaponOut)
def read_weapon(weapon_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if db_weapon is None:
        raise HTTPException(status_code=404, detail="Weapon not found")
    return db_weapon

@api_router.put("/weapons/{weapon_id}", response_model=WeaponOut)
def update_weapon(weapon_id: int, weapon: WeaponCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if db_weapon is None:
        raise HTTPException(status_code=404, detail="Weapon not found")
    
    db_weapon.name = weapon.name
    db_weapon.manga_id = weapon.manga_id
    db.commit()
    db.refresh(db_weapon)
    return db_weapon

@api_router.delete("/weapons/{weapon_id}")
def delete_weapon(weapon_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if db_weapon is None:
        raise HTTPException(status_code=404, detail="Weapon not found")
    
    db.delete(db_weapon)
    db.commit()
    return {"detail": "Weapon deleted"}


################################################################ Haki ################################################################

@api_router.post("/haki/", response_model=HakiOut)
def create_haki(haki: HakiCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_haki = Haki(name=haki.name, manga_id=haki.manga_id)
    db.add(db_haki)
    db.commit()
    db.refresh(db_haki)
    return db_haki

@api_router.get("/haki/", response_model=List[HakiOut])
def read_hakis(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    hakis = db.query(Haki).offset(skip).limit(limit).all()
    return hakis

@api_router.get("/haki/{haki_id}", response_model=HakiOut)
def read_haki(haki_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_haki = db.query(Haki).filter(Haki.id == haki_id).first()
    if db_haki is None:
        raise HTTPException(status_code=404, detail="Haki not found")
    return db_haki

@api_router.put("/haki/{haki_id}", response_model=HakiOut)
def update_haki(haki_id: int, haki: HakiCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_haki = db.query(Haki).filter(Haki.id == haki_id).first()
    if db_haki is None:
        raise HTTPException(status_code=404, detail="Haki not found")
    
    db_haki.name = haki.name
    db_haki.manga_id = haki.manga_id
    db.commit()
    db.refresh(db_haki)
    return db_haki

@api_router.delete("/haki/{haki_id}")
def delete_haki(haki_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_haki = db.query(Haki).filter(Haki.id == haki_id).first()
    if db_haki is None:
        raise HTTPException(status_code=404, detail="Haki not found")
    
    db.delete(db_haki)
    db.commit()
    return {"detail": "Haki deleted"}


################################################################ Boats ################################################################

@api_router.post("/boats/", response_model=BoatOut)
def create_boat(boat: BoatCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_boat = Boat(name=boat.name, manga_id=boat.manga_id)
    db.add(db_boat)
    db.commit()
    db.refresh(db_boat)
    return db_boat

@api_router.get("/boats/", response_model=List[BoatOut])
def read_boats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    boats = db.query(Boat).offset(skip).limit(limit).all()
    return boats

@api_router.get("/boats/{boat_id}", response_model=BoatOut)
def read_boat(boat_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_boat = db.query(Boat).filter(Boat.id == boat_id).first()
    if db_boat is None:
        raise HTTPException(status_code=404, detail="Boat not found")
    return db_boat

@api_router.put("/boats/{boat_id}", response_model=BoatOut)
def update_boat(boat_id: int, boat: BoatCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_boat = db.query(Boat).filter(Boat.id == boat_id).first()
    if db_boat is None:
        raise HTTPException(status_code=404, detail="Boat not found")
    
    db_boat.name = boat.name
    db_boat.manga_id = boat.manga_id
    db.commit()
    db.refresh(db_boat)
    return db_boat

@api_router.delete("/boats/{boat_id}")
def delete_boat(boat_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_boat = db.query(Boat).filter(Boat.id == boat_id).first()
    if db_boat is None:
        raise HTTPException(status_code=404, detail="Boat not found")
    
    db.delete(db_boat)
    db.commit()
    return {"detail": "Boat deleted"}

################################################################ Rank ################################################################

@api_router.post("/ranks/", response_model=RankOut)
def create_rank(rank: RankCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_rank = Rank(name=rank.name, manga_id=rank.manga_id)
    db.add(db_rank)
    db.commit()
    db.refresh(db_rank)
    return db_rank

@api_router.get("/ranks/", response_model=List[RankOut])
def read_ranks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    ranks = db.query(Rank).offset(skip).limit(limit).all()
    return ranks

@api_router.get("/ranks/{rank_id}", response_model=RankOut)
def read_rank(rank_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_rank = db.query(Rank).filter(Rank.id == rank_id).first()
    if db_rank is None:
        raise HTTPException(status_code=404, detail="Rank not found")
    return db_rank

@api_router.put("/ranks/{rank_id}", response_model=RankOut)
def update_rank(rank_id: int, rank: RankCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_rank = db.query(Rank).filter(Rank.id == rank_id).first()
    if db_rank is None:
        raise HTTPException(status_code=404, detail="Rank not found")
    
    db_rank.name = rank.name
    db_rank.manga_id = rank.manga_id
    db.commit()
    db.refresh(db_rank)
    return db_rank

@api_router.delete("/ranks/{rank_id}")
def delete_rank(rank_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_rank = db.query(Rank).filter(Rank.id == rank_id).first()
    if db_rank is None:
        raise HTTPException(status_code=404, detail="Rank not found")
    
    db.delete(db_rank)
    db.commit()
    return {"detail": "Rank deleted"}


################################################################ Region ################################################################

@api_router.post("/regions/", response_model=RegionOut)
def create_region(region: RegionCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_region = Region(name=region.name, manga_id=region.manga_id)
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region

@api_router.get("/regions/", response_model=List[RegionOut])
def read_regions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    regions = db.query(Region).offset(skip).limit(limit).all()
    return regions

@api_router.get("/regions/{region_id}", response_model=RegionOut)
def read_region(region_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_region = db.query(Region).filter(Region.id == region_id).first()
    if db_region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return db_region

@api_router.put("/regions/{region_id}", response_model=RegionOut)
def update_region(region_id: int, region: RegionCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_region = db.query(Region).filter(Region.id == region_id).first()
    if db_region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    
    db_region.name = region.name
    db_region.manga_id = region.manga_id
    db.commit()
    db.refresh(db_region)
    return db_region

@api_router.delete("/regions/{region_id}")
def delete_region(region_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_region = db.query(Region).filter(Region.id == region_id).first()
    if db_region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    
    db.delete(db_region)
    db.commit()
    return {"detail": "Region deleted"}


################################################################ Island ################################################################

@api_router.post("/islands/", response_model=IslandOut)
def create_island(island: IslandCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_island = Island(name=island.name, manga_id=island.manga_id)
    db.add(db_island)
    db.commit()
    db.refresh(db_island)
    return db_island

@api_router.get("/islands/", response_model=List[IslandOut])
def read_islands(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    islands = db.query(Island).offset(skip).limit(limit).all()
    return islands

@api_router.get("/islands/{island_id}", response_model=IslandOut)
def read_island(island_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_island = db.query(Island).filter(Island.id == island_id).first()
    if db_island is None:
        raise HTTPException(status_code=404, detail="Island not found")
    return db_island

@api_router.put("/islands/{island_id}", response_model=IslandOut)
def update_island(island_id: int, island: IslandCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_island = db.query(Island).filter(Island.id == island_id).first()
    if db_island is None:
        raise HTTPException(status_code=404, detail="Island not found")
    
    db_island.name = island.name
    db_island.manga_id = island.manga_id
    db.commit()
    db.refresh(db_island)
    return db_island

@api_router.delete("/islands/{island_id}")
def delete_island(island_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_island = db.query(Island).filter(Island.id == island_id).first()
    if db_island is None:
        raise HTTPException(status_code=404, detail="Island not found")
    
    db.delete(db_island)
    db.commit()
    return {"detail": "Island deleted"}

################################################################ Crew ################################################################

@api_router.post("/crews/", response_model=CrewOut)
def create_crew(crew: CrewCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_crew = Crew(name=crew.name, manga_id=crew.manga_id)
    db.add(db_crew)
    db.commit()
    db.refresh(db_crew)
    return db_crew

@api_router.get("/crews/", response_model=List[CrewOut])
def read_crews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    crews = db.query(Crew).offset(skip).limit(limit).all()
    return crews

@api_router.get("/crews/{crew_id}", response_model=CrewOut)
def read_crew(crew_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_crew = db.query(Crew).filter(Crew.id == crew_id).first()
    if db_crew is None:
        raise HTTPException(status_code=404, detail="Crew not found")
    return db_crew

@api_router.put("/crews/{crew_id}", response_model=CrewOut)
def update_crew(crew_id: int, crew: CrewCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_crew = db.query(Crew).filter(Crew.id == crew_id).first()
    if db_crew is None:
        raise HTTPException(status_code=404, detail="Crew not found")
    
    db_crew.name = crew.name
    db_crew.manga_id = crew.manga_id
    db.commit()
    db.refresh(db_crew)
    return db_crew

@api_router.delete("/crews/{crew_id}")
def delete_crew(crew_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_crew = db.query(Crew).filter(Crew.id == crew_id).first()
    if db_crew is None:
        raise HTTPException(status_code=404, detail="Crew not found")
    
    db.delete(db_crew)
    db.commit()
    return {"detail": "Crew deleted"}


app.include_router(api_router)