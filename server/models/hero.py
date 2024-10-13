from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from models.hero_power import HeroPower


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-heropowers.hero',)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    super_name = Column(String, nullable=False)
    
    # Relationship mapping hero to powers
    heropowers = relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    # Association proxy to get powers through hero_power
    powers = association_proxy('heropowers', 'power')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "powers": [power.to_dict() for power in self.powers if power is not None] 
        }

def __repr__(self):
        return f"<Hero (id={self.id}, name={self.name}, super_name={self.super_name})>"