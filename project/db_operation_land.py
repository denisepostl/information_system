from models import Person, Address, Land, db
from sqlalchemy.exc import IntegrityError

def add_land_to_database(type, size, ownership, unit, form_data):
    """
    Add a land entry to the database.

    Parameters:
    - type (str): The type of land.
    - size (float): The size of the land.
    - ownership (str): The ownership status of the land.
    - unit (str): The unit of measurement for the land size.
    - form_data (dict): A dictionary containing form data related to the land.
        It may include:
            - 'firstName' (str): The first name of the landowner (if ownership is 'gepachtet').
            - 'lastName' (str): The last name of the landowner (if ownership is 'gepachtet').
            - 'phoneNumber' (str): The phone number of the landowner (if ownership is 'gepachtet').
            - 'addressStreet' (str): The street address of the landowner (if ownership is 'gepachtet').
            - 'addressCity' (str): The city of the landowner (if ownership is 'gepachtet').
            - 'addressState' (str): The state of the landowner (if ownership is 'gepachtet').
            - 'addressZipCode' (str): The zip code of the landowner (if ownership is 'gepachtet').

    Returns:
    - None
    """
    if ownership == 'gepachtet':
        person = Person(first_name=form_data['firstName'], last_name=form_data['lastName'], phone_number=form_data['phoneNumber'])
        db.session.add(person)
        db.session.commit()

        address = Address(street=form_data['addressStreet'], city=form_data['addressCity'], state=form_data['addressState'], zip_code=form_data['addressZipCode'], person=person)
        db.session.add(address)
        db.session.commit()

        new_land = Land(type=type, size=size, ownership=ownership, unit=unit, person_id=person.id)
    else:
        new_land = Land(type=type, size=size, ownership=ownership, unit=unit)

    db.session.add(new_land)
    db.session.commit()

def delete_land_from_database(land_id):
    """
    Delete a land entry from the database.

    Parameters:
    - land_id (int): The ID of the land entry to be deleted.

    Returns:
    - None
    """
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

def get_land_details_from_database(land_id):
    """
    Retrieve details of a land entry from the database.

    Parameters:
    - land_id (int): The ID of the land entry to retrieve details for.

    Returns:
    - dict or None: A dictionary containing details of the land entry if found, None otherwise.
    """
    land = Land.query.get(land_id)

    if land:
        land_details = {'type': land.type, 'size': land.size, 'ownership': land.ownership}

        if land.ownership == 'gepachtet':
            person = Person.query.get(land.person_id)

            if person:
                land_details['person'] = {'first_name': person.first_name, 'last_name': person.last_name, 'phone_number': person.phone_number}

                address = Address.query.filter_by(person_id=land.person_id).first()
                if address:
                    land_details['person']['address'] = {'street': address.street, 'city': address.city, 'state': address.state, 'zip_code': address.zip_code}
                else:
                    land_details['person']['address'] = None
            else:
                land_details['person'] = None
        else:
            land_details['person'] = None

        return land_details
    else:
        return None

def edit_land_in_database(land_id, form_data):
    """
    Edit a land entry in the database.

    Parameters:
    - land_id (int): The ID of the land entry to be edited.
    - form_data (dict): A dictionary containing form data for editing the land entry.

    Returns:
    - Land or None: The edited land entry if successful, None otherwise.
    """
    land = Land.query.get(land_id)

    if land:
        if land.ownership == 'gepachtet' and form_data.get('editOwnership') == 'eigenbesitz':
            person_id = land.person_id
            person = Person.query.get(person_id)

            if person:
                address = Address.query.filter_by(person_id=person_id).first()

                if address:
                    db.session.delete(address)

                db.session.delete(person)

                land.person_id = None

        elif land.ownership == 'eigenbesitz' and form_data.get('editOwnership') == 'gepachtet':
            new_person = Person(first_name=form_data.get('editFirstName'), last_name=form_data.get('editLastName'), phone_number=form_data.get('editPhoneNumber'))
            new_address = Address(street=form_data.get('editAddressStreet'), city=form_data.get('editAddressCity'), state=form_data.get('editAddressState'), zip_code=form_data.get('editAddressZipCode'), person=new_person)

            try:
                db.session.add(new_person)
                db.session.add(new_address)
                db.session.flush()
                land.person_id = new_person.id
            except IntegrityError:
                db.session.rollback()
                return None  
            
        land.type = form_data.get('editType')
        land.size = form_data.get('editSize')
        land.ownership = form_data.get('editOwnership')
        land.unit = form_data.get('editUnit')

        if land.ownership == 'gepachtet':
            person_id = land.person_id
            person = Person.query.get(person_id)

            if person:
                person.first_name = form_data.get('editFirstName')
                person.last_name = form_data.get('editLastName')
                person.phone_number = form_data.get('editPhoneNumber')

                address_id = person_id
                address = Address.query.get(address_id)

                if address:
                    address.street = form_data.get('editAddressStreet')
                    address.city = form_data.get('editAddressCity')
                    address.state = form_data.get('editAddressState')
                    address.zip_code = form_data.get('editAddressZipCode')
                else:
                    address = Address(street=form_data.get('editAddressStreet'), city=form_data.get('editAddressCity'), state=form_data.get('editAddressState'), zip_code=form_data.get('editAddressZipCode'), person=person)
                    db.session.add(address)

                db.session.merge(person)
                db.session.merge(address)

        db.session.merge(land)
        db.session.commit()

        return land
    else:
        return None

def search_lands_in_database(ownership):
    """
    Search for land entries in the database based on ownership status.

    Parameters:
    - ownership (str): The ownership status to search for ('eigenbesitz' or 'gepachtet').

    Returns:
    - list: A list of dictionaries containing details of the land entries found.
    """
    lands = Land.query.filter_by(ownership=ownership).all()

    lands_data = []

    for land in lands:
        land_data = {'type': land.type, 'size': land.size, 'ownership': land.ownership, 'unit': land.unit}

        if land.ownership == 'gepachtet' and land.person_id:
            person = Person.query.get(land.person_id)

            if person:
                land_data['person'] = {'first_name': person.first_name, 'last_name': person.last_name, 'phone_number': person.phone_number}

                address = Address.query.filter_by(person_id=land.person_id).first()

                if address:
                    land_data['person']['address'] = {'street': address.street, 'city': address.city, 'state': address.state, 'zip_code': address.zip_code}
                else:
                    land_data['person']['address'] = None
            else:
                land_data['person'] = None
        else:
            land_data['person'] = None

        lands_data.append(land_data)

    return lands_data