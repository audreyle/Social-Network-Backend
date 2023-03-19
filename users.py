"""Methods available to the User class"""
# pylint: disable=R0903
import sys
from peewee import IntegrityError, DoesNotExist

from loguru import logger

from socialnetwork_model import UsersTable

logger.remove()
logger.add('loguru_file_{time:YYYY-MM-DD}.log', level='DEBUG')
logger.add(sys.stderr, level='WARNING')


# A base class that will also contain the database
class BaseCollection:
    """
    Class representing the basic data model for all SqlLite database tables
    """
    def __init__(self, database):
        self.database = database


class UserCollection(BaseCollection):
    """
    Class representing User
    """

    def add_user(self, user_id, user_name, user_last_name, email):
        """
        Adds a new user to the collection
        """
        try:
            # .transaction() acts like a context manager
            with self.database.transaction():
                new_user = UsersTable.create(
                    user_id=user_id,
                    user_name=user_name,
                    user_last_name=user_last_name,
                    email=email
                )
                new_user.save()
                print(f"Success adding user {user_id}")
                logger.info("Success adding user")
            return True
        except IntegrityError:
            print(f'{user_id} already exists in the database!')
            logger.error("User already exists in the database!")
            return False

    def search_user(self, user_id):
        """
        Searches for user data. We search by user_id because it is our primary key in
        UsersTable. We pass it the parameter user_id.
        """
        try:
            with self.database.transaction():
                # Find a user by their user_id.
                result = UsersTable.get(UsersTable.user_id == user_id)
                logger.info(f"Found user! {user_id}")
            return result
        # Catches any errors not finding this record
        except DoesNotExist:
            logger.error(f'{user_id} does not exist in the database!')
            return None

    def delete_user(self, user_id):
        """
        Deletes an existing user
        """
        try:
            with self.database.transaction():
                # Find a person with the same name
                result = UsersTable.get(UsersTable.user_id == user_id)
                # Deletes it
                result.delete_instance()
                logger.info(f"Success deleting {user_id}")
            return True
        # Catches any errors not finding this record
        except DoesNotExist:
            logger.error(f'Cannot delete user because {user_id} does not exist in the database!')
            return False

    def update_email(self, user_id, email):
        """
        Modifies an existing user
        """
        try:
            with self.database.transaction():
                # Find the person
                result = UsersTable.get(UsersTable.user_id == user_id)
                # Update fields
                result.email = email
                # Save it in the db
                result.save()
                logger.info(f"Successly updated email for {user_id} to {email}")
            return True
        except DoesNotExist:
            logger.error(f'Cannot update email because {user_id} does not exist in the database!')
            return False
