from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from models import db, Vehicle, Livestock, Feedstock, Land, Person, Address, Harvest
from sqlalchemy import or_
import logging 
import requests
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@postgres-db:5432/farming_db'

db.init_app(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    brand = request.form['brand']
    model = request.form['model']
    year = request.form['year']
    
    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join('static', filename)  
            image.save(filepath)
    else:
        filepath = None

    new_vehicle = Vehicle(brand=brand, model=model, year=year, image_path=filename)  
    db.session.add(new_vehicle)
    db.session.commit()

    return redirect(url_for('vehicles'))

@app.route('/add_livestock', methods=['POST'])
def add_livestock():
    ear_tag = request.form['ear_tag']
    species = request.form['species']
    birthday = request.form['birthday']
    gender = request.form['gender']
    
    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join('static', filename)
            image.save(filepath)
    else:
        filepath = None

    new_livestock = Livestock(ear_tag=ear_tag, species=species, birthday=birthday, gender=gender, image_path=filename)
    db.session.add(new_livestock)
    db.session.commit()

    return redirect(url_for('livestock'))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/harvest_chart')
def harvest_chart():
    harvests = Harvest.query.all()  

    dates = [harvest.date.strftime('%m-%d') for harvest in harvests]  
    quantities = [harvest.quantity for harvest in harvests]

    plt.plot(dates, quantities, marker='o')
    plt.gcf().autofmt_xdate()  
    plt.xticks(rotation=45, ha="right")  

    plt.xlabel('Erntedatum')
    plt.ylabel('Erntemenge (kg)')
    plt.title('Zeitlicher Ernteertrag')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return jsonify({'graph_url': graph_url})

@app.route('/vehicles')
def vehicles():
    return render_template('vehicles.html', vehicles=Vehicle.query.all())

@app.route('/search_livestock', methods=['GET'])
def search_livestock():
    search_query = request.args.get('search', '')

    if search_query:
        livestock = Livestock.query.filter(or_(Livestock.ear_tag.ilike(f'%{search_query}%'),
                                               Livestock.species.ilike(f'%{search_query}%'))).all()
    else:
        livestock = []

    livestock_list = [{
        'ear_tag': animal.ear_tag,
        'species': animal.species,
        'birthday': str(animal.birthday),
        'gender': animal.gender,
        'image_path': animal.image_path,  
        'id': animal.id
    } for animal in livestock]

    return jsonify(livestock_list)

@app.route('/search_feedstock', methods=['GET'])
def search_feedstock():
    search_query = request.args.get('search', '')

    if search_query:
        feedstock = Feedstock.query.filter(Feedstock.category.ilike(f'%{search_query}%')).all()
    else:
        feedstock = []

    feedstock_list = [{
        'id': item.id,
        'category': item.category,
        'quantity': item.quantity,
        'unit': item.unit
    } for item in feedstock]

    return jsonify(feedstock_list)

@app.route('/search_vehicles', methods=['GET'])
def search_vehicles():
    search_query = request.args.get('search', '')

    if search_query:
        vehicles = Vehicle.query.filter(or_(Vehicle.brand.ilike(f'%{search_query}%'), Vehicle.model.ilike(f'%{search_query}%'))).all()
    else:
        vehicles = []

    vehicle_list = [{
        'brand': vehicle.brand,
        'model': vehicle.model,
        'year': vehicle.year,
        'id': vehicle.id,
        'image_path': vehicle.image_path  
    } for vehicle in vehicles]

    return jsonify(vehicle_list)

@app.route('/lands')
def lands():
    return render_template('areas.html', lands=Land.query.all())

@app.route('/add_land', methods=['POST'])
def add_land():
    type = request.form['type']
    size = request.form['size']
    ownership = request.form['ownership']

    if ownership == 'gepachtet':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        phone_number = request.form['phoneNumber']
        street = request.form['addressStreet']
        city = request.form['addressCity']
        state = request.form['addressState']
        zip_code = request.form['addressZipCode']

        person = Person(first_name=first_name, last_name=last_name, phone_number=phone_number)
        db.session.add(person)
        db.session.commit()

        address = Address(street=street, city=city, state=state, zip_code=zip_code, person=person)
        db.session.add(address)
        db.session.commit()

        new_land = Land(type=type, size=size, ownership=ownership, person_id=person.id)
    else:
        new_land = Land(type=type, size=size, ownership=ownership)

    db.session.add(new_land)
    db.session.commit()

    return redirect(url_for('lands'))


@app.route('/delete_land', methods=['GET'])
def delete_land():
    land_id = request.args.get('id')
    land = Land.query.get(land_id)

    if land:
        ownership = land.ownership

        if ownership == 'gepachtet':
            person_id = land.person_id  
            if person_id:
                person = Person.query.get(person_id)
                if person:
                    addresses = person.addresses
                    for address in addresses:
                        db.session.delete(address)

                    db.session.delete(person)

        db.session.delete(land)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Land not found")

    
@app.route('/edit_land', methods=['POST'])
def edit_land():
    land_id = request.form.get('editId')
    land = Land.query.get(land_id)

    if land:
        land.type = request.form.get('editType')
        land.size = request.form.get('editSize')
        land.ownership = request.form.get('editOwnership')

        if land.ownership == 'gepachtet':
            person_id = request.form.get('editPersonId')
            person = Person.query.get(person_id)

            if person:
                person.first_name = request.form.get('editFirstName')
                person.last_name = request.form.get('editLastName')
                person.phone_number = request.form.get('editPhoneNumber')

                address_id = request.form.get('editAddressId')
                address = Address.query.get(address_id)

                if address:
                    address.street = request.form.get('editAddressStreet')
                    address.city = request.form.get('editAddressCity')
                    address.state = request.form.get('editAddressState')
                    address.zip_code = request.form.get('editAddressZipCode')
                else:
                    address = Address(street=request.form.get('editAddressStreet'),
                                      city=request.form.get('editAddressCity'),
                                      state=request.form.get('editAddressState'),
                                      zip_code=request.form.get('editAddressZipCode'),
                                      person=person)
                    db.session.add(address)

                land.person = person

            else:
                person = Person(first_name=request.form.get('editFirstName'),
                                last_name=request.form.get('editLastName'),
                                phone_number=request.form.get('editPhoneNumber'))
                db.session.add(person)

                address = Address(street=request.form.get('editAddressStreet'),
                                  city=request.form.get('editAddressCity'),
                                  state=request.form.get('editAddressState'),
                                  zip_code=request.form.get('editAddressZipCode'),
                                  person=person)
                db.session.add(address)

                land.person = person

        db.session.commit()
        return redirect(url_for('lands'))
    else:
        return jsonify(success=False, message="Land not found")

    
@app.route('/harvest')
def harvest():
    return render_template('harvest.html', harvests=Harvest.query.all(), lands=Land.query.all())


@app.route('/add_harvest', methods=['POST'])
def add_harvest():
    crop = request.form['crop']
    quantity = request.form['quantity']
    unit = request.form['unit']
    date = request.form['date']
    land_id = request.form['land_id']

    new_harvest = Harvest(crop=crop, quantity=quantity, unit=unit, date=date, land_id=land_id)
    db.session.add(new_harvest)
    db.session.commit()

    return redirect(url_for('harvest'))

@app.route('/getharvests', methods=['GET'])
def get_harvests():
    harvests = Harvest.query.all()
    harvest_list = []
    for harvest in harvests:
        harvest_list.append({
            'crop': harvest.crop,
            'quantity': harvest.quantity,
            'unit': harvest.unit,
            'date': str(harvest.date),
            'land': harvest.land.type
        })
    return jsonify(harvest_list)

@app.route('/delete_harvest', methods=['GET'])
def delete_harvest():
    harvest_id = request.args.get('id')
    harvest = Harvest.query.get(harvest_id)

    if harvest:
        db.session.delete(harvest)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Ernte nicht gefunden")

@app.route('/edit_harvest', methods=['POST'])
def edit_harvest():
    harvest_id = request.form['editId']
    crop = request.form['editCrop']
    quantity = request.form['editQuantity']
    unit = request.form['editUnit']
    date = request.form['editDate']
    land_id = request.form['editLandId']

    harvest = Harvest.query.get(harvest_id)

    if harvest:
        harvest.crop = crop
        harvest.quantity = quantity
        harvest.unit = unit
        harvest.date = date
        harvest.land_id = land_id
        db.session.commit()

    return redirect(url_for('harvest'))

@app.route('/livestock')
def livestock():
    return render_template('livestock.html', livestock=Livestock.query.all())


@app.route('/feedstock')
def feedstock():
    return render_template('feedstock.html', feedstock=Feedstock.query.all())

@app.route('/add_feedstock', methods=['POST'])
def add_feedstock():
    category = request.form['category']
    quantity = request.form['quantity']
    unit = request.form['unit']

    new_feedstock = Feedstock(category=category, quantity=quantity, unit=unit)
    db.session.add(new_feedstock)
    db.session.commit()

    return redirect(url_for('feedstock'))

@app.route('/getfeedstock', methods=['GET'])
def get_feedstock():
    feedstock_items = Feedstock.query.all()
    feedstock_list = []
    for item in feedstock_items:
        feedstock_list.append({
            'category': item.category,
            'quantity': item.quantity,
            'unit': item.unit
        })
    return jsonify(feedstock_list)

@app.route('/delete_feedstock', methods=['GET'])
def delete_feedstock():
    feedstock_id = request.args.get('id')
    feedstock_item = Feedstock.query.get(feedstock_id)

    if feedstock_item:
        db.session.delete(feedstock_item)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Futter nicht gefunden")

@app.route('/edit_feedstock', methods=['POST'])
def edit_feedstock():
    feedstock_id = request.form['editId']
    category = request.form['editCategory']
    quantity = request.form['editQuantity']
    unit = request.form['editUnit']

    feedstock_item = Feedstock.query.get(feedstock_id)

    if feedstock_item:
        feedstock_item.category = category
        feedstock_item.quantity = quantity
        feedstock_item.unit = unit
        db.session.commit()

    return redirect(url_for('feedstock'))

@app.route('/getlivestock', methods=['GET'])
def get_livestock():
    livestock = Livestock.query.all()
    livestock_list = []
    for animal in livestock:
        livestock_list.append({
            'ear_tag': animal.ear_tag,
            'species': animal.species,
            'birthday': str(animal.birthday),
            'gender': animal.gender
        })
    return jsonify(livestock_list)

@app.route('/delete_livestock', methods=['GET'])
def delete_livestock():
    livestock_id = request.args.get('id')
    animal = Livestock.query.get(livestock_id)

    if animal:
        db.session.delete(animal)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Tier nicht gefunden")

@app.route('/edit_livestock', methods=['POST'])
def edit_livestock():
    livestock_id = request.form['editId']
    ear_tag = request.form['editEarTag']
    species = request.form['editSpecies']
    birthday = request.form['editBirthday']
    gender = request.form['editGender']

    animal = Livestock.query.get(livestock_id)

    if animal:
        animal.ear_tag = ear_tag
        animal.species = species
        animal.birthday = birthday
        animal.gender = gender

        if 'editImage' in request.files:
            new_image = request.files['editImage']
            if new_image and allowed_file(new_image.filename):
                filename = secure_filename(new_image.filename)
                filepath = os.path.join('static', filename)
                new_image.save(filepath)
                animal.image_path = filename

        db.session.commit()

    return redirect(url_for('livestock'))


@app.route('/getvehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    vehicle_list = []
    for vehicle in vehicles:
        vehicle_list.append({
            'brand': vehicle.brand,
            'model': vehicle.model,
            'year': vehicle.year
        })
    return jsonify(vehicle_list)

@app.route('/delete_vehicle', methods=['GET'])
def delete_vehicle():
    vehicle_id = request.args.get('id')
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Fahrzeug nicht gefunden")

@app.route('/edit_vehicle', methods=['POST'])
def edit_vehicle():
    vehicle_id = request.form['editId']
    model = request.form['editModel']
    brand = request.form['editBrand']
    year = request.form['editYear']

    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle:
        vehicle.brand = brand
        vehicle.model = model
        vehicle.year = year

        if 'editImage' in request.files:
            new_image = request.files['editImage']
            if new_image and allowed_file(new_image.filename):
                filename = secure_filename(new_image.filename)
                filepath = os.path.join('static', filename)
                new_image.save(filepath)
                vehicle.image_path = filename

        db.session.commit()

    return redirect(url_for('vehicles'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0')