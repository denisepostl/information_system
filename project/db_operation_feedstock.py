from models import db, Feedstock

def search_feedstock_in_database(search_query):
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
    new_feedstock = Feedstock(category=category, quantity=quantity, unit=unit)
    db.session.add(new_feedstock)
    db.session.commit()

def get_all_feedstock_from_database():
    feedstock_items = Feedstock.query.all()
    feedstock_list = [{
        'category': item.category,
        'quantity': item.quantity,
        'unit': item.unit
    } for item in feedstock_items]

    return feedstock_list

def delete_feedstock_from_database(feedstock_id):
    feedstock_item = Feedstock.query.get(feedstock_id)

    if feedstock_item:
        db.session.delete(feedstock_item)
        db.session.commit()
        return True
    else:
        return False
    
def update_feedstock_in_database(feedstock_id, category, quantity, unit):
    feedstock_item = Feedstock.query.get(feedstock_id)

    if feedstock_item:
        feedstock_item.category = category
        feedstock_item.quantity = quantity
        feedstock_item.unit = unit
        db.session.commit()

