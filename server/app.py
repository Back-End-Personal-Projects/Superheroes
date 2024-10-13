from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models.hero import Hero
from models.power import Power
from models.hero_power import HeroPower
from flask import jsonify
from db import db

# Create Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Welcome to the Superheroes API!"

#Building the API
#Heroes
# Get all heroes
@app.route('/heroes', methods=['GET'])
def heroes():
    heroes = []
    for hero in Hero.query.all():
        hero_dict = hero.to_dict()
        heroes.append(hero_dict)

    response = jsonify(heroes),200

    return response

#Get hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def heroes_by_id(id):
    hero = Hero.query.filter(Hero.id == id).first()

    Hero_dict = hero.to_dict()

    response = make_response(Hero_dict,200)

    return response

#Update hero
@app.route('/heroes/<int:id>', methods=['PUT'])
def update_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    data = request.get_json()
    hero.name = data.get('name', hero.name)
    hero.super_name = data.get('super_name', hero.super_name)
    db.session.commit()
    return jsonify(hero.to_dict()), 200

#Powers
@app.route('/powers', methods=['GET', 'POST'])
def powers():
    if request.method == 'GET':
        powers = []
        for power in Power.query.all():
            power_dict = power.to_dict()
            powers.append(power_dict)

        response = jsonify(powers),200

        return response

    elif request.method == 'POST':
        new_power = Power(
            power_id=request.form.get("id"),
            name=request.form.get("name"),
            description=request.form.get("description"),
            
        )

        db.session.add(new_power)
        db.session.commit()

        power_dict = new_power.to_dict()

        response = make_response(power_dict,201)

        return response
    
#Get, Update, Delete power by id
@app.route('/powers/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def get_power_by_id(id):
    power = Power.query.filter(Power.id == id).first()
    
    if power == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response

    else:
        if request.method == 'GET':
            power_dict = power.to_dict()

            response = make_response(power_dict,200)

            return response

        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(power, attr, request.form.get(attr))

            db.session.add(power)
            db.session.commit()

            power_dict = power.to_dict()

            response = make_response(
                power_dict,200)

            return response

        elif request.method == 'DELETE':
            db.session.delete(power)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Power deleted."
            }

            response = make_response(response_body,200)

            return response

#Create hero power
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    new_hero_power = HeroPower(
        strength=data['strength'],
        hero_id=data['hero_id'],
        power_id=data['power_id']
    )
    db.session.add(new_hero_power)
    db.session.commit()
    return jsonify(new_hero_power.to_dict()), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
