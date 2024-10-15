from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from models.hero_power import HeroPower


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-heropowers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(String, nullable=False)
    
    # Relationship mapping hero to powers
    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    # Association proxy to get powers through hero_power
    powers = association_proxy('hero_powers', 'power')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
        }


def __repr__(self):
    return f"<Hero (id={self.id}, name={self.name}, super_name={self.super_name})>"