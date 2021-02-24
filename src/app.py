import random
import pyperclip
from dearpygui import core, simple
from cryption import encrypt, decrypt
from datetime import datetime
import model

DEBUG_MODE = False

VERSION = 1.0
TITLE = 'Password Manager'
RESIZABLE = True
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 900
ITEM_WIDTH = int(WINDOW_WIDTH * 0.96)
SCROLL_BAR_SIZE = 10.0

FONT = 'font/FiraCode-Medium.ttf'
FONT_SIZE = 15

DEFAULT_THEME = 'Cherry'


def update_theme(theme):
    """Update theme.

    Args:
        theme (str): theme name
    """
    core.set_theme(theme)


def save_password():
    """Save password info to database.
    """
    title = core.get_value('##title')
    identifier = core.get_value('##identifier')
    password = core.get_value('##password')
    note = core.get_value('##note')

    is_valid = True
    if not title:
        add_error_message('Title is required. Please set the Title.')
        is_valid = False
    if not identifier:
        add_error_message('Identifier is required. Please set the Identifier.')
        is_valid = False
    if not password:
        add_error_message('Password is required. Please set the Password')
        is_valid = False

    if not is_valid:
        return

    password_info = model.PasswordInfo(
        title=title,
        identifier=identifier,
        password=encrypt(password),
        note=note
    )
    model.insert_one_item(password_info)
    add_info_message('Password was saved successfully.')
    update_password_table()


def clear_input():
    """Clear input
    """
    core.set_value('##title', '')
    core.set_value('##identifier', '')
    core.set_value('##password', '')
    core.set_value('##note', '')


def add_info_message(message: str):
    """Log message for info.

    Args:
        message (str): message to display
    """
    core.log_info(message, logger='##log_message')


def add_error_message(message: str):
    """Log message for error.

    Args:
        message (str): message to display
    """
    core.log_error(message, logger='##log_message')


def clear_log():
    """Clear log
    """
    core.clear_log(logger='##log_message')


def format_password(password: str) -> str:
    """Shuffle the password.

    Args:
        password (str): password string

    Returns:
        str: shuffled password
    """
    return ''.join(random.sample(password, len(password)))[:10]


def update_password_table():
    """Update password table contents.

    Clear the all contents in the password table,
    and recreate table entirely.
    """
    if not core.does_item_exist('##password_table'):
        header = ['No', 'Title', 'Identifier', 'Password', 'Note']
        core.add_table('##password_table', header, callback=table_printer, width=ITEM_WIDTH, height=int(WINDOW_HEIGHT * 0.45))

    core.clear_table('##password_table')
    password_infos = model.select_all_items()
    if password_infos:
        for password_info in password_infos:
            core.add_row('##password_table', [
                password_info.row_id,
                password_info.title,
                password_info.identifier,
                format_password(password_info.password.decode()),
                password_info.note,
            ])
    add_info_message('Password table was updated.')


def delete_password_table(_, is_yes: bool):
    """Delete password table contents.

    Args:
        is_yes (bool): Yes(True) or No(False) which user select on the popup
    """
    core.close_popup("Are you sure to continue?##ask_delete")
    if not is_yes:
        return

    model.delete_all_items()
    add_info_message('All passwords was deleted successfully.')

    update_password_table()


def table_printer(table_name):
    selected_cells = core.get_table_selections(table_name)
    if selected_cells and len(selected_cells) == 1:
        cell_row = selected_cells[0][0]
        row_id_column = 0
        row_id = str(core.get_table_item(table_name, cell_row, row_id_column))
        password_info = model.PasswordInfo(row_id=row_id)
        decrypted_password = decrypt(model.select_password_by_row_id(password_info))
        pyperclip.copy(decrypted_password)
        add_info_message(f'Row id: {row_id}\'s password was copied to clipboard.')
        return


# NOTE THIS FUNCTION WILL BE CALLED EVERY FRAME
# By setting core.set_render_callback(apply_centering)
def apply_centering():
    items = list(core.get_data("item_center_list"))
    if items:
        for item in items:
            container_width = core.get_item_rect_size(core.get_item_parent(item))[0]
            item_width, item_height = core.get_item_rect_size(item)
            simple.set_item_height(f'{item}_container', int(item_height))
            pos = int((container_width / 2) - (item_width / 2))
            simple.set_item_width(f'{item}_dummy', pos)


# Center widget
# TODO NEED TO FIX
def center_item(name: str):
    with simple.child(f'{name}_container', autosize_x=True, no_scrollbar=True, border=False):
        core.add_dummy(name=f'{name}_dummy')
        core.add_same_line(name=f'{name}_sameline')
        core.move_item(name, parent=f'{name}_container')
    items = list(core.get_data('item_center_list'))
    items.append(name)
    core.add_data('item_center_list', items)
    y_space = core.get_style_item_spacing()[1]
    core.set_item_style_var(f'{name}_container', core.mvGuiStyleVar_ItemSpacing, [0, y_space])


