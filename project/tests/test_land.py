import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project.models import db, Person, Address, Land
from project.db_operation_land import add_land_to_database, delete_land_from_database, get_land_details_from_database, edit_land_in_database, search_lands_in_database

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_add_land_to_database(app, client):
    with app.app_context():
        form_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'phoneNumber': '123456789',
            'addressStreet': '123 Main St',
            'addressCity': 'City',
            'addressState': 'State',
            'addressZipCode': '12345'
        }

        add_land_to_database('Type', 100, 'gepachtet', 'unit', form_data)

        land = Land.query.first()
        person = Person.query.first()
        address = Address.query.first()

        assert land is not None
        assert person is not None
        assert address is not None
        assert land.type == 'Type'
        assert land.size == 100
        assert land.ownership == 'gepachtet'
        assert person.first_name == 'John'
        assert person.last_name == 'Doe'
        assert person.phone_number == '123456789'
        assert address.street == '123 Main St'
        assert address.city == 'City'
        assert address.state == 'State'
        assert address.zip_code == '12345'

def test_delete_land_from_database(app, client):
    with app.app_context():
        land = Land(type='Type', size=100, ownership='gepachtet', unit='unit')
        db.session.add(land)
        db.session.commit()

        land_id = land.id
        delete_land_from_database(land_id)

        assert Land.query.get(land_id) is None

def test_get_land_details_from_database(app, client):
    with app.app_context():
        land = Land(type='Type', size=100, ownership='gepachtet', unit='unit')
        db.session.add(land)
        db.session.commit()

        land_id = land.id
        details = get_land_details_from_database(land_id)

        assert details is not None
        assert details['type'] == 'Type'
        assert details['size'] == 100
        assert details['ownership'] == 'gepachtet'

def test_edit_land_in_database(app, client):
    with app.app_context():
        land = Land(type='Type', size=100, ownership='gepachtet', unit='unit')
        db.session.add(land)
        db.session.commit()

        land_id = land.id
        form_data = {
            'editType': 'NewType',
            'editSize': 200,
            'editOwnership': 'eigenbesitz',
            'editUnit': 'newUnit',
            'editFirstName': 'NewFirst',
            'editLastName': 'NewLast',
            'editPhoneNumber': '987654321',
            'editAddressStreet': '456 New St',
            'editAddressCity': 'New City',
            'editAddressState': 'New State',
            'editAddressZipCode': '54321'
        }

        edited_land = edit_land_in_database(land_id, form_data)

        assert edited_land is not None
        assert edited_land.type == 'NewType'
        assert edited_land.size == 200
        assert edited_land.ownership == 'eigenbesitz'
        assert edited_land.unit == 'newUnit'

def test_search_lands_in_database(app, client):
    with app.app_context():
        land1 = Land(type='Type1', size=100, ownership='gepachtet', unit='unit1')
        land2 = Land(type='Type2', size=200, ownership='gepachtet', unit='unit2')
        land3 = Land(type='Type3', size=300, ownership='eigenbesitz', unit='unit3')

        db.session.add_all([land1, land2, land3])
        db.session.commit()

        owned_lands = search_lands_in_database('eigenbesitz')
        leased_lands = search_lands_in_database('gepachtet')

        assert len(owned_lands) == 1
        assert len(leased_lands) == 2
