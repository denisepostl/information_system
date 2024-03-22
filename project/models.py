from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

    addresses = db.relationship('Address', backref='person', lazy=True)

    def __repr__(self):
        return f'<Person {self.first_name} {self.last_name}>'

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)

    person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<Address {self.street} {self.city} {self.state}>'

class Livestock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ear_tag = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    image_path = db.Column(db.String(255))

    def __repr__(self):
        return f'<Livestock {self.species} {self.ear_tag}>'

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255)) 

    def __repr__(self):
        return f'<Vehicle {self.brand} {self.model}>'

class Land(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Float, nullable=False)
    ownership = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(50))  

    person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return f'<Land {self.size} {self.type}>'

class Feedstock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Feedstock {self.category} {self.quantity} {self.unit}>'

class Harvest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    land_id = db.Column(db.Integer, db.ForeignKey('land.id', ondelete='CASCADE'), nullable=False)
    land = db.relationship('Land', backref=db.backref('harvests', lazy=True))

    def __repr__(self):
        return f'<Harvest {self.crop} {self.quantity}>'
