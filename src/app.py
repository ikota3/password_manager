import os
import menu
import input_field
import table
import logger
import model
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_PADDING
from dearpygui import core, simple

DEBUG_MODE = False

RESIZABLE = False

TITLE = 'Password Manager'
FONT = os.path.join(os.path.dirname(__file__), '../font/FiraCode-Medium.ttf')
FONT_SIZE = 15
DEFAULT_THEME = 'Cherry'

WIDGET_WIDTH = WINDOW_WIDTH - (WINDOW_PADDING * 2) - 16  # 16...
WIDGET_HALF_WIDTH = (WIDGET_WIDTH // 2)

# INPUT ID CONSTANT
TITLE_ID = '##input_title'
IDENTIFIER_ID = '##input_identifier'
PASSWORD_ID = '##input_password'
NOTE_ID = '##input_note'

# COLOR CONSTANT
RED = (219, 82, 75, 100)
GREEN = (123, 213, 0, 100)
BLUE = (62, 138, 204, 100)


def main():

    center_items = []
    core.add_data('item_center_list', center_items)

    with simple.window(TITLE):
        with simple.menu_bar('##menu_bar'):
            with simple.menu('File'):
                # core.add_menu_item('Import', callback=None)
                # core.add_menu_item('Export', callback=None)
                with simple.menu('Theme'):
                    themes = ['Dark', 'Light', 'Classic', 'Dark 2', 'Grey', 'Dark Grey', 'Cherry', 'Purple', 'Gold', 'Red']
                    for theme in themes:
                        core.add_menu_item(theme, callback=menu.update_theme)
                # core.add_menu_item('Exit', callback=None)
            with simple.menu('About'):
                core.add_menu_item('Version', callback=menu.show_version)

        with simple.group('##input_group'):
            # Title input
            core.add_text('Title:')
            core.add_input_text(TITLE_ID, hint='Enter title', width=WIDGET_WIDTH)
            core.add_spacing(count=2)

            # Identifier input
            core.add_text('Identifier:')
            core.add_input_text(IDENTIFIER_ID, hint='Enter identifier', width=WIDGET_WIDTH)
            core.add_spacing(count=2)

            # Password input
            core.add_text('Password:')
            core.add_input_text(PASSWORD_ID, hint='Enter password', width=WIDGET_WIDTH)
            core.add_spacing(count=2)

            # Note input
            core.add_text('Note:')
            core.add_input_text(NOTE_ID, hint='Enter note info', width=WIDGET_WIDTH)
            core.add_spacing(count=10)

            # Save button
            save_clear_spacing = 50
            core.add_button('##save', label='Save', callback=input_field.save_password, width=WIDGET_HALF_WIDTH - (save_clear_spacing // 2))
            core.set_item_color('##save', core.mvGuiCol_Button, color=GREEN)
            core.add_same_line(spacing=save_clear_spacing)
            # Clear input entry button
            core.add_button('##clear_input', label='Clear input', callback=input_field.clear_input, width=WIDGET_HALF_WIDTH - (save_clear_spacing // 2))
            core.add_spacing(count=20)

        with simple.group('##log_group'):
            # Logger
            core.add_logger('##log_message', auto_scroll_button=False, copy_button=False, filter=False, clear_button=False, width=WIDGET_WIDTH, height=80)
            core.set_log_level(core.mvTRACE, logger='##log_message')
            core.add_spacing(count=10)

            # Clear log button
            core.add_button('##clear_log', label='Clear log', callback=logger.clear_log, width=WIDGET_WIDTH)
            core.add_spacing(count=10)

        with simple.group('##password_table_group'):
            # Password table
            header = ['No', 'Title', 'Identifier', 'Password', 'Note']
            core.add_table('##password_table', header, callback=table.table_printer, height=int(WINDOW_HEIGHT * 0.45), width=WIDGET_WIDTH)
            core.add_spacing(count=10)

            table.update_password_table()

            # Update password table button
            update_delete_spacing = 20
            core.add_button('##update_table', label='Update table', callback=table.update_password_table, width=WIDGET_HALF_WIDTH - (update_delete_spacing // 2))
            core.set_item_color('##update_table', core.mvGuiCol_Button, color=BLUE)
            core.add_same_line(spacing=update_delete_spacing)

            # Delete password table button
            core.add_button('##delete_table', label='Delete table', width=WIDGET_HALF_WIDTH - (update_delete_spacing // 2))
            core.set_item_color('##delete_table', core.mvGuiCol_Button, color=RED)
            with simple.popup('##delete_table', '##ask_delete', mousebutton=core.mvMouseButton_Left, modal=True):
                with simple.group('##delete_table_button_group'):
                    delete_table_spacing = 10
                    delete_table_half_width = core.get_main_window_size()[1] // 5 - delete_table_spacing

                    core.add_text('##delete_table_button', default_value='Are you sure to delete all data?')

                    core.add_spacing(count=delete_table_spacing)
                    core.add_button('##delete_table_button_yes', label='Yes', callback=table.delete_password_table, callback_data=True, width=delete_table_half_width)
                    core.add_same_line(spacing=delete_table_spacing)
                    core.add_button('##delete_table_button_no', label='No', callback=table.delete_password_table, callback_data=False, width=delete_table_half_width)

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
    core.set_style_window_padding(WINDOW_PADDING, WINDOW_PADDING)
    core.set_exit_callback(model.close_connection)

    # core.set_render_callback(apply_centering)
    core.start_dearpygui(primary_window=TITLE)


if __name__ == '__main__':
    main()
