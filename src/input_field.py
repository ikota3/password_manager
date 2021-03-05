import model
import logger
import table
from dearpygui import core
from cryption import encrypt
from app import TITLE_ID, IDENTIFIER_ID, PASSWORD_ID, NOTE_ID


def save_password():
    """Save password info to database.
    """
    title = core.get_value(TITLE_ID)
    identifier = core.get_value(IDENTIFIER_ID)
    password = core.get_value(PASSWORD_ID)
    note = core.get_value(NOTE_ID)

    is_valid = True
    if not title:
        logger.add_error_message('Title is required. Please set the Title.')
        is_valid = False
    if not identifier:
        logger.add_error_message('Identifier is required. Please set the Identifier.')
        is_valid = False
    if not password:
        logger.add_error_message('Password is required. Please set the Password')
        is_valid = False

    if not is_valid:
        return

    password_info = model.PasswordInfo(
        title=title,
        identifier=identifier,
        password=encrypt(password),
        note=note
    )

    try:
        model.insert_one_item(password_info)
    except Exception:
        core.add_error_message('Failed to save password.')
        return

    logger.add_info_message('Password was saved successfully.')
    table.update_password_table()


def clear_input():
    """Clear input
    """
    core.set_value(TITLE_ID, '')
    core.set_value(IDENTIFIER_ID, '')
    core.set_value(PASSWORD_ID, '')
    core.set_value(NOTE_ID, '')
