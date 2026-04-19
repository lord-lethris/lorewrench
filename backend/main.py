from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

characters = []

class Character(BaseModel):
    name: str
    bio: str

@app.get("/")
def read_root():
    return {"message": "LoreWrench API running"}

@app.post("/character")
def create_character(character: Character):
    characters.append(character)
    return {"message": "Character created", "character": character}

@app.get("/characters")
def get_characters():
    return characters