from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from db import db
from sqlalchemy_serializer import SerializerMixin

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    
    serialize_rules =('-hero.hero_powers', '-power.hero_powers',)

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    

    #Foreign key to store the hero id
    hero_id = db.Column(db.Integer, ForeignKey('heroes.id', ondelete='CASCADE'), nullable=False)
    #Foreign key to store the power id
    power_id = db.Column(db.Integer, ForeignKey('powers.id', ondelete='CASCADE'), nullable=False)

    #Relationship mapping to related hero
    hero = relationship('Hero', back_populates='hero_powers')
   
    #Relationship mapping to related power
    power = relationship('Power', back_populates='hero_powers')

 # Validation
    @validates('strength')
    def validate_strength(self, key, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError(f"Strength must be one of: {', '.join(valid_strengths)}")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "strength": self.strength,
            "hero": {
                "id": self.hero.id,
                "name": self.hero.name,
                "super_name": self.hero.super_name
            } if self.hero else None,
            "power": {
                "id": self.power.id,
                "name": self.power.name,
                "description": self.power.description
            } if self.power else None
        }

    def __repr__(self):
        return (f"<HeroPower (id={self.id}, "
                f"strength={self.strength}, "
                f"hero_id={self.hero_id}, "
                f"power_id={self.power_id}, "
                f"hero_name={self.hero.name if self.hero else 'None'}, "
                f"power_name={self.power.name if self.power else 'None'})>")
    