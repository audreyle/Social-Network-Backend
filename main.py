"""
main driver for a simple social network project
"""
import sys
from csv import DictReader

from loguru import logger
import user_status
import users
from socialnetwork_model import database

logger.remove()
logger.add('loguru_file_{time:YYYY-MM-DD}.log', level='DEBUG')
logger.add(sys.stderr, level='WARNING')

logger.debug("This is a debug")
logger.info("This is an info")
logger.warning("This is a warning")
logger.error("This is an error")


def init_user_collection():
    """
    Creates and returns a new instance of UserCollection
    """
    return users.UserCollection(database)


def init_status_collection():
    """
    Creates and returns a new instance of UserStatusCollection
    """
    return user_status.UserStatusCollection(database)


def load_accounts_csv_to_db(file, uc_instance):
    """
    Opens a CSV file with user data,
    adds it to an existing instance of
    UserCollection, then loads it to UsersTable
    crated in our SqlLite database instance

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if the file can't be found
    - Otherwise, it returns True.
    """
    try:
        with open(file, "r", encoding="utf-8") as user_file:
            reader = DictReader(user_file)
            for row in reader:
                uc_instance.add_user(
                    row["USER_ID"],
                    row["NAME"],
                    row["LASTNAME"],
                    row["EMAIL"]
                )
        logger.info("Successfully loaded users to database.")
        return True
    except FileNotFoundError as error:
        logger.error(f'Detailed error message: {error}')
        print(f'Detailed error message: {error}')
        return False


def load_status_csv_to_db(file, sc_instance):
    """
    Opens a CSV file with status data,
    adds it to an existing instance of
    UserStatusCollection, then loads it to UserStatusTable
    created in our SqlLite database instance

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if the file can't be found
    - Otherwise, it returns True.
    """
    try:
        with open(file, "r", encoding="utf-8") as status_file:
            reader = DictReader(status_file)
            for row in reader:
                sc_instance.add_status(
                    row["STATUS_ID"],
                    row["USER_ID"],
                    row["STATUS_TEXT"]
                )
        logger.info("Successfully loaded status data to database.")
        return True
    except FileNotFoundError as error:
        logger.error(f'Detailed error message: {error}')
        print(f'Detailed error message: {error}')
        return False


def add_user(user_id, user_name, user_last_name, email, uc_instance):
    """
    Takes all the user inputs from menu.py and creates a new instance of User
    in user_collection, which are then written in UsersTable into our database.

    Requirements:
    - user_id cannot already exist in the database.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    """
    return uc_instance.add_user(user_id, user_name, user_last_name, email)


def delete_user(user_id, uc_instance):
    """
    Deletes a user from our user_collection instance and updates
    UsersTable in our SqlLite database.
    Automatically deletes the status messages associated with that
    user in the UserStatusTable.

    Requirements:
    - Returns None if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    """
    return uc_instance.delete_user(user_id)


def search_user(user_id, uc_instance):
    """
    Searches for a user in our user_collection instance.

    Requirements:
    - If the user is found in UsersTable, returns the corresponding User instance.
    - Otherwise, it returns None.
    """
    user = uc_instance.search_user(user_id)
    if user is None:
        return None
    return user


def update_email(user_id, email, uc_instance):
    """
    Updates the email value of an existing user and saves the change in
    UsersTable.

    Requirements:
    - Returns False if it can't find the user in the database.
    - Otherwise, it returns True once it's made the changes.
    """
    return uc_instance.update_email(user_id, email)


def add_status(status_id, user_id, status_text, sc_instance):
    """
    Creates a new instance of UserStatus and stores it in our UserStatus
    collection instance, which is then written to the UserStatusTable
    in our SqlLite database.

    Requirements:
    - Returns False if the user does not exist.
    - Returns True if successful.
    """
    return sc_instance.add_status(status_id, user_id, status_text)


def delete_status(status_id, sc_instance):
    """
    Delete a status in our status_collection instance.

    Requirements:
    - If the status_id can't be found in the database, returns
    False
    - Otherwise, it returns True.
    """
    return sc_instance.delete_status(status_id)


def search_status(status_id, sc_instance):
    """
    Searches for a status in our status_collection instance.

    Requirements:
    - If the status_id exists in UserStatusTable,
    returns the corresponding UserStatus instance.
    - Otherwise, it returns None.
    """
    return sc_instance.search_status(status_id)


def update_status(status_id, status_text, sc_instance):
    """
    Updates a status text if status_id exists.
    Returns True if successful.
    Returns False if the status_id does not exist
    """
    return sc_instance.update_status_text(status_id, status_text)
