from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .database import SessionLocal, engine
from .models import Base, Character

from .models import CharacterRelationship

import requests

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (fine for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CharacterCreate(BaseModel):
    name: str
    bio: str

class GenerateRequest(BaseModel):
    drama: int
    tone: int

class SceneRequest(BaseModel):
    character1_id: int
    character2_id: int
    drama: int
    tone: int

@app.get("/")
def read_root():
    return {"message": "LoreWrench API running"}

@app.post("/character")
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    db_character = Character(name=character.name, bio=character.bio)
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

@app.get("/characters")
def get_characters(db: Session = Depends(get_db)):
    return db.query(Character).all()

class RelationshipCreate(BaseModel):
    character_id: int
    related_character_id: int
    relationship_type: str

@app.post("/relationship")
def create_relationship(rel: RelationshipCreate, db: Session = Depends(get_db)):
    relationship = CharacterRelationship(
        character_id=rel.character_id,
        related_character_id=rel.related_character_id,
        relationship_type=rel.relationship_type
    )
    db.add(relationship)
    db.commit()
    db.refresh(relationship)
    return relationship

@app.get("/relationships")
def get_relationships(db: Session = Depends(get_db)):
    return db.query(CharacterRelationship).all()

@app.post("/generate_character")
def generate_character(req: GenerateRequest):
    drama = req.drama
    tone = req.tone

    # Translate sliders into text
    drama_level = "low"
    if drama > 70:
        drama_level = "high"
    elif drama > 40:
        drama_level = "medium"

    tone_desc = "dark"
    if tone > 70:
        tone_desc = "light"
    elif tone > 40:
        tone_desc = "balanced"

    prompt = f"""
    Create a {tone_desc} {drama_level} drama fantasy character.

    Respond ONLY in this format:

    Name: <name>
    Bio: <short description>
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    text = data["response"]

    name = ""
    bio = ""

    for line in text.split("\n"):
        if line.lower().startswith("name:"):
            name = line.split(":", 1)[1].strip()
        if line.lower().startswith("bio:"):
            bio = line.split(":", 1)[1].strip()

    return {"name": name, "bio": bio}


@app.post("/generate_scene")
def generate_scene(req: SceneRequest, db: Session = Depends(get_db)):
    char1 = db.query(Character).filter(Character.id == req.character1_id).first()
    char2 = db.query(Character).filter(Character.id == req.character2_id).first()

    if not char1 or not char2:
        return {"scene": "Error: Characters not found"}

    # Get relationship (if exists)
    rels = db.query(CharacterRelationship).filter(
        CharacterRelationship.character_id == req.character1_id,
        CharacterRelationship.related_character_id == req.character2_id
    ).all()

    relationship_list = [r.relationship_type for r in rels]

    if relationship_list:
        relationship = ", ".join(relationship_list)
    else:
        relationship = "unknown relationship"









    # Translate sliders
    drama_level = "low"
    if req.drama > 70:
        drama_level = "high"
    elif req.drama > 40:
        drama_level = "medium"

    tone_desc = "dark"
    if req.tone > 70:
        tone_desc = "light"
    elif req.tone > 40:
        tone_desc = "balanced"

    prompt = f"""
    Write a {tone_desc}, {drama_level} drama scene in NOVEL format.

    DO NOT write a script or screenplay.

    Rules:
    - Use normal prose (like a book)
    - Use paragraphs
    - Include dialogue using quotation marks
    - DO NOT use character names followed by colons
    - DO NOT use stage directions like (this)

    Characters:

    Character 1:
    Name: {char1.name}
    Bio: {char1.bio}

    Character 2:
    Name: {char2.name}
    Bio: {char2.bio}

    Relationships: {relationship}

    These characters may have a complex or conflicting relationship. Reflect this in the scene.

    Write a short immersive scene.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    text = data.get("response", "")

    if not text:
        return {"scene": f"Error: {data}"}

    return {"scene": text}