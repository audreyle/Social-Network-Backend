"""
Unit testing methods in UserStatus class
"""
from unittest import TestCase

from peewee import SqliteDatabase
from socialnetwork_model import UserStatusTable, UsersTable
from user_status import UserStatusCollection
from users import UserCollection


class TestUserStatusCollection(TestCase):
    """
    Creating a test User class for testing methods in UserStatus class
    """
    def setUp(self):
        """
        Create a mock database to avoid using users.db during testing
        """
        self.database = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})
        # Bind UserStatusTable to this test database instead of users.db
        self.database.bind([UserStatusTable, UsersTable])
        # Connect and create the test table using the data model for UserStatusTable
        self.database.connect()
        self.database.create_tables([UserStatusTable, UsersTable])
        # Seeding data
        self.user_collection = UserCollection(self.database)
        self.user_collection.add_user("peterpan1", "Peter", "Pan", "peter.pan1@gmail.com")
        self.user_collection.add_user("jerry.tom1", "Jerry", "Mouse", "jerry.tom1@gmail.com")
        self.user_collection.add_user("scooby.doo1", "Scooby", "Doo", "scooby.doo1@gmail.com")
        self.user_collection.add_user("king.arthur", "Arthur", "Pendagron", "king.arthur@gmail.com")
        scooby_user = self.user_collection.search_user("scooby.doo1")
        king_arthur_user = self.user_collection.search_user("king.arthur")
        self.status_collection = UserStatusCollection(self.database)
        self.status_collection.add_status("scooby.doo1_00001", scooby_user, "Scooby, Scooby Dooo!")
        self.status_collection.add_status("king.arthur_00001", king_arthur_user,
                                          "I live for honor")

    def tearDown(self):
        """
        Disconnect test databases
        """
        self.database.drop_tables([UserStatusTable, UsersTable])
        self.database.close()

    def test_add_status_to_user_success(self):
        """
        Testing add_status in user_status.py
        """
        # since we already created the user peterpan1 in SetUp, we don't go straight
        # to adding a status and it should work
        status_id = "peterpan1_00003"
        user_id = "peterpan1"
        status_text = "Come with me when dreams are born and time is never planned."
        self.assertTrue(self.status_collection.add_status(status_id, user_id, status_text))
        result = self.status_collection.search_status(status_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.status_id, status_id)
        self.assertEqual(result.status_text, status_text)

    def test_add_status_to_user_fail(self):
        """
        Testing how add_status in user_status.py fails
        """
        # Adding a status to a user would fail if the status_id was the same
        # Verify that a status object exists by searching for status_id in the database.
        result = self.status_collection.search_status("scooby.doo1_00001")
        self.assertIsNotNone(result)
        self.assertEqual(result.status_text, "Scooby, Scooby Dooo!")
        # now try adding the status with the same status_id
        result2 = self.status_collection.add_status("scooby.doo1_00001", "scooby.doo1",
                                                    "I can't help but sing")
        self.assertFalse(result2)
        # it would also fail if the user_id was deleted
        self.user_collection.delete_user("scooby.doo1")
        result3 = self.status_collection.search_status("scooby.doo1_00001")
        self.assertIsNone(result3)

    def test_search_status_success(self, scooby_user=None):
        """
        Testing search_status in user_status.py
        """
        result = self.status_collection.search_status("scooby.doo1_00001")
        self.assertIsNotNone(result)
        self.assertEqual(result.status_text, "Scooby, Scooby Dooo!")

    def test_search_status_by_user_fail(self):
        """
        Testing how search_status in user_status.py fails
        """
        # fails to find a status if the user has been deleted or doesn't exist
        self.assertFalse(self.status_collection.search_status("shaggy1_00001"))
        # also fails if the user hasn't published anything
        self.user_collection.add_user("velma2", "Velma", "Dinkley", "velma2@gmail.com")
        self.assertFalse(self.status_collection.search_status("velma2"))

    def test_delete_status_by_user_success(self):
        """
        Testing delete_status in user_status.py
        """
        # I'm creating a new user and status to delete for convenience
        # but I could've easily done that in SetUp
        self.user_collection.add_user("velma2", "Velma", "Dinkley", "velma2@gmail.com")
        velma_user = self.user_collection.search_user("velma2")
        self.status_collection.add_status("velma2_00001", velma_user, "Jinkies!")
        result = self.status_collection.search_status("velma2_00001")
        # checking that the binding by user_id works
        self.assertIsNotNone(result)
        self.assertEqual(result.status_text, "Jinkies!")
        # also testing that velma_user has a hidden attribute called user_has_written
        # is created when I make user_id the foreign key in UserStatusTable
        self.assertEqual(velma_user.user_has_written, "velma2_00001")
        # deleting status
        self.status_collection.delete_status("velma2_00001")
        # checking if UserTable no longer has the status
        self.assertFalse(velma_user.user_has_written, "velma2_00001")

    def test_delete_status_by_user_fail(self):
        """
        Testing how delete_status in user_status.py fails
        """
        # we fail to delete a status by the user when the user does not exist
        self.assertFalse(self.status_collection.delete_status("daphne3_00003"))
        # or they haven't published that status
        self.assertFalse(self.status_collection.delete_status("king.arthur_00001"))

    def test_update_status_by_user_success(self):
        """
        Testing update_status_text in user_status.py
        """
        # Just like velma2, I wanted to create a user inside the function to test
        # how the foreign key works more easily
        self.user_collection.add_user("merlin.wizard8", "Merlin", "Wyllt",
                                      "merlin.wizard@gmail.com")
        merlin_user = self.user_collection.search_user("merlin.wizard8")
        self.status_collection.add_status("merlin.wizard8_00001", merlin_user,
                                          "A dark age indeed! Age of inconvenience!")
        result = self.status_collection.search_status("merlin.wizard8_00001")
        # checking this works
        self.assertIsNotNone(result)
        self.assertEqual(result.status_text, "A dark age indeed! "
                                             "Age of inconvenience!")
        # checking backref of foreign key in UserStatusTable, which is the user_id,
        # and produces an attribute called user_has_written that contains the status_id
        self.assertEqual(merlin_user.user_has_written, "merlin.wizard8_00001")
        # now updating status
        self.status_collection.update_status_text("merlin.wizard8_00001",
                                                  "Have you ever considered being a squirrel?")
        # Verify that status_text was changed
        result2 = self.status_collection.search_status("merlin.wizard8_00001")
        self.assertEqual(result2.status_text, "Have you ever considered being a squirrel?")

    def test_update_status_by_user_fail(self):
        """
        Testing how update_status_text in user_status.py fails
        """
        # the test would fail to update the status if we had the wrong status_id
        self.assertFalse(self.status_collection.update_status_text("king.arthur_00002",
                                                                   "I am a squirrel!"))
        # the test would fail to update statuses as well if we deleted the user
        self.user_collection.delete_user("king.arthur")
        self.assertFalse(self.status_collection.update_status_text("king.arthur_00001",
                                                                   "I am legend"))
