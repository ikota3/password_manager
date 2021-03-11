import random
import model
import logger
import pyperclip
from dearpygui import core
from cryption import decrypt
from constants import WINDOW_HEIGHT


ROW_ID_COLUMN = 0


def format_password(password: str) -> str:
    """Shuffle the password.

    Args:
        password (str): password string

    Returns:
        str: Shuffled password
    """
    return ''.join(random.sample(password, len(password)))[:10]


def update_password_table():
    """Update password table contents.

    Clear the all contents in the password table,
    and recreate table entirely.
    """

    core.clear_table('##password_table')

    try:
        password_infos = model.select_all_items()
    except Exception:
        logger.add_error_message('Failed to fetch passwords.')
        return

    if password_infos:
        for password_info in password_infos:
            core.add_row('##password_table', [
                password_info.row_id,
                password_info.title,
                password_info.identifier,
                format_password(password_info.password.decode()),
                password_info.note,
            ])
    logger.add_info_message('Password table was updated.')


def delete_password_table(_, is_yes: bool):
    """Delete password table contents.

    Args:
        is_yes (bool): Yes(True) or No(False) which user select on the popup
    """
    core.close_popup("##ask_delete")
    if not is_yes:
        return

    try:
        model.delete_all_items()
    except Exception:
        logger.add_error_message('Failed to delete all passwords.')
        return

    logger.add_info_message('All passwords was deleted successfully.')

    update_password_table()


def table_printer(table_name):
    selected_cells = core.get_table_selections(table_name)
    if selected_cells and len(selected_cells) == 1:
        cell_row = selected_cells[0][0]
        row_id = str(core.get_table_item(table_name, cell_row, ROW_ID_COLUMN))

        password_info = model.PasswordInfo(row_id=row_id)
        try:
            encrypted_password = model.select_password_by_row_id(password_info)
        except Exception:
            logger.add_error_message('Failed to get password.')
            return

        decrypted_password = decrypt(encrypted_password)
        pyperclip.copy(decrypted_password)

        logger.add_info_message(f'Row id: {row_id}\'s password was copied to clipboard.')
