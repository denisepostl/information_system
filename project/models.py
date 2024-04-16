from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    """
    Model class for storing information about a person.

    Attributes:
    - id (int): Primary key identifier for the person.
    - first_name (str): First name of the person.
    - last_name (str): Last name of the person.
    - phone_number (str): Phone number of the person.
    - addresses (Relationship): One-to-many relationship with Address model.
    """

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

    addresses = db.relationship('Address', backref='person', lazy=True)

    def __repr__(self):
        return f'<Person {self.first_name} {self.last_name}>'

class Address(db.Model):
    """
    Model class for storing information about a person's address.

    Attributes:
    - id (int): Primary key identifier for the address.
    - street (str): Street address.
    - city (str): City of the address.
    - state (str): State of the address.
    - zip_code (str): ZIP code of the address.
    - person_id (int): Foreign key reference to Person model.
    """
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)

    person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<Address {self.street} {self.city} {self.state}>'

class Livestock(db.Model):
    """
    Model class for storing information about livestock.

    Attributes:
    - id (int): Primary key identifier for the livestock.
    - ear_tag (str): Ear tag of the livestock.
    - species (str): Species of the livestock.
    - birthday (date): Birthday of the livestock.
    - gender (str): Gender of the livestock.
    - image_path (str): Path to the image of the livestock.
    """
    id = db.Column(db.Integer, primary_key=True)
    ear_tag = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    image_path = db.Column(db.String(255))

    def __repr__(self):
        return f'<Livestock {self.species} {self.ear_tag}>'

class Vehicle(db.Model):
    """
    Model class for storing information about vehicles.

    Attributes:
    - id (int): Primary key identifier for the vehicle.
    - brand (str): Brand of the vehicle.
    - model (str): Model of the vehicle.
    - year (int): Year of the vehicle.
    - image_path (str): Path to the image of the vehicle.
    """
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255)) 

    def __repr__(self):
        return f'<Vehicle {self.brand} {self.model}>'

class Land(db.Model):
    """
    Model class for storing information about land.

    Attributes:
    - id (int): Primary key identifier for the land.
    - type (str): Type of the land.
    - size (float): Size of the land.
    - ownership (str): Ownership status of the land.
    - unit (str): Unit of measurement for land size.
    - person_id (int): Foreign key reference to Person model.
    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Float, nullable=False)
    ownership = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(50))  

    person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return f'<Land {self.size} {self.type}>'

class Feedstock(db.Model):
    """
    Model class for storing information about feedstock.

    Attributes:
    - id (int): Primary key identifier for the feedstock.
    - category (str): Category of the feedstock.
    - quantity (int): Quantity of the feedstock.
    - unit (str): Unit of measurement for the feedstock quantity.
    """
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Feedstock {self.category} {self.quantity} {self.unit}>'

class Harvest(db.Model):
    """
    Model class for storing information about harvests.

    Attributes:
    - id (int): Primary key identifier for the harvest.
    - crop (str): Crop of the harvest.
    - quantity (int): Quantity of the harvest.
    - unit (str): Unit of measurement for the harvest quantity.
    - date (date): Date of the harvest.
    - land_id (int): Foreign key reference to Land model.
    - land (Relationship): Many-to-one relationship with Land model.
    """
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    land_id = db.Column(db.Integer, db.ForeignKey('land.id', ondelete='CASCADE'), nullable=False)
    land = db.relationship('Land', backref=db.backref('harvests', lazy=True))

    def __repr__(self):
        return f'<Harvest {self.crop} {self.quantity}>'
