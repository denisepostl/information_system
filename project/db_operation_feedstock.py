from models import db, Feedstock

def search_feedstock_in_database(search_query):
    """
    Search for feedstock items in the database based on a search query.

    Parameters:
    - search_query (str): The query string to search for in the category field.

    Returns:
    - list: A list of dictionaries representing feedstock items matching the search query.
            Each dictionary contains the keys 'id', 'category', 'quantity', and 'unit'.
    """
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

    return feedstock_list

def add_feedstock_to_database(category, quantity, unit):
    """
    Add a new feedstock item to the database.

    Parameters:
    - category (str): The category of the feedstock item.
    - quantity (float): The quantity of the feedstock item.
    - unit (str): The unit of measurement for the quantity.

    Returns:
    - None
    """
    new_feedstock = Feedstock(category=category, quantity=quantity, unit=unit)
    db.session.add(new_feedstock)
    db.session.commit()

def get_all_feedstock_from_database():
    """
    Retrieve all feedstock items from the database.

    Returns:
    - list: A list of dictionaries representing all feedstock items in the database.
            Each dictionary contains the keys 'category', 'quantity', and 'unit'.
    """
    feedstock_items = Feedstock.query.all()
    feedstock_list = [{
        'category': item.category,
        'quantity': item.quantity,
        'unit': item.unit
    } for item in feedstock_items]

    return feedstock_list

def delete_feedstock_from_database(feedstock_id):
    """
    Delete a feedstock item from the database.

    Parameters:
    - feedstock_id (int): The ID of the feedstock item to delete.

    Returns:
    - bool: True if the feedstock item was successfully deleted, False otherwise.
    """
    feedstock_item = Feedstock.query.get(feedstock_id)

    if feedstock_item:
        db.session.delete(feedstock_item)
        db.session.commit()
        return True
    else:
        return False
    
def update_feedstock_in_database(feedstock_id, category, quantity, unit):
    """
    Update a feedstock item in the database.

    Parameters:
    - feedstock_id (int): The ID of the feedstock item to update.
    - category (str): The new category for the feedstock item.
    - quantity (float): The new quantity for the feedstock item.
    - unit (str): The new unit of measurement for the quantity.

    Returns:
    - None
    """
    feedstock_item = Feedstock.query.get(feedstock_id)

    if feedstock_item:
        feedstock_item.category = category
        feedstock_item.quantity = quantity
        feedstock_item.unit = unit
        db.session.commit()

