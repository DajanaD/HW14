from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import Contact, ContactCreate
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/notes', tags=["notes"])


@router.get("/", response_model=List[Contact])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve all contacts.

    :param skip: Number of records to skip.
    :param limit: Maximum number of records to retrieve.
    :param db: Database session object.
    :param current_user: Current authenticated user.
    :return: List of contacts.
    """
    contacts = await repository_contacts.get_contacts(skip, limit, db, current_user)
    return contacts


@router.get("/{contact_id}", response_model=Contact)
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a contact by its identifier.

    :param contact_id: Identifier of the contact.
    :param db: Database session object.
    :param current_user: Current authenticated user.
    :return: Contact object.
    """
    db_contact = await repository_contacts.get_contact_by_id(db, contact_id, current_user)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return db_contact


@router.post("/", response_model=Contact)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Create a new contact.

    :param contact: ContactCreate object containing contact details.
    :param db: Database session object.
    :param current_user: Current authenticated user.
    :return: Newly created contact object.
    """
    return await repository_contacts.create_contact(db=db, contact=contact, current_user=current_user)


@router.put("/{contact_id}", response_model=Contact)
async def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Update an existing contact.

    :param contact_id: Identifier of the contact to update.
    :param contact: ContactCreate object containing updated contact details.
    :param db: Database session object.
    :param current_user: Current authenticated user.
    :return: Updated contact object.
    """
    db_contact = await repository_contacts.update_contact(db=db, contact_id=contact_id, contact=contact, current_user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return db_contact


@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Delete a contact.

    :param contact_id: Identifier of the contact to delete.
    :param db: Database session object.
    :param current_user: Current authenticated user.
    :return: Confirmation message.
    """
    db_contact = await repository_contacts.delete_contact(db=db, contact_id=contact_id, current_user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return {"message": "Contact deleted successfully"}
