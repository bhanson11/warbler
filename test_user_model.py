"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        #drop all tables and then recreate them all for clean test environment between tests
        db.drop_all()
        db.create_all()

        #create test users
        u1 = User.signup("testuser1", "test1@test.com", "password", None)
        u2 = User.signup("testuser2", "test2@test.com", "password", None)

        #assign ID's to test users
        u1.id = 1234
        u2.id = 5678

        db.session.commit()

        #store users as variables for us in tests                
        self.u1 = User.query.get(1234)
        self.u2 = User.query.get(5678)

        # set up test client
        self.client = app.test_client()
    
    def tearDown(self):
        """teardown to reset to clean test environment"""
        reset = super().tearDown()
        db.session.rollback()
        return reset

    def test_user_model(self):
        """Does basic model work? Test repr"""

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

    ### test following

    def test_user_follows(self):
        """testing following functionality"""

        # Does is_following successfully detect when user1 is following user2?
        self.u1.following.append(self.u2)
        db.session.commit()
        # if u1 follows u2 does it show that u1 is following u2?
        self.assertTrue(self.u1.is_following(self.u2))
        

    def test_user_is_following(self):
        # if u1 is not following u2 is that successfully detected or vice versa?
        self.u1.following.append(self.u2)
        db.session.commit()
        # does u2 show u1 as a follower correctly?
        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))
        
    def test_user_is_followed_by(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u2.is_folowed_by(self.u1))
        self.assertFalse(self.u1.is_followed_by(self.u2))

    ### sign up tests ###

    def test_valid_signup(self):
        test_u = User.signup("testnewuser", "testingnewuser@testy.com", "password", None)
        test_u.id = 11111
        db.session.commit()

        test_u = User.query.get(test_u.id)
        self.assertIsNotNone(test_u.id)
        self.assertEqual(test_u.username, "testnewuser")
        self.assertEqual(test_u.email, "testingnewuser@testy.com")
    
    def test_invalid_username_signup(self):
        invalidu = User.signup(None, "testiuser@test.com", "password", None)
        invalidu.id = 5678910
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalide = User.signup("testemail", None, "password", None)
        invalide.id = 1235773
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testpass", "password@email.com", "", None)

        with self.assertRaises(ValueError) as context: 
            User.signup("testpass", "password@email.com", None, None)

