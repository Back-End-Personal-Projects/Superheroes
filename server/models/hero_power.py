from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from db import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    
    serialize_rules =('-hero.hero_powers', '-power.hero_powers',)

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    # hero_id = db.Column(db.Integer, ForeignKey('heroes.id', ondelete='CASCADE'), nullable=False)
    # power_id = db.Column(db.Integer, ForeignKey('powers.id', ondelete='CASCADE'), nullable=False)

    #Foreign key to store the hero id
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    #Foreign key to store the power id
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    #Relationship mapping to related hero
    hero = relationship('Hero', back_populates='heropowers')
   
    #Relationship mapping to related power
    power = relationship('Power', back_populates='heropowers')

    #Validation
    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak','Average']:
            raise ValueError("Strength must be one of:'Strong', 'Weak','Average'")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "strength": self.strength,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "hero": self.hero.to_dict(),
            "power": self.power.to_dict()
        }

    def __repr__(self):
        return f"<HeroPower (id={self.id}, strength={self.strength}, hero_id={self.hero_id}, power_id={self.power_id})>"