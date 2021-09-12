"""User model tests."""

from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows
from sqlalchemy.exc import IntegrityError

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()


class MessageModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        db.session.commit()

        m = Message(text="testtext")
        u = User(username="testuser",
                 email="test@test.com",
                 password="password")

        u.messages.append(m)
        db.session.add(u)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        db.session.commit()

    def test_user_model(self):
        m = Message(text='testtext2')
        u = User.query.filter_by(username='testuser').one()

        self.assertEqual(len(u.messages), 1)

        u.messages.append(m)
        db.session.commit()

        self.assertEqual(len(m.user.messages), 2)