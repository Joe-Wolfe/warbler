"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

from app import app
import os
from unittest import TestCase
from models import db, User
from sqlalchemy.exc import IntegrityError

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""


class UserModelTestCase(TestCase):
    """Test model for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_is_following(self):
        u1 = User.signup("test1", "test1@test.com", "password", None)
        u1.id = 11111
        u2 = User.signup("test2", "test2@test.com", "password", None)
        u2.id = 22222
        u3 = User.signup("test3", "test3@test.com", "password", None)
        u3.id = 33333
        db.session.commit()

        u1.following.append(u2)
        db.session.commit()

        self.assertEqual(len(u1.following), 1)
        self.assertEqual(len(u2.followers), 1)
        self.assertEqual(len(u3.following), 0)
        self.assertEqual(u1.following[0].id, u2.id)
        self.assertEqual(u2.followers[0].id, u1.id)
        self.assertNotEqual(u1.following[0].id, u3.id)

    def test_is_followed_by(self):
        u1 = User.signup("test1", "test1@test.com", "password", None)
        u1.id = 11111
        u2 = User.signup("test2", "test2@test.com", "password", None)
        u2.id = 22222
        u3 = User.signup("test3", "test3@test.com", "password", None)
        u3.id = 33333
        db.session.commit()

        u1.following.append(u2)
        db.session.commit()

        self.assertEqual(len(u1.following), 1)
        self.assertEqual(len(u2.followers), 1)
        self.assertEqual(len(u3.following), 0)
        self.assertEqual(u1.following[0].id, u2.id)
        self.assertEqual(u2.followers[0].id, u1.id)
        self.assertNotEqual(u1.following[0].id, u3.id)

    def test_user_signup(self):
        test_user = User.signup("testuser", "test@test.com", "password", None)
        db.session.commit()

        test_user_in_db = User.query.get(test_user.id)

        self.assertIsNotNone(test_user_in_db)
        self.assertEqual(test_user_in_db.username, "testuser")
        self.assertEqual(test_user_in_db.email, "test@test.com")
        self.assertNotEqual(test_user_in_db.password, "password")
        self.assertTrue(test_user_in_db.password.startswith("$2b$"))

    def test_user_invalid_username_signup(self):
        test_user = User.signup(None, "", "password", None)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_user_authenticate(self):

        test_user = User.signup("testuser", "test@test.com", "password", None)
        user = User.authenticate("testuser", "password")

        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@test.com")

    def test_user_invalid_username_authenticate(self):

        test_user = User.signup("testuser", "test@test.com", "password", None)
        user = User.authenticate("badusername", "password")
        self.assertFalse(user)

    def test_user_invalid_password_authenticate(self):

        test_user = User.signup("testuser", "test@test.com", "password", None)
        user = User.authenticate("testuser", "badpassword")
        self.assertFalse(user)
