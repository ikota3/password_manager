from dearpygui import core


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
