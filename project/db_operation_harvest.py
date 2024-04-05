from models import db, Harvest

def add_harvest_to_database(crop, quantity, unit, date, land_id):
    new_harvest = Harvest(crop=crop, quantity=quantity, unit=unit, date=date, land_id=land_id)
    db.session.add(new_harvest)
    db.session.commit()

def get_all_harvests_from_database():
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
    harvest = Harvest.query.get(harvest_id)

    if harvest:
        db.session.delete(harvest)
        db.session.commit()
        return True
    else:
        return False

def update_harvest_in_database(harvest_id, crop, quantity, unit, date, land_id):
    harvest = Harvest.query.get(harvest_id)

    if harvest:
        harvest.crop = crop
        harvest.quantity = quantity
        harvest.unit = unit
        harvest.date = date
        harvest.land_id = land_id
        db.session.commit()