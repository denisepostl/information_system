import pytest
from flask_sqlalchemy import SQLAlchemy
from project.models import db, Livestock
from project.db_operation_livestock import add_livestock_to_database, get_all_livestock_from_database, delete_livestock_from_database, update_livestock_in_database, search_livestock_in_database
from datetime import date

@pytest.fixture
def app():
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
    return app.test_client()

def test_add_livestock_to_database(app):
    with app.app_context():
        add_livestock_to_database('Tag123', 'Cow', date(2020, 1, 1), 'Female', None)
        animal = Livestock.query.first()
        assert animal.ear_tag == 'Tag123'
        assert animal.species == 'Cow'
        assert animal.birthday == date(2020, 1, 1)
        assert animal.gender == 'Female'
        assert animal.image_path is None

def test_get_all_livestock_from_database(app):
    with app.app_context():
        add_livestock_to_database('Tag1', 'Cow', date(2020, 1, 1), 'Female', None)
        add_livestock_to_database('Tag2', 'Sheep', date(2019, 1, 1), 'Male', None)
        add_livestock_to_database('Tag3', 'Chicken', date(2021, 1, 1), 'Female', None)

        livestock = get_all_livestock_from_database()
        assert len(livestock) == 3
        assert livestock[0]['ear_tag'] == 'Tag1'
        assert livestock[1]['ear_tag'] == 'Tag2'
        assert livestock[2]['ear_tag'] == 'Tag3'

def test_delete_livestock_from_database(app):
    with app.app_context():
        add_livestock_to_database('Tag123', 'Cow', date(2020, 1, 1), 'Female', None)
        animal = Livestock.query.first()
        assert delete_livestock_from_database(animal.id) == True
        assert delete_livestock_from_database(999) == False

def test_update_livestock_in_database(app):
    with app.app_context():
        add_livestock_to_database('Tag123', 'Cow', date(2020, 1, 1), 'Female', None)
        animal = Livestock.query.first()
        update_livestock_in_database(animal.id, 'NewTag', 'Sheep', date(2019, 1, 1), 'Male', None)
        assert animal.ear_tag == 'NewTag'
        assert animal.species == 'Sheep'
        assert animal.birthday == date(2019, 1, 1)
        assert animal.gender == 'Male'
        assert animal.image_path is None

def test_search_livestock_in_database(app):
    with app.app_context():
        add_livestock_to_database('Tag1', 'Cow', date(2020, 1, 1), 'Female', None)
        add_livestock_to_database('Tag2', 'Sheep', date(2019, 1, 1), 'Male', None)
        add_livestock_to_database('Tag3', 'Chicken', date(2021, 1, 1), 'Female', None)

        results = search_livestock_in_database('Tag')
        assert len(results) == 3
        assert results[0]['ear_tag'] == 'Tag1'
        assert results[1]['ear_tag'] == 'Tag2'
        assert results[2]['ear_tag'] == 'Tag3'
