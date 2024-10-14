from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from db import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from models.hero_power import HeroPower

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    
    serialize_rules =('-heropowers.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
   
    #Relationship mapping powers to heropowers 
    hero_powers = db.relationship('HeroPower', back_populates="power", cascade='all, delete-orphan')

    # Association proxy to get hero for this power through hero_power
    heroes = association_proxy('hero_powers', 'hero')

    #Validation
    @validates('description')
    def validate_description(self, key, value):
        if not value or len(value) < 20:
            raise ValueError("Description must be present and at least 20 characters long")
        return value
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    def __repr__(self):
        return f"<Power (id={self.id}, name={self.name}, description={self.description})>"