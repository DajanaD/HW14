from sqlalchemy.orm import Session
from src.database.models import Contact, User
from schemas import ContactCreate
from sqlalchemy.sql import and_

async def get_contacts(user: User, db: Session):
    """
    Get all contacts for a user.

    :param user: User object.
    :param db: Database session object.
    :return: List of contacts for the given user.
    """
    return db.query(Contact).filter(Contact.user_id == user.id).all()

async def get_contact_by_id(user: User, db: Session, contact_id: int):
    """
    Get a contact by its identifier for a user.

    :param user: User object.
    :param db: Database session object.
    :param contact_id: Identifier of the contact.
    :return: The contact if exists, otherwise None.
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

async def create_contact(body: ContactCreate, user: User, db: Session):
    """
    Create a new contact for a user.

    :param body: Schema object for creating a contact.
    :param user: User object.
    :param db: Database session object.
    :return: The newly created contact.
    """
    db_contact = Contact(title=body.title, description=body.description, user=user)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

async def update_contact(user: User, db: Session, contact_id: int, contact: ContactCreate):
    """
    Update an existing contact for a user.

    :param user: User object.
    :param db: Database session object.
    :param contact_id: The identifier of the contact to update.
    :param contact: Schema object for updating the contact.
    :return: The updated contact if exists, otherwise None.
    """
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

async def delete_contact(user: User, db: Session, contact_id: int):
    """
    Delete a contact for a user.

    :param user: User object.
    :param db: Database session object.
    :param contact_id: The identifier of the contact to delete.
    :return: The deleted contact if exists, otherwise None.
    """
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact
