# Superheroes
The Superheroes project is a web application that allows users to manage a database of superheroes and their associated powers. It utilizes Flask, SQLAlchemy, and SQLite to create a relational database and an API for interacting with the data.

# Features
1. Create, read, update, and delete superheroes.
2. Manage superhero powers and their descriptions.
3. Associate superheroes with multiple powers.
4. Validate data input for heroes and powers.

# Technologies Used
1. Flask: A lightweight WSGI web application framework.
2. SQLAlchemy: An ORM for handling database operations.
3. SQLite: A lightweight database for development and testing.
4. Flask-Migrate: A tool for handling SQLAlchemy database migrations.
5. SQLAlchemy-Serializer: For serializing model data to JSON format.
6. Association Proxy: To simplify relationships between models.

# Set Up
Run these commands to install the dependencies and set up the database:

- pipenv install
- pipenv shell
- cd server
- export FLASK_APP=app.py
- export FLASK_RUN_PORT=5555
- pip install Flask-Migrate
- pip install sqlalchemy-serializer
- pip install faker
- flask db init
- flask db migrate -m 'initial migration'
- flask db upgrade head
- python app.py
- python seed.py
- flask run

You can view the models in the server/models.py module, and the migrations in the server/migrations/versions directory.

# Testing with postman
GET /heroes: Retrieve a list of all superheroes.
POST /heroes: Create a new superhero.
GET /powers: Retrieve a list of all powers.
POST /powers: Create a new power.
GET /hero_power: Retrieve all hero-power associations.

The application will be accessible at http://127.0.0.1:5000.
