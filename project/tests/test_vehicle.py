import pytest
from flask_sqlalchemy import SQLAlchemy
from project.models import db, Vehicle
from project.db_operation_vehicle import add_vehicle_to_db, get_all_vehicles, delete_vehicle_by_id, update_vehicle_in_database, search_vehicles_in_database, is_valid_year

@pytest.fixture
def app():
    """
    Create a Flask application instance for testing.

    Returns:
    - Flask: The Flask application instance.
    """
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture
def client(app):
    """
    Create a test client for the Flask application.

    Parameters:
    - app (Flask): The Flask application instance.

    Returns:
    - FlaskClient: The test client for the Flask application.
    """
    return app.test_client()

def test_add_vehicle_to_db(app):
    """
    Test adding a vehicle entry to the database.

    Parameters:
    - app (Flask): The Flask application instance.
    """
    with app.app_context():
        add_vehicle_to_db('Toyota', 'Camry', 2022, 'test_image.jpg')
        vehicle = Vehicle.query.first()
        assert vehicle.brand == 'Toyota'
        assert vehicle.model == 'Camry'
        assert vehicle.year == 2022
        assert vehicle.image_path == 'test_image.jpg'

def test_get_all_vehicles(app):
    """
    Test retrieving all vehicle entries from the database.

    Parameters:
    - app (Flask): The Flask application instance.
    """
    with app.app_context():
        add_vehicle_to_db('Toyota', 'Camry', 2022, 'test_image.jpg')
        add_vehicle_to_db('Honda', 'Civic', 2021, 'another_image.jpg')
        vehicles = get_all_vehicles()
        assert len(vehicles) == 2
        assert vehicles[0]['brand'] == 'Toyota'
        assert vehicles[1]['brand'] == 'Honda'

def test_delete_vehicle_by_id(app):
    """
    Test deleting a vehicle entry from the database by its ID.

    Parameters:
    - app (Flask): The Flask application instance.
    """
    with app.app_context():
        add_vehicle_to_db('Toyota', 'Camry', 2022, 'test_image.jpg')
        vehicle = Vehicle.query.first()
        assert delete_vehicle_by_id(vehicle.id) == True
        assert delete_vehicle_by_id(999) == False

def test_update_vehicle_in_database(app):
    """
    Test updating a vehicle entry in the database.

    Parameters:
    - app (Flask): The Flask application instance.
    """
    with app.app_context():
        add_vehicle_to_db('Toyota', 'Camry', 2022, 'test_image.jpg')
        vehicle = Vehicle.query.first()
        update_vehicle_in_database(vehicle, 'Ford', 'Fusion', 2023, None)
        assert vehicle.brand == 'Ford'
        assert vehicle.model == 'Fusion'
        assert vehicle.year == 2023

def test_search_vehicles_in_database(app):
    """
    Test searching for vehicle entries in the database.

    Parameters:
    - app (Flask): The Flask application instance.
    """
    with app.app_context():
        add_vehicle_to_db('Toyota', 'Camry', 2022, 'test_image.jpg')
        add_vehicle_to_db('Honda', 'Civic', 2021, 'another_image.jpg')
        results = search_vehicles_in_database('Toy')
        assert len(results) == 1
        assert results[0]['brand'] == 'Toyota'

def test_valid_year():
    """
    Test checking if a given year string is valid.

    Returns:
    - bool: True if the year string is valid, False otherwise.
    """
    assert is_valid_year("2022") == True
    assert is_valid_year("1000") == True
    assert is_valid_year("9999") == True

def test_invalid_year():
    """
    Test checking if a given year string is invalid.

    Returns:
    - bool: True if the year string is invalid, False otherwise.
    """
    assert is_valid_year("abc") == False
    assert is_valid_year("10000") == False
    assert is_valid_year("999") == False
    assert is_valid_year("") == False
    assert is_valid_year(" ") == False