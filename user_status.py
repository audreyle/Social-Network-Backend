"""
classes to manage the user status messages
"""
import sys
from peewee import IntegrityError, DoesNotExist

from loguru import logger

from socialnetwork_model import UserStatusTable

logger.remove()
logger.add('loguru_file_{time:YYYY-MM-DD}.log', level='DEBUG')
logger.add(sys.stderr, level='WARNING')


class UserStatusCollection:
    """
    class to hold status message data
    """

    def __init__(self, database):
        self.database = database

    def add_status(self, status_id, user_id, status_text):
        """
        add a status to the collection
        """
        try:
            with self.database.transaction():
                new_status = UserStatusTable.create(
                    status_id=status_id,
                    user_id=user_id,
                    status_text=status_text,
                )
                new_status.save()
                print(f"Saved {user_id} 's {status_id}: {status_text} to UserStatusTable")
                logger.info(f"Successfully added a status for {user_id}")
            return True
        # Catch any errors with duplicate keys (status_id)
        except IntegrityError:
            print(f'Doh! Did you forget to add {user_id} as a user beforehand?')
            logger.error(f"Failed to add {user_id} as a user before adding their status.")
            return False

    def search_status(self, status_id):
        """
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        """
        try:
            with self.database.transaction():
                # Find a status by its status_id
                result = UserStatusTable.get(UserStatusTable.status_id == status_id)
                logger.info(f"Found this status for {status_id}: ")
            return result
        # Catches any errors not finding this record
        except DoesNotExist:
            logger.error(f'{status_id} does not exist in the UserStatus database!')
            return None

    def delete_status(self, status_id):
        """
        deletes the status message with id, status_id
        """
        try:
            with self.database.transaction():
                # Find the status going by this status_id
                result = UserStatusTable.get(UserStatusTable.status_id == status_id)
                # Deletes it
                result.delete_instance()
                print(f"Removed {status_id}")
                logger.info(f"Successfully deleted {status_id}")
            return True
        # Catches any errors not finding this record
        except DoesNotExist:
            print(f'Could not delete {status_id} because it does not exist.')
            logger.error(f'There is no {status_id} in existence in the UserStatus database '
                         f'to delete.')
            return False

    def update_status_text(self, status_id, status_text):
        """
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        """
        try:
            with self.database.transaction():
                # Find the status by its id
                result = UserStatusTable.get(UserStatusTable.status_id == status_id)
                # Update the status text
                result.status_text = status_text
                # Save it in the db
                result.save()
                logger.info(f'Successfully updated the status text for {status_id}')
            return True
        # Catches any errors not finding this record
        except DoesNotExist:
            logger.error(f'There is no {status_id} in the UserStatus database to update.')
            return False
