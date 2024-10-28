from flask import Flask, jsonify, request, make_response
#from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models.hero import Hero
from models.power import Power
from models.hero_power import HeroPower
from flask import jsonify
from db import db

# Create Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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

    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    Hero_dict = hero.to_dict()

    response = make_response(Hero_dict,200)

    return response

#Create new hero
@app.route('/heroes', methods=['POST'])
def create_episode():
    data = request.get_json()

    if not all(key in data for key in ('name', 'super_name')):
        return jsonify({"error": "Missing required fields: name, super_name"}), 400

    new_hero = Hero(
        name=data['name'],
        super_name=data['super_name']
    )
    
    db.session.add(new_hero)
    db.session.commit()

    return jsonify(new_hero.to_dict()), 201

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

# Update hero (PATCH)
@app.route('/heroes/<int:id>', methods=['PATCH'])
def patch_heroes(id):
    hero = Hero.query.get_or_404(id)  

    data = request.get_json()  

    if 'name' in data:
        hero.name = data['name']
    if 'super_name' in data:
        hero.super_name = data['super_name']

    db.session.commit()  
    return jsonify(hero.to_dict()), 200 

# Delete a hero
@app.route('/heroes/<int:id>', methods=['DELETE'])
def delete_hero(id):
    hero = Hero.query.get_or_404(id)  

    db.session.delete(hero)  
    db.session.commit()  

    return jsonify({"message": "Hero deleted successfully."}), 200 


#Powers
# Get all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = []
    for power in Power.query.all():
        power_dict = power.to_dict()
        powers.append(power_dict)

    response = jsonify(powers),200

    return response

#Get power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def powers_by_id(id):
    power = Power.query.filter(Power.id == id).first()
    
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    Power_dict = power.to_dict()

    response = make_response(Power_dict,200)

    return response

#Create new power
@app.route('/powers', methods=['POST'])
def create_power():
    data = request.get_json()
    new_power = Power(
        name=data['name'],
        description=data['description']
    )
    
    db.session.add(new_power)
    db.session.commit()

    return jsonify(new_power.to_dict()), 201

#Update powers
@app.route('/powers/<int:id>', methods=['PUT'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    power.name = data.get('name', power.name)
    power.description = data.get('description', power.description)
    db.session.commit()
    return jsonify(power.to_dict()), 200

# Update powers (PATCH)
@app.route('/powers/<int:id>', methods=['PATCH'])
def patch_power(id):
    power = Power.query.get_or_404(id)  

    data = request.get_json()  

    if 'name' in data:
        power.name = data['name']
    if 'description' in data:
        power.description = data['description']

    db.session.commit()  
    return jsonify(power.to_dict()), 200 

# Delete a power
@app.route('/powers/<int:id>', methods=['DELETE'])
def delete_power(id):
    power = Power.query.get_or_404(id)  

    db.session.delete(power)  
    db.session.commit()  

    return jsonify({"message": "Power deleted successfully."}), 200
#HeroPowers
# Get all Heropowers
@app.route('/hero_powers', methods=['GET'])
def get_hero_powers():
    hero_powers = [hero_power.to_dict() for hero_power in HeroPower.query.all()]
    return jsonify(hero_powers), 200

#Get heropowers by ID
@app.route('/hero_powers/<int:id>', methods=['GET'])
def hero_powers_by_id(id):
    hero_power = HeroPower.query.filter(HeroPower.id == id).first()
    
    if not hero_power:
        return jsonify({"error": "Heropower not found"}), 404
   
    hero_power_dict = hero_power.to_dict()

    response = make_response(hero_power_dict,200)

    return response

#Create hero_power
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    if not all(key in data for key in ('strength', 'hero_id', 'power_id')):
        return jsonify({"error": "Missing required fields: strength, hero_id, power_id"}), 400
    
    # Check if hero_id and power_id exist
    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])
    if not hero:
        return jsonify({"error": "Hero with this ID does not exist."}), 400
    if not power:
        return jsonify({"error": "Power with this ID does not exist."}), 400

    new_hero_power = HeroPower(

        hero_id=data['hero_id'],
        power_id=data['power_id'],
        strength=data['strength']
    )

    try:
        db.session.add(new_hero_power)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify(new_hero_power.to_dict()), 201

#Update hero_power(PUT)
@app.route('/hero_powers/<int:id>', methods=['PUT'])
def update_hero_power(id):
    hero_power = HeroPower.query.get(id)

    if not hero_power:
        return jsonify({"error": "Hero power not found"}), 404
   
    data = request.get_json()
    
    hero_power.hero_id = data.get('hero_id', hero_power.hero_id)
    hero_power.power_id = data.get('power_id', hero_power.power_id)
    
    db.session.commit()
    return jsonify(hero_power.to_dict()), 200

# Update hero_power (PATCH)
@app.route('/hero_powers/<int:id>', methods=['PATCH'])
def patch_hero_power(id):
    hero_power = HeroPower.query.get_or_404(id)  

    data = request.get_json()  

    if 'strength' in data:
        hero_power.strength = data['strength']  

    if 'hero_id' in data:
        hero_power.hero_id = data['hero_id']
    if 'power_id' in data:
        hero_power.power_id = data['power_id']

    db.session.commit()  
    return jsonify(hero_power.to_dict()), 200 

# Delete a hero_power
@app.route('/hero_powers/<int:id>', methods=['DELETE'])
def delete_hero_power(id):
    hero_power = HeroPower.query.get_or_404(id)  

    db.session.delete(hero_power)  
    db.session.commit()  

    return jsonify({"message": "Hero_power deleted successfully."}), 200  


if __name__ == '__main__':
    app.run(port=5555, debug=True)
