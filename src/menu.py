from constants import VERSION
from dearpygui import core, simple


def update_theme(theme):
    """Update theme.

    Args:
        theme (str): theme name
    """
    core.set_theme(theme)


def show_version():
    """Show version of this app.
    """
    window_name = 'Version info##version_info_window'
    if not core.does_item_exist(window_name):
        with simple.window(window_name, on_close=lambda: core.delete_item(window_name), autosize=True, no_resize=True):
            core.add_text('##version_info_0', default_value=f'Password Manager v{VERSION}')