def show_version():
    """Show version of this app.
    """
    with simple.window('Version Info##version_info_window', autosize=True, x_pos=int((WINDOW_WIDTH // 2) * 0.9), y_pos=int((WINDOW_HEIGHT // 2) * 0.9), on_close=lambda: core.delete_item('Version Info##version_info_window')):
        core.add_text('##version_info_0', default_value=f'Password Manager v{VERSION}')


def main():

    center_items = []
    core.add_data('item_center_list', center_items)

    with simple.window(TITLE, x_pos=0, y_pos=0):
        with simple.menu_bar('Menu bar'):
            with simple.menu('File'):
                # core.add_menu_item('Import', callback=None)
                # core.add_menu_item('Export', callback=None)
                with simple.menu('Theme'):
                    themes = ['Dark', 'Light', 'Classic', 'Dark 2', 'Grey', 'Dark Grey', 'Cherry', 'Purple', 'Gold', 'Red']
                    for theme in themes:
                        core.add_menu_item(theme, callback=update_theme)
                # core.add_menu_item('Exit', callback=None)
            with simple.menu('About'):
                # core.add_menu_item('Help', callback=None)
                # TODO IF CLICK 2 TIMES, THE VERSION INFO WINDOW WILL BE BIT WEIRD
                core.add_menu_item('Version', callback=show_version)

        with simple.group('##input_group'):
            # Title input
            core.add_text('Title:')
            core.add_input_text('##title', hint='Enter title', width=ITEM_WIDTH)
            core.add_spacing(count=2)

            # Identifier input
            core.add_text('Identifier:')
            core.add_input_text('##identifier', hint='Enter identifier', width=ITEM_WIDTH)
            core.add_spacing(count=2)

            # Password input
            core.add_text('Password:')
            core.add_input_text('##password', hint='Enter password', width=ITEM_WIDTH)
            core.add_spacing(count=2)

            # Note input
            core.add_text('Note:')
            core.add_input_text('##note', hint='Enter note info', width=ITEM_WIDTH)
            core.add_spacing(count=10)

            # Save button
            spacing = 20
            core.add_button('Save', callback=save_password, width=(ITEM_WIDTH - spacing) // 2)
            core.add_same_line(spacing=20)

            # Clear input entry button
            core.add_button('Clear input##clear_input', callback=clear_input, width=(ITEM_WIDTH - spacing) // 2)
            core.add_spacing(count=20)

        with simple.group('##log_group'):
            # Log label
            core.add_text('Log message:')
            core.add_spacing(count=10)

            # Logger
            core.add_logger('##log_message', width=ITEM_WIDTH, height=100, auto_scroll_button=False, copy_button=False, filter=False, clear_button=False)
            core.set_log_level(core.mvTRACE, logger='##log_message')
            core.add_spacing(count=10)

            # Clear log button
            core.add_button('Clear log##clear_log', callback=clear_log, width=ITEM_WIDTH)
            core.add_spacing(count=10)

        with simple.group('##password_table_group'):
            # Password table
            update_password_table()
            core.add_spacing(count=10)

            # Update password table button
            core.add_button('Update table', callback=update_password_table, width=(ITEM_WIDTH - spacing) // 2)
            core.add_same_line(spacing=20)

            # Delete password table button
            core.add_button('Delete table', width=(ITEM_WIDTH - spacing) // 2)
            with simple.popup('Delete table', 'Are you sure to continue?##ask_delete', mousebutton=core.mvMouseButton_Left, modal=True):
                with simple.group('##delete_table_button_group'):
                    core.add_text('##delete_table_button', default_value='Are you sure to delete all data?')
                    core.add_button('##delete_table_button_yes', label='Yes', callback=delete_password_table, callback_data=True)
                    core.add_same_line(spacing=10)
                    core.add_button('##delete_table_button_no', label='No', callback=delete_password_table, callback_data=False)
                    # TODO WONT WORK NEED TO FIX center_item FUNCTION
                    # center_item('##delete_table_button')
                    # center_item('##delete_table_button_yes')
                    # center_item('##delete_table_button_no')
                # center_item('##delete_table_button_group')

    if DEBUG_MODE:
        # core.show_logger()
        simple.show_debug()
        # simple.show_documentation()

    # Common Configuration
    core.set_theme(DEFAULT_THEME)
    core.add_additional_font(FONT, FONT_SIZE)
    core.set_main_window_title(TITLE)
    core.set_main_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    core.set_main_window_resizable(RESIZABLE)
    core.set_style_scrollbar_size(SCROLL_BAR_SIZE)

    core.set_exit_callback(model.close_connection)

    # core.set_render_callback(apply_centering)
    core.start_dearpygui(primary_window=TITLE)


if __name__ == '__main__':
    main()
