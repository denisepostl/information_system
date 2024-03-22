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
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from db_operation_vehicle import add_vehicle_to_db, get_all_vehicles, delete_vehicle_by_id, update_vehicle_in_database, search_vehicles_in_database, is_valid_year
from db_operation_livestock import add_livestock_to_database, search_livestock_in_database, get_all_livestock_from_database, delete_livestock_from_database, update_livestock_in_database
from db_operation_feedstock import search_feedstock_in_database, add_feedstock_to_database, get_all_feedstock_from_database, delete_feedstock_from_database, update_feedstock_in_database
from db_operation_harvest import add_harvest_to_database, delete_harvest_from_database, get_all_harvests_from_database, add_harvest_to_database, update_harvest_in_database
from db_operation_land import add_land_to_database, delete_land_from_database, get_land_details_from_database, edit_land_in_database, search_lands_in_database

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#Connection to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@postgres-db:5432/farming_db'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#Vehicle
@app.route('/vehicles')
def vehicles():
    return render_template('vehicles.html', vehicles=Vehicle.query.all())

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    brand = request.form['brand']
    model = request.form['model']
    year = request.form['year']

    if not is_valid_year(year):
        error = 'Ungültiges Jahr'
        return render_template('vehicles.html', error=error)

    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join('static', filename)
            image.save(filepath)
    else:
        filepath = None

    try:
        add_vehicle_to_db(brand, model, int(year), filename)
    except Exception as e:
        error = str(e)
        return render_template('vehicles.html', error=error)

    return redirect(url_for('vehicles'))

@app.route('/edit_vehicle', methods=['POST'])
def edit_vehicle():
    vehicle_id = request.form['editId']
    model = request.form['editModel']
    brand = request.form['editBrand']
    year = request.form['editYear']

    if not is_valid_year(year):
        error = 'Ungültiges Jahr'
        return render_template('vehicles.html', error=error)

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        error = 'Fahrzeug nicht gefunden'
        return render_template('vehicles.html', error=error)

    try:
        update_vehicle_in_database(vehicle, brand, model, int(year), request.files.get('editImage'))
    except Exception as e:
        error = str(e)
        return render_template('vehicles.html', error=error)

    return redirect(url_for('vehicles'))

@app.route('/getvehicles', methods=['GET'])
def get_vehicles():
    vehicle_list = get_all_vehicles()
    return jsonify(vehicle_list)

@app.route('/delete_vehicle', methods=['GET'])
def delete_vehicle():
    vehicle_id = request.args.get('id')
    success = delete_vehicle_by_id(vehicle_id)

    if success:
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Fahrzeug nicht gefunden")


@app.route('/search_vehicles', methods=['GET'])
def search_vehicles():
    search_query = request.args.get('search', '')
    
    vehicle_list = search_vehicles_in_database(search_query)

    return jsonify(vehicle_list)

#Livestock
@app.route('/livestock')
def livestock():
    return render_template('livestock.html', livestock=Livestock.query.all())


@app.route('/add_livestock', methods=['POST'])
def add_livestock():
    ear_tag = request.form['ear_tag']
    species = request.form['species']
    birthday = request.form['birthday']
    gender = request.form['gender']
    
    image_file = request.files.get('image')

    add_livestock_to_database(ear_tag, species, birthday, gender, image_file)

    return redirect(url_for('livestock'))

@app.route('/search_livestock', methods=['GET'])
def search_livestock():
    search_query = request.args.get('search', '')

    livestock_list = search_livestock_in_database(search_query)

    return jsonify(livestock_list)

@app.route('/getlivestock', methods=['GET'])
def get_livestock():
    livestock_list = get_all_livestock_from_database()

    return jsonify(livestock_list)

@app.route('/delete_livestock', methods=['GET'])
def delete_livestock():
    livestock_id = request.args.get('id')

    if delete_livestock_from_database(livestock_id):
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

    new_image = request.files.get('editImage')

    update_livestock_in_database(livestock_id, ear_tag, species, birthday, gender, new_image)

    return redirect(url_for('livestock'))


#Feedstock
@app.route('/feedstock')
def feedstock():
    return render_template('feedstock.html', feedstock=Feedstock.query.all())

@app.route('/search_feedstock', methods=['GET'])
def search_feedstock():
    search_query = request.args.get('search', '')

    feedstock_list = search_feedstock_in_database(search_query)

    return jsonify(feedstock_list)

@app.route('/add_feedstock', methods=['POST'])
def add_feedstock():
    category = request.form['category']
    quantity = request.form['quantity']
    unit = request.form['unit']

    add_feedstock_to_database(category, quantity, unit)

    return redirect(url_for('feedstock'))

@app.route('/getfeedstock', methods=['GET'])
def get_feedstock():
    feedstock_list = get_all_feedstock_from_database()

    return jsonify(feedstock_list)

@app.route('/delete_feedstock', methods=['GET'])
def delete_feedstock():
    feedstock_id = request.args.get('id')

    if delete_feedstock_from_database(feedstock_id):
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Futter nicht gefunden")

@app.route('/edit_feedstock', methods=['POST'])
def edit_feedstock():
    feedstock_id = request.form['editId']
    category = request.form['editCategory']
    quantity = request.form['editQuantity']
    unit = request.form['editUnit']

    update_feedstock_in_database(feedstock_id, category, quantity, unit)

    return redirect(url_for('feedstock'))

#Harvest
@app.route('/harvest')
def harvest():
    return render_template('harvest.html', harvests=Harvest.query.all(), lands=Land.query.all())

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

@app.route('/add_harvest', methods=['POST'])
def add_harvest():
    crop = request.form['crop']
    quantity = request.form['quantity']
    unit = request.form['unit']
    date = request.form['date']
    land_id = request.form['land_id']

    add_harvest_to_database(crop, quantity, unit, date, land_id)

    return redirect(url_for('harvest'))

@app.route('/getharvests', methods=['GET'])
def get_harvests():
    harvest_list = get_all_harvests_from_database()

    return jsonify(harvest_list)

@app.route('/delete_harvest', methods=['GET'])
def delete_harvest():
    harvest_id = request.args.get('id')

    if delete_harvest_from_database(harvest_id):
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

    update_harvest_in_database(harvest_id, crop, quantity, unit, date, land_id)

    return redirect(url_for('harvest'))

#Land
@app.route('/lands')
def lands():
    return render_template('areas.html', lands=Land.query.all())

@app.route('/add_land', methods=['POST'])
def add_land():
    type = request.form['type']
    size = request.form['size']
    ownership = request.form['ownership']
    unit = request.form.get('unit')  

    form_data = request.form.to_dict()

    add_land_to_database(type, size, ownership, unit, form_data)

    return redirect(url_for('lands'))

@app.route('/delete_land', methods=['GET'])
def delete_land():
    land_id = request.args.get('id')
    delete_land_from_database(land_id)
    return jsonify(success=True)

@app.route('/get_land_details')
def get_land_details():
    land_id = request.args.get('id')
    land_details = get_land_details_from_database(land_id)

    if land_details:
        return jsonify(land_details)
    else:
        return jsonify(success=False, message="Land not found")

@app.route('/edit_land', methods=['POST'])
def edit_land():
    land_id = request.form.get('editId')
    form_data = request.form.to_dict()

    edited_land = edit_land_in_database(land_id, form_data)

    if edited_land:
        return redirect(url_for('lands'))
    else:
        return jsonify(success=False, message="Land not found or error occurred during edit")

@app.route('/search_lands', methods=['GET'])
def search_lands():
    ownership = request.args.get('ownership')
    lands_data = search_lands_in_database(ownership)
    return jsonify(lands_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0')
