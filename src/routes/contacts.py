from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import Contact, ContactCreate
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/notes', tags=["notes"])


# Отримати всі контакти
@router.get("/", response_model=List[Contact])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, db, current_user)
    return contacts

# Отримати контакт за ідентифікатором
@router.get("/{contact_id}", response_model=Contact)
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    db_contact = await repository_contacts.get_contact_by_id(db, contact_id, current_user)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return db_contact

# Створити новий контакт
@router.post("/", response_model=Contact)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(db=db, contact=contact, current_user=current_user)

# Оновити існуючий контакт
@router.put("/{contact_id}", response_model=Contact)
async def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    db_contact = await repository_contacts.update_contact(db=db, contact_id=contact_id, contact=contact, current_user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return db_contact

# Видалити контакт
@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    db_contact = await repository_contacts.delete_contact(db=db, contact_id=contact_id, current_user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return {"message": "Contact deleted successfully"}










