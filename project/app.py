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

#API-KEY
WEATHERBIT_API_KEY = "549a083fd4b143afa7be7cb4003a41ac"

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Route for the index page.

    Accepts POST requests to fetch weather data based on user input (city, country, postal code).
    Returns:
    - Renders index.html template with weather data.
    - JSON response with error message if weather data retrieval fails.
    """

    if request.method == 'POST':
        city = request.form['city']
        country = request.form['country']
        postal_code = request.form['postal_code']
        lang = 'de'

        url = f'https://api.weatherbit.io/v2.0/forecast/daily'
        params = {
            'city': city,
            'country': country,
            'postal_code': postal_code,  
            'lang': lang,
            'key': WEATHERBIT_API_KEY
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            weather_data = response.json()
            return render_template('index.html', weather_data=weather_data)
        else:
            return jsonify({'error': 'Fehler beim Abrufen der Wetterdaten'}), 500

    return render_template('index.html')

#Vehicle
@app.route('/vehicles')
def vehicles():
    """
    Route for displaying all vehicles.

    Returns:
    - Renders vehicles.html template with all vehicle data.
    """
    return render_template('vehicles.html', vehicles=Vehicle.query.all())

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    """
    Route for adding a new vehicle.

    Accepts POST requests with form data.
    Returns:
    - Redirects to the vehicles page.
    - Renders vehicles page with error message if any error occurs during addition.
    """
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
    """
    Route for editing a vehicle.

    Accepts POST requests with form data.
    Returns:
    - Redirects to the vehicles page.
    - Renders vehicles page with error message if any error occurs during edit.
    """
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
    """
    Route for retrieving all vehicle data.

    Returns:
    - JSON response with all vehicle data.
    """
    vehicle_list = get_all_vehicles()
    return jsonify(vehicle_list)

@app.route('/delete_vehicle', methods=['GET'])
def delete_vehicle():
    """
    Route for deleting a vehicle.

    Accepts GET requests with query parameter 'id' for vehicle ID.
    Returns:
    - JSON response indicating success or failure of deletion.
    """
    vehicle_id = request.args.get('id')
    success = delete_vehicle_by_id(vehicle_id)

    if success:
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Fahrzeug nicht gefunden")


@app.route('/search_vehicles', methods=['GET'])
def search_vehicles():
    """
    Route for searching vehicles.

    Accepts GET requests with query parameter 'search' for search query.
    Returns:
    - JSON response with matching vehicle data.
    """
    search_query = request.args.get('search', '')
    
    vehicle_list = search_vehicles_in_database(search_query)

    return jsonify(vehicle_list)

#Livestock
@app.route('/livestock')
def livestock():
    """
    Route for displaying all livestock.

    Returns:
    - Renders livestock.html template with all livestock data.
    """
    return render_template('livestock.html', livestock=Livestock.query.all())


@app.route('/add_livestock', methods=['POST'])
def add_livestock():
    """
    Route for adding a new livestock.

    Accepts POST requests with form data.
    Returns:
    - Redirects to the livestock page.
    """
    ear_tag = request.form['ear_tag']
    species = request.form['species']
    birthday = request.form['birthday']
    gender = request.form['gender']
    
    image_file = request.files.get('image')

    add_livestock_to_database(ear_tag, species, birthday, gender, image_file)

    return redirect(url_for('livestock'))

@app.route('/search_livestock', methods=['GET'])
def search_livestock():
    """
    Route for searching livestock.

    Accepts GET requests with query parameter 'search' for search query.
    Returns:
    - JSON response with matching livestock data.
    """
    search_query = request.args.get('search', '')

    livestock_list = search_livestock_in_database(search_query)

    return jsonify(livestock_list)

@app.route('/getlivestock', methods=['GET'])
def get_livestock():
    """
    Route for retrieving all livestock data.

    Returns:
    - JSON response with all livestock data.
    """

    livestock_list = get_all_livestock_from_database()

    return jsonify(livestock_list)

@app.route('/delete_livestock', methods=['GET'])
def delete_livestock():
    """
    Route for deleting a livestock.

    Accepts GET requests with query parameter 'id' for livestock ID.
    Returns:
    - JSON response indicating success or failure of deletion.
    """
    livestock_id = request.args.get('id')

    if delete_livestock_from_database(livestock_id):
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Tier nicht gefunden")
    
@app.route('/edit_livestock', methods=['POST'])
def edit_livestock():
    """
    Route for editing a livestock.

    Accepts POST requests with form data.
    Returns:
    - Redirects to the livestock page.
    """
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
    """
    Route for displaying all feedstock.

    Returns:
    - Renders feedstock.html template with all feedstock data.
    """
    return render_template('feedstock.html', feedstock=Feedstock.query.all())

@app.route('/search_feedstock', methods=['GET'])
def search_feedstock():
    """
    Route for searching feedstock.

    Accepts GET requests with query parameter 'search' for search query.
    Returns:
    - JSON response with matching feedstock data.
    """
    search_query = request.args.get('search', '')

    feedstock_list = search_feedstock_in_database(search_query)

    return jsonify(feedstock_list)

@app.route('/add_feedstock', methods=['POST'])
def add_feedstock():
    """
    Route for adding a new feedstock.

    Accepts POST requests with form data.
    Returns:
    - Redirects to the feedstock page.
    """
    category = request.form['category']
    quantity = request.form['quantity']
    unit = request.form['unit']

    add_feedstock_to_database(category, quantity, unit)

    return redirect(url_for('feedstock'))

@app.route('/getfeedstock', methods=['GET'])
def get_feedstock():
    """
    Route for retrieving all feedstock data.

    Returns:
    - JSON response with all feedstock data.
    """
    feedstock_list = get_all_feedstock_from_database()

    return jsonify(feedstock_list)

@app.route('/delete_feedstock', methods=['GET'])
def delete_feedstock():
    """
    Route for deleting a feedstock.

    Accepts GET requests with query parameter 'id' for feedstock ID.
    Returns:
    - JSON response indicating success or failure of deletion.
    """
    feedstock_id = request.args.get('id')

    if delete_feedstock_from_database(feedstock_id):
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Futter nicht gefunden")

@app.route('/edit_feedstock', methods=['POST'])
def edit_feedstock():
    """
    Route for editing a feedstock.

    Accepts POST requests with form data.
    Returns:
    - Redirects to the feedstock page.
    """
    feedstock_id = request.form['editId']
    category = request.form['editCategory']
    quantity = request.form['editQuantity']
    unit = request.form['editUnit']

    update_feedstock_in_database(feedstock_id, category, quantity, unit)

    return redirect(url_for('feedstock'))

#Harvest
@app.route('/harvest')
def harvest():
    """
    Route for displaying all harvests.

    Returns:
    - Renders harvest.html template with all harvest data.
    """
    return render_template('harvest.html', harvests=Harvest.query.all(), lands=Land.query.all())

@app.route('/harvest_chart')
def harvest_chart():
    """
    Route for generating a harvest chart.

    Returns:
    - JSON response with base64-encoded image URL of the chart.
    """
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
    """
    Route for adding a new harvest.

    Accepts POST requests with form data.
    Returns:
    - Redirects to the harvest page.
    """
    crop = request.form['crop']
    quantity = request.form['quantity']
    unit = request.form['unit']
    date = request.form['date']
    land_id = request.form['land_id']

    add_harvest_to_database(crop, quantity, unit, date, land_id)

    return redirect(url_for('harvest'))

@app.route('/getharvests', methods=['GET'])
def get_harvests():
    """
    Route for retrieving all harvest data.

    Returns:
    - JSON response with all harvest data.
    """
    harvest_list = get_all_harvests_from_database()

    return jsonify(harvest_list)

@app.route('/delete_harvest', methods=['GET'])
def delete_harvest():
    """
    Route for deleting a harvest.

    Accepts GET requests with query parameter 'id' for harvest ID.
    Returns:
    - JSON response indicating success or failure of deletion.
    """
    harvest_id = request.args.get('id')

    if delete_harvest_from_database(harvest_id):
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Ernte nicht gefunden")

@app.route('/edit_harvest', methods=['POST'])
def edit_harvest():
    """
    Route for editing a harvest.

    Accepts POST requests with form data.
    Returns:
    - Redirects to the harvest page.
    """
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
    """
    Route for displaying all lands.

    Returns:
    - Renders areas.html template with all land data.
    """
    return render_template('areas.html', lands=Land.query.all())

@app.route('/add_land', methods=['POST'])
def add_land():
    """
    Route for adding a new land.

    Accepts POST requests with form data.
    Returns:
    - Redirects to the lands page.
    """
    type = request.form['type']
    size = request.form['size']
    ownership = request.form['ownership']
    unit = request.form.get('unit')  

    form_data = request.form.to_dict()

    add_land_to_database(type, size, ownership, unit, form_data)

    return redirect(url_for('lands'))

@app.route('/delete_land', methods=['GET'])
def delete_land():
    """
    Route for deleting a land.

    Accepts GET requests with query parameter 'id' for land ID.
    Returns:
    - JSON response indicating success or failure of deletion.
    """
    land_id = request.args.get('id')
    delete_land_from_database(land_id)
    return jsonify(success=True)

@app.route('/get_land_details')
def get_land_details():
    """
    Route for retrieving details of a specific land.

    Accepts GET requests with query parameter 'id' for land ID.
    Returns:
    - JSON response with land details.
    """
    land_id = request.args.get('id')
    land_details = get_land_details_from_database(land_id)

    if land_details:
        return jsonify(land_details)
    else:
        return jsonify(success=False, message="Land not found")

@app.route('/edit_land', methods=['POST'])
def edit_land():
    """
    Route for editing a land.

    Accepts POST requests with form data.
    Returns:
    - Redirects to the lands page.
    """
    land_id = request.form.get('editId')
    form_data = request.form.to_dict()

    edited_land = edit_land_in_database(land_id, form_data)

    if edited_land:
        return redirect(url_for('lands'))
    else:
        return jsonify(success=False, message="Land not found or error occurred during edit")

@app.route('/search_lands', methods=['GET'])
def search_lands():
    """
    Route for searching lands.

    Accepts GET requests with query parameter 'ownership' for ownership type.
    Returns:
    - JSON response with matching land data.
    """
    ownership = request.args.get('ownership')
    lands_data = search_lands_in_database(ownership)
    return jsonify(lands_data)

if __name__ == '__main__':
    """
    Main entry point of the application.

    Runs the Flask app.
    """
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0')
