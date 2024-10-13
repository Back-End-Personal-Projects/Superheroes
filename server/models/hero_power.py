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
    hero = relationship('Hero', back_populates='heropowers')
   
    #Relationship mapping to related power
    power = relationship('Power', back_populates='heropowers')

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
            "strength": self.strength,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "hero": self.hero.to_dict() if self.hero else None,
            "power": self.power.to_dict() if self.power else None
        }

    def __repr__(self):
        return f"<HeroPower (id={self.id},strength={self.strength},hero_id={self.hero_id},power_id={self.power_id})>"