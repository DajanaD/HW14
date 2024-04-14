import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactCreate
from src.repository.contacts import (
    get_contacts,
    get_contact_by_id,
    create_contact,
    update_contact,
    delete_contact,
)


class TestNotes(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact_by_id(user=self.user, db=self.session, contact_id=1)
        self.assertEqual(result, contact)

    async def test_get_contact_by_id_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact_by_id(user=self.user, db=self.session, contact_id=1)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactCreate(title="test", description="test contact")
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)
        self.assertEqual(result.user, self.user)

    async def test_update_contact_found(self):
        contact_id = 1
        body = ContactCreate(title="updated", description="updated contact")
        contact = Contact(id=contact_id, user=self.user)
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(user=self.user, db=self.session, contact_id=contact_id, contact=body)
        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)

    async def test_update_contact_not_found(self):
        contact_id = 1
        body = ContactCreate(title="updated", description="updated contact")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(user=self.user, db=self.session, contact_id=contact_id, contact=body)
        self.assertIsNone(result)

    async def test_delete_contact_found(self):
        contact_id = 1
        contact = Contact(id=contact_id, user=self.user)
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await delete_contact(user=self.user, db=self.session, contact_id=contact_id)
        self.assertEqual(result, contact)

    async def test_delete_contact_not_found(self):
        contact_id = 1
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await delete_contact(user=self.user, db=self.session, contact_id=contact_id)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
