import pytest
from flask_sqlalchemy import SQLAlchemy
from project.models import db, Harvest, Land
from project.db_operation_harvest import add_harvest_to_database, get_all_harvests_from_database, delete_harvest_from_database, update_harvest_in_database
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

def test_add_harvest_to_database(app):
    with app.app_context():
        land = Land(type='Farm', size=10.0, ownership='Private')
        db.session.add(land)
        db.session.commit()

        add_harvest_to_database('Tomatoes', 50, 'kg', date(2022, 1, 1), land.id)
        harvest = Harvest.query.first()
        assert harvest.crop == 'Tomatoes'
        assert harvest.quantity == 50
        assert harvest.unit == 'kg'
        assert harvest.date == date(2022, 1, 1)
        assert harvest.land.type == 'Farm'

def test_get_all_harvests_from_database(app):
    with app.app_context():
        land1 = Land(type='Farm', size=10.0, ownership='Private')
        land2 = Land(type='Garden', size=5.0, ownership='Public')
        db.session.add_all([land1, land2])
        db.session.commit()

        add_harvest_to_database('Apples', 30, 'lbs', date(2021, 12, 1), land1.id)
        add_harvest_to_database('Carrots', 20, 'lbs', date(2022, 2, 1), land2.id)

        harvests = get_all_harvests_from_database()
        assert len(harvests) == 2
        assert harvests[0]['crop'] == 'Apples'
        assert harvests[1]['crop'] == 'Carrots'

def test_delete_harvest_from_database(app):
    with app.app_context():
        land = Land(type='Farm', size=10.0, ownership='Private')
        db.session.add(land)
        db.session.commit()

        add_harvest_to_database('Oranges', 40, 'lbs', date(2022, 3, 1), land.id)
        harvest = Harvest.query.first()

        assert delete_harvest_from_database(harvest.id) == True
        assert delete_harvest_from_database(999) == False

def test_update_harvest_in_database(app):
    with app.app_context():
        land = Land(type='Farm', size=10.0, ownership='Private')
        db.session.add(land)
        db.session.commit()

        add_harvest_to_database('Grapes', 60, 'lbs', date(2022, 4, 1), land.id)
        harvest = Harvest.query.first()

        update_harvest_in_database(harvest.id, 'Berries', 25, 'kg', date(2022, 5, 1), land.id)
        updated_harvest = Harvest.query.first()

        assert updated_harvest.crop == 'Berries'
        assert updated_harvest.quantity == 25
        assert updated_harvest.unit == 'kg'
        assert updated_harvest.date == date(2022, 5, 1)
        assert updated_harvest.land.type == 'Farm'
