"""
Provides a basic frontend
"""
import sys
import main

from loguru import logger

logger.remove()
logger.add('loguru_file_{time:YYYY-MM-DD}.log', level='DEBUG')
logger.add(sys.stderr, level='WARNING')


def load_accounts_csv_to_db(uc_instance):
    """
    Loads user accounts from a file
    """
    filename = input('Enter filename of user file: ')
    main.load_accounts_csv_to_db(filename, uc_instance)


def load_status_csv_to_db(sc_instance):
    """
    Loads status updates from a file
    """
    filename = input('Enter filename for status file: ')
    main.load_status_csv_to_db(filename, sc_instance)


def add_user(uc_instance):
    """
    Adds a new user into the database
    """
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    logger.info(f"Calling add_user with user_id")
    logger.debug(f"add_user parameter user_id: {user_id}")
    if not main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name,
                         uc_instance):
        logger.error("An error occurred while trying to add new user")
        print("An error occurred while trying to add new user")
    else:
        logger.debug("User was successfully added")
        print("User was successfully added")


def delete_user(uc_instance):
    """
    Deletes user from the database
    """
    user_id = input("Enter the user_id of the user to delete: ")
    if not main.delete_user(user_id, uc_instance):
        logger.debug(f'{user_id} does not exist')
        print(f"Failed to remove {user_id}. Does not exist!")
    else:
        logger.debug(f'{user_id} deleted')
        print(f"Removed {user_id}")


def search_user(uc_instance):
    """
    Searches a user in the database
    """
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, uc_instance)
    logger.debug(result)
    if result is None:
        logger.error("ERROR: User does not exist")
        print("ERROR: User does not exist")
    else:
        logger.debug(f"User ID: {result.user_id}")
        print(f"User ID: {result.user_id}")
        logger.debug(f"Email: {result.email}")
        print(f"Email: {result.email}")
        logger.debug(f"Name: {result.user_name}")
        print(f"Name: {result.user_name}")
        logger.debug(f"Last name: {result.user_last_name}")
        print(f"Last name: {result.user_last_name}")


def update_email(uc_instance):
    """
    Updates information for an existing user
    """
    user_id = input("Enter the user_id of the user whose information you wish to update: ")
    email = input("Enter their new email address: ")
    if not main.update_email(user_id, email, uc_instance):
        logger.error("An error occurred while trying to update user email")
        print(f"Failed to update to {email}")
    else:
        logger.debug("User email was successfully updated")
        print(f"{user_id}'s new email is now {email}")


def add_status(sc_instance):
    """
    Adds a new status into the database
    """
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(status_id, user_id, status_text, sc_instance):
        logger.error("An error occurred while trying to add new status")
        print("An error occurred while trying to add new status")
    else:
        logger.debug("New status was successfully added")
        print("New status was successfully added")


def delete_status(sc_instance):
    """
    Deletes status from the database
    """
    status_id = input("Enter the status_id of the status to delete: ")
    if not main.delete_status(status_id, sc_instance):
        logger.error("An error occurred while trying to delete status")
        print("An error occurred while trying to delete status")
    else:
        logger.debug("Status was successfully deleted")
        print("Status was successfully deleted")


def search_status(sc_instance):
    """
    Searches a status in the database
    """
    status_id = input("Enter a status_id to search for status: ")
    status = main.search_status(status_id, sc_instance)
    if status is not None:
        # return status.status_id, status.user_id, status.status_text
        print(
            f"{status.status_id} from {status.user_id} has status(es): {status.status_text}."
        )
    else:
        logger.error("ERROR: Status does not exist")
        print(f"{status_id} was not found")


def update_status(sc_instance):
    """
    Updates information for an existing status
    """
    status_id = input("Enter the status_id of the status you wish to update: ")
    status_text = input("Enter a new status text: ")
    result = main.update_status(status_id, status_text, sc_instance)
    if result:
        print(f"{status_id}'s new status is now {status_text}")
        logger.error("An error occurred while trying to update status")
    else:
        print(f"Failed to update to {status_id}")
        logger.debug("Status was successfully updated")


def quit_program():
    """
    Quits program
    """
    sys.exit()


if __name__ == "__main__":
    user_collection_instance = main.init_user_collection()
    status_collection_instance = main.init_status_collection()
    while True:
        user_input = input(
            '1. Add user\n2. Search user\n3. Delete user\n4. Update email\n'
            '5. Add status\n6. Search status\n7. Delete status\n8. Update status text\n'
            '9. Load user data to database\n10. Load status data to database\n11. Exit\nEnter option: ')
        if user_input == "1":
            add_user(user_collection_instance)
        elif user_input == "2":
            search_user(user_collection_instance)
        elif user_input == "3":
            delete_user(user_collection_instance)
        elif user_input == "4":
            update_email(user_collection_instance)
        elif user_input == "5":
            add_status(status_collection_instance)
        elif user_input == "6":
            search_status(status_collection_instance)
        elif user_input == "7":
            delete_status(status_collection_instance)
        elif user_input == "8":
            update_status(status_collection_instance)
        elif user_input == "9":
            load_accounts_csv_to_db( user_collection_instance)
        elif user_input == "10":
            load_status_csv_to_db(status_collection_instance)
        elif user_input == "11":
            sys.exit(0)
        else:
            print("Did not understand input")