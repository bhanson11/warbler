"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

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

    ### test following

    def test_user_follows(self):
        """testing following functionality"""

        # if test u1 follows u2 is that successful?
        self.u1.following.append(self.u2)
        db.session.commit()

        # if u1 follows u2 does it show that u1 is following u2?
        

        # if u1 is not following u2 is that successfully detected?

        # does u2 show u1 as a follower correctly?
        
        # does u2 show u1 not as a follower correctly? 
        
        # 