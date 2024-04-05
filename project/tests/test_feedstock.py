import pytest
from flask_sqlalchemy import SQLAlchemy
from project.models import db, Feedstock
from project.db_operation_feedstock import search_feedstock_in_database, add_feedstock_to_database, get_all_feedstock_from_database, delete_feedstock_from_database, update_feedstock_in_database

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

def test_search_feedstock_in_database(app):
    with app.app_context():
        add_feedstock_to_database('Seeds', 100, 'kg')
        add_feedstock_to_database('Fertilizer', 50, 'lbs')
        add_feedstock_to_database('Water', 200, 'liters')

        results = search_feedstock_in_database('Seed')
        assert len(results) == 1
        assert results[0]['category'] == 'Seeds'

        empty_results = search_feedstock_in_database('UnknownItem')
        assert len(empty_results) == 0

def test_add_feedstock_to_database(app):
    with app.app_context():
        add_feedstock_to_database('Seeds', 100, 'kg')
        feedstock_item = Feedstock.query.first()
        assert feedstock_item.category == 'Seeds'
        assert feedstock_item.quantity == 100
        assert feedstock_item.unit == 'kg'

def test_get_all_feedstock_from_database(app):
    with app.app_context():
        add_feedstock_to_database('Seeds', 100, 'kg')
        add_feedstock_to_database('Fertilizer', 50, 'lbs')
        add_feedstock_to_database('Water', 200, 'liters')

        feedstock_items = get_all_feedstock_from_database()
        assert len(feedstock_items) == 3
        assert feedstock_items[0]['category'] == 'Seeds'
        assert feedstock_items[1]['category'] == 'Fertilizer'
        assert feedstock_items[2]['category'] == 'Water'

def test_delete_feedstock_from_database(app):
    with app.app_context():
        add_feedstock_to_database('Seeds', 100, 'kg')
        feedstock_item = Feedstock.query.first()

        assert delete_feedstock_from_database(feedstock_item.id) == True
        assert delete_feedstock_from_database(999) == False

def test_update_feedstock_in_database(app):
    with app.app_context():
        add_feedstock_to_database('Seeds', 100, 'kg')
        feedstock_item = Feedstock.query.first()

        update_feedstock_in_database(feedstock_item.id, 'NewSeeds', 50, 'lbs')
        updated_feedstock_item = Feedstock.query.first()

        assert updated_feedstock_item.category == 'NewSeeds'
        assert updated_feedstock_item.quantity == 50
        assert updated_feedstock_item.unit == 'lbs'
