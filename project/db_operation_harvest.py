from models import db, Harvest

def add_harvest_to_database(crop, quantity, unit, date, land_id):
    """
    Add a harvest entry to the database.

    Parameters:
    - crop (str): The crop harvested.
    - quantity (float): The quantity of the crop harvested.
    - unit (str): The unit of measurement for the quantity.
    - date (datetime): The date of the harvest.
    - land_id (int): The ID of the land associated with the harvest.

    Returns:
    - None
    """
    new_harvest = Harvest(crop=crop, quantity=quantity, unit=unit, date=date, land_id=land_id)
    db.session.add(new_harvest)
    db.session.commit()

def get_all_harvests_from_database():
    """
    Retrieve all harvest entries from the database.

    Returns:
    - list: A list containing dictionaries with information about each harvest.
      Each dictionary contains the following keys:
        - 'crop': The crop harvested.
        - 'quantity': The quantity of the crop harvested.
        - 'unit': The unit of measurement for the quantity.
        - 'date': The date of the harvest (formatted as a string).
        - 'land': The type of land associated with the harvest.
    """
    harvests = Harvest.query.all()
    harvest_list = [{
        'crop': harvest.crop,
        'quantity': harvest.quantity,
        'unit': harvest.unit,
        'date': str(harvest.date),
        'land': harvest.land.type
    } for harvest in harvests]

    return harvest_list

def delete_harvest_from_database(harvest_id):
    """
    Delete a harvest entry from the database.

    Parameters:
    - harvest_id (int): The ID of the harvest entry to be deleted.

    Returns:
    - bool: True if the deletion is successful, False otherwise.
    """
    harvest = Harvest.query.get(harvest_id)

    if harvest:
        db.session.delete(harvest)
        db.session.commit()
        return True
    else:
        return False

def update_harvest_in_database(harvest_id, crop, quantity, unit, date, land_id):
    """
    Update a harvest entry in the database.

    Parameters:
    - harvest_id (int): The ID of the harvest entry to be updated.
    - crop (str): The updated crop harvested.
    - quantity (float): The updated quantity of the crop harvested.
    - unit (str): The updated unit of measurement for the quantity.
    - date (datetime): The updated date of the harvest.
    - land_id (int): The updated ID of the land associated with the harvest.

    Returns:
    - None
    """
    harvest = Harvest.query.get(harvest_id)

    if harvest:
        harvest.crop = crop
        harvest.quantity = quantity
        harvest.unit = unit
        harvest.date = date
        harvest.land_id = land_id
        db.session.commit()