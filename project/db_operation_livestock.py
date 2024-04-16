from models import db, Livestock  
import os 
from werkzeug.utils import secure_filename
from sqlalchemy import or_

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    """
    Check if the filename has an allowed extension.

    Parameters:
    - filename (str): The name of the file to check.

    Returns:
    - bool: True if the filename has an allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def add_livestock_to_database(ear_tag, species, birthday, gender, image_file):
    """
    Add a livestock entry to the database.

    Parameters:
    - ear_tag (str): The ear tag of the livestock.
    - species (str): The species of the livestock.
    - birthday (datetime): The birthday of the livestock.
    - gender (str): The gender of the livestock.
    - image_file (FileStorage): The image file of the livestock.

    Returns:
    - None
    """
    filename = None

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        filepath = os.path.join('static', filename)
        image_file.save(filepath)

    new_livestock = Livestock(ear_tag=ear_tag, species=species, birthday=birthday, gender=gender, image_path=filename)
    db.session.add(new_livestock)
    db.session.commit()

def search_livestock_in_database(search_query):
    """
    Search for livestock entries in the database based on a search query.

    Parameters:
    - search_query (str): The search query.

    Returns:
    - list: A list of dictionaries containing details of the livestock entries found.
    """
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

    return livestock_list

def get_all_livestock_from_database():
    """
    Retrieve all livestock entries from the database.

    Returns:
    - list: A list of dictionaries containing details of all livestock entries.
    """
    livestock = Livestock.query.all()
    livestock_list = [{
        'ear_tag': animal.ear_tag,
        'species': animal.species,
        'birthday': str(animal.birthday),
        'gender': animal.gender
    } for animal in livestock]

    return livestock_list

def delete_livestock_from_database(livestock_id):
    """
    Delete a livestock entry from the database.

    Parameters:
    - livestock_id (int): The ID of the livestock entry to be deleted.

    Returns:
    - bool: True if the deletion is successful, False otherwise.
    """
    animal = Livestock.query.get(livestock_id)

    if animal:
        db.session.delete(animal)
        db.session.commit()
        return True
    else:
        return False
    
def update_livestock_in_database(livestock_id, ear_tag, species, birthday, gender, new_image):
    """
    Update a livestock entry in the database.

    Parameters:
    - livestock_id (int): The ID of the livestock entry to be updated.
    - ear_tag (str): The updated ear tag of the livestock.
    - species (str): The updated species of the livestock.
    - birthday (datetime): The updated birthday of the livestock.
    - gender (str): The updated gender of the livestock.
    - new_image (FileStorage): The new image file of the livestock (optional).

    Returns:
    - None
    """
    animal = Livestock.query.get(livestock_id)

    if animal:
        animal.ear_tag = ear_tag
        animal.species = species
        animal.birthday = birthday
        animal.gender = gender

        if new_image and allowed_file(new_image.filename):
            filename = secure_filename(new_image.filename)
            filepath = os.path.join('static', filename)
            new_image.save(filepath)
            animal.image_path = filename

        db.session.commit()
