from sqlalchemy.orm import Session
from src.database.models import Contact, User
from schemas import ContactCreate

# Отримати всі контакти
async def get_contacts(user: User, db: Session):
    return db.query(Contact).filter(Contact.user_id == user.id).all()

# Отримати контакт за ідентифікатором
async def get_contact_by_id(user: User, db: Session, contact_id: int):
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

# Створити новий контакт
async def create_contact(body: ContactCreate, user: User, db: Session):
    db_contact = Contact(title=body.title, description=body.description, user=user)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Оновити існуючий контакт
async def update_contact(user: User, db: Session, contact_id: int, contact: ContactCreate):
    db_contact = db.query(Contact).filter(add_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

# Видалити контакт
async def delete_contact(user: User, db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(add_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact
