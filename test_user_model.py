"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase
from psycopg2.errors import NotNullViolation
from models import db, User, Message, Follows
from sqlalchemy.exc import IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        db.session.commit()

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        db.session.commit()

    def test_user_model(self):
        u = User.query.filter_by(username='testuser').one()

        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr(self):
        u = User.query.filter_by(username='testuser').one()

        self.assertEqual(repr(u), f'<User #{u.id}: {u.username}, {u.email}>')

    def test_is_following(self):
        u1 = User.query.filter_by(username='testuser').one()
        u2 = User.query.filter_by(username='testuser2').one()

        self.assertFalse(u1.is_following(u2), False)

        u2.followers.append(u1)
        db.session.commit()

        self.assertTrue(u1.is_following(u2), True)

    def test_is_followed_by(self):
        u1 = User.query.filter_by(username='testuser').one()
        u2 = User.query.filter_by(username='testuser2').one()

        self.assertFalse(u1.is_followed_by(u2), False)

        u1.followers.append(u2)
        db.session.commit()

        self.assertTrue(u1.is_followed_by(u2), True)

    def test_signup(self):
        self.assertTrue(User.signup('testuser3', 'test3@test.com',
                                    'testpassword', "/testimage.jpg"))
        db.session.rollback()
        self.assertTrue(User.signup(
            'testuser3', 'test3@test.com', 'testpassword', None))

    def test_authenticate(self):
        u1 = User.query.filter_by(username='testuser').one()

        self.assertFalse(User.authenticate('fakeuser', 'HASHED_PASSWORD'))