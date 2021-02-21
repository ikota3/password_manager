from dearpygui import core, simple
from cryption import encrypt, decrypt
import model

DEBUG_MODE = False

VERSION = 1.0
TITLE = 'Password Manager'
WIDTH = 720
HEIGHT = 860
# PADDING = 100
RESIZABLE = True

FONT = 'font/FiraCode-Medium.ttf'
FONT_SIZE = 15

DEFAULT_THEME = 'Cherry'


def add_log_message(message):
    core.log(message, logger='log_message')


def save_callback(sender, data):
    title = core.get_value('title')
    identifier = core.get_value('identifier')
    password = core.get_value('password')
    note = core.get_value('note')

    if not title:
        add_log_message('[ERROR] Title has not been set.\n')
        return
    if not identifier:
        add_log_message('[ERROR] Identifier has not been set.\n')
        return
    if not password:
        add_log_message('[ERROR] Password has not been set.\n')
        return

    password_info = model.Password_Info(
        title=title,
        identifier=identifier,
        password=encrypt(password),
        note=note
    )
    model.insert_one_item(password_info)


def update_password_list():
    if not core.does_item_exist('Password_table'):
        core.add_table('Password_table', [
            'ROW_ID', 'Title', 'Identifier', 'Password', 'Note', 'Created At', 'Updated At'
        ])

    # TODO Get max char of each column, and set to each width.
    # ? set_managed_column_width
    core.clear_table('Password_table')
    password_infos = model.select_all_item()
    if password_infos:
        for password_info in password_infos:
            print(f'app.py: {type(password_info.password)}')
            core.add_row('Password_table', [
                password_info.row_id,
                password_info.title,
                password_info.identifier,
                password_info.password.decode(),
                password_info.note,
                password_info.created_at,
                password_info.updated_at
            ])


# def table_printer(sender, data):
#     core.log_debug(f'sender is {sender}')
    # coord_list = core.get_table_data(sender)
    # for coordinates in coord_list:
    #     core.log_debug(core.get_table_item(sender, coordinates[0], coordinates[1]))


def main():
    core.set_main_window_size(WIDTH, HEIGHT)
    core.set_main_window_resizable(RESIZABLE)
    core.set_theme(DEFAULT_THEME)
    core.add_additional_font(FONT, FONT_SIZE)
    core.set_exit_callback(model.close_connection)

    if DEBUG_MODE:
        core.show_logger()
        simple.show_debug()

    with simple.window(TITLE):
        with simple.menu_bar('Menu bar'):
            with simple.menu('File'):
                core.add_menu_item('Import', callback=None)
                core.add_menu_item('Export', callback=None)
                core.add_menu_item('Exit', callback=None)
                with simple.menu('Theme'):
                    core.add_menu_item('Dark')
            with simple.menu('About'):
                core.add_menu_item('Help', callback=None)
                core.add_menu_item('Version info', callback=None)

        # Title
        core.add_text('Title:')
        core.add_input_text('title', hint='Enter title', label='')
        core.add_spacing(count=2)

        # Identifier
        core.add_text('Identifier:')
        core.add_input_text('identifier', hint='Enter identifier', label='')
        core.add_spacing(count=2)

        # Password
        core.add_text('Password:')
        core.add_input_text('password', hint='Enter password', label='')
        core.add_spacing(count=2)

        # Note
        core.add_text('Note:')
        core.add_input_text('note', hint='Enter note info', label='')
        core.add_spacing(count=10)

        # Save button
        core.add_button('Save', callback=save_callback)
        core.add_spacing(count=10)

        # Log
        core.add_text('Log message:')
        # core.add_input_text('log_message', multiline=True, readonly=True, label='')
        core.add_logger('log_message', width=WIDTH, height=100)
        # core.set_log_level(1, logger='log_message')
        core.add_spacing(count=10)

        # Update password table button
        core.add_button('Update table', callback=update_password_list)
        core.add_spacing(count=10)

        # Password table
        update_password_list()

        # Another method for making label to left side
        # core.add_managed_columns("cols", 2, border=False)
        # core.set_managed_column_width("cols", 0, 100)
        # core.set_managed_column_width("cols", 1, 300)
        # core.add_text("Status:  ")
        # core.add_text("status", default_value="Right side status text")
        # core.add_text("Another field:")
        # core.add_progress_bar("progress")

    core.start_dearpygui(primary_window=TITLE)


if __name__ == '__main__':
    main()
