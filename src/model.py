import os
import datetime
import sqlite3
from dataclasses import dataclass, field

DB_LOCATION = os.path.normpath(os.path.join(os.path.dirname(__file__), '../password_manager.db'))


def create_connection() -> sqlite3.Connection:
    """Create connection.

    Returns:
        sqlite3.Connection: connection object.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_LOCATION, check_same_thread=False)
    except sqlite3.Error as e:
        print(e)
        raise

    return conn


def close_connection():
    """Close connection.
    """
    con.close()


try:
    con = create_connection()
except Exception:
    raise
con.execute("""
            create table if not exists password_info (
                row_id INTEGER PRIMARY KEY,
                title TEXT,
                identifier TEXT,
                password BLOB,
                note TEXT,
                created_at DATE,
                updated_at DATE
            );
            """)


@dataclass
class PasswordInfo:
    """Class for storing password information.

    Args:
        row_id (int): Row id.
        title (str): Title.
        identifier (str): Identifier.
        password (bytes): Password.
        note (str): Note.
        created_at (str): Created time.
        updated_at (str): Updated time.
    """
    row_id: int = field(default=None)
    title: str = field(default=None)
    identifier: str = field(default=None)
    password: bytes = field(default=None)
    note: str = field(default=None)
    created_at: str = field(default=None)
    updated_at: str = field(default=None)


def insert_one_item(password_info: PasswordInfo):
    """Insert one item in password info.

    Args: PasswordInfo
    """
    try:
        with con:
            con.execute(
                """
                insert into password_info (
                    title,
                    identifier,
                    password,
                    note,
                    created_at,
                    updated_at
                ) values (?, ?, ?, ?, ?, ?);
                """,
                (
                    password_info.title,
                    password_info.identifier,
                    sqlite3.Binary(password_info.password),
                    password_info.note,
                    datetime.datetime.now(),
                    datetime.datetime.now()
                )
            )
    except sqlite3.Error as e:
        print(e)
        raise


# TODO not tested
def update_item_by_row_id(password_info: PasswordInfo):
    """Update one item in password info.

    Args: PasswordInfo
    """
    try:
        with con:
            con.execute(
                """
                update password_info
                set
                    title = ?,
                    identifier = ?,
                    note = ?,
                    updated_at = ?
                where
                    row_id = ?;
                """,
                (
                    password_info.title,
                    password_info.identifier,
                    password_info.note,
                    datetime.datetime.now(),
                    password_info.row_id
                )
            )
    except sqlite3.Error as e:
        print(e)
        raise


# TODO not tested
def delete_item_by_row_id(password_info: PasswordInfo):
    """Delete one item in password info.

    Args: PasswordInfo
    """
    try:
        with con:
            con.execute(
                """
                delete from password_info
                where row_id = ?;
                """,
                (password_info.row_id)
            )
    except sqlite3.Error as e:
        print(e)
        raise


def delete_all_items():
    """Delete all items in password info.
    """
    try:
        with con:
            con.execute(
                """
                delete from password_info;
                """
            )
    except sqlite3.Error as e:
        print(e)
        raise


def select_all_items() -> list[PasswordInfo]:
    """Select all items in password_info.

    Returns: list of passwordinfo
    """
    try:
        with con:
            results = con.execute(
                """
                select
                    row_id,
                    title,
                    identifier,
                    password,
                    note,
                    created_at,
                    updated_at
                from password_info
                order by row_id
                """
            ).fetchall()
            return [PasswordInfo(*row) for row in results]
    except sqlite3.Error as e:
        print(e)
        raise


def select_password_by_row_id(password_info: PasswordInfo) -> str:
    """Select password from password_info.

    Args: PasswordInfo
    """
    try:
        with con:
            result = con.execute(
                """
                select
                    password
                from password_info
                where row_id = ?
                """,
                (password_info.row_id)
            ).fetchone()[0]
            return result
    except sqlite3.Error as e:
        print(e)
        raise


if __name__ == '__main__':
    close_connection()
