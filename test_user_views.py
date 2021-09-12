from app import app
from unittest import TestCase
from app import app, g, add_user_to_g
from flask import session
from models import db, User, Message, Follows
import json
import os

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()


class FlaskTests(TestCase):
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
        app.config['TESTING'] = True

    def tearDown(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        db.session.commit()

    def test_signup(self):
        with self.client:
            response = self.client.get('/signup')
            self.assertIn(b'Join Warbler today.', response.data)

    def test_login(self):
        with self.client:
            response = self.client.get('/login')
            self.assertIn(b'Welcome back.', response.data)

    def test_list_users(self):
        with self.client:
            response = self.client.get('/users')
            self.assertIn(b'<p>@testuser</p>', response.data)

    def test_users_show(self):
        with self.client:
            u = User.query.first()
            response = self.client.get(f'/users/{u.id}')
            self.assertIn(
                b'<ul class="list-group" id="messages">', response.data)

    def test_show_likes(self):
        with self.client:
            u = User.query.first()
            response = self.client.get(f'/users/{u.id}/likes')

            self.assertIn(b'Access unauthorized.', response.data)