from models import db, Vehicle  
import os 
from werkzeug.utils import secure_filename
from sqlalchemy import or_

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def add_vehicle_to_db(brand, model, year, image_path):
    """
    Add a vehicle entry to the database.

    Parameters:
    - brand (str): The brand of the vehicle.
    - model (str): The model of the vehicle.
    - year (int): The year of manufacture of the vehicle.
    - image_path (str): The file path of the vehicle image.

    Returns:
    - None
    """
    new_vehicle = Vehicle(brand=brand, model=model, year=year, image_path=image_path)
    db.session.add(new_vehicle)
    db.session.commit()

def get_all_vehicles():
    """
    Retrieve all vehicle entries from the database.

    Returns:
    - list: A list of dictionaries containing details of all vehicle entries.
    """
    vehicles = Vehicle.query.all()
    vehicle_list = []
    for vehicle in vehicles:
        vehicle_list.append({
            'brand': vehicle.brand,
            'model': vehicle.model,
            'year': vehicle.year
        })
    return vehicle_list

def delete_vehicle_by_id(vehicle_id):
    """
    Delete a vehicle entry from the database.

    Parameters:
    - vehicle_id (int): The ID of the vehicle entry to be deleted.

    Returns:
    - bool: True if the deletion is successful, False otherwise.
    """
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        return True
    else:
        return False
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def update_vehicle_in_database(vehicle, brand, model, year, new_image):
    """
    Update a vehicle entry in the database.

    Parameters:
    - vehicle: The vehicle entry to be updated.
    - brand (str): The updated brand of the vehicle.
    - model (str): The updated model of the vehicle.
    - year (int): The updated year of manufacture of the vehicle.
    - new_image (FileStorage): The new image file of the vehicle (optional).

    Returns:
    - None
    """
    vehicle.brand = brand
    vehicle.model = model
    vehicle.year = year

    if new_image and allowed_file(new_image.filename):
        filename = secure_filename(new_image.filename)
        filepath = os.path.join('static', filename)
        new_image.save(filepath)
        vehicle.image_path = filename

    db.session.commit()

def search_vehicles_in_database(search_query):
    """
    Search for vehicle entries in the database based on a search query.

    Parameters:
    - search_query (str): The search query.

    Returns:
    - list: A list of dictionaries containing details of the vehicle entries found.
    """
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

    return vehicle_list

def is_valid_year(year_str):
    """
    Check if a year string is a valid year.

    Parameters:
    - year_str (str): The year as a string.

    Returns:
    - bool: True if the year string is a valid year, False otherwise.
    """
    try:
        year = int(year_str)
        return 1000 <= year <= 9999
    except ValueError:
        return False
