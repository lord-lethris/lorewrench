from sqlalchemy import Column, Integer, String
from .database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    bio = Column(String)

class CharacterRelationship(Base):
    __tablename__ = "character_relationships"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    related_character_id = Column(Integer, ForeignKey("characters.id"))
    relationship_type = Column(String)