import os
import datetime
import sqlite3
from dataclasses import dataclass, field

DB_LOCATION = os.path.normpath(os.path.join(os.path.dirname(__file__), '../password_manager.db'))


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_LOCATION, check_same_thread=False)
    except sqlite3.Error as e:
        print(e)

    return conn


def close_connection():
    con.close()


con = create_connection()
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
class Password_Info:
    row_id: int = field(default=None)
    title: str = field(default=None)
    identifier: str = field(default=None)
    password: bytes = field(default=None)
    note: str = field(default=None)
    created_at: datetime.datetime = field(default=None)
    updated_at: datetime.datetime = field(default=None)


def insert_one_item(password_info: Password_Info):
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


def update_one_item(password_info: Password_Info):
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


def delete_one_item(password_info: Password_Info):
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


def select_all_item():
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
            return [Password_Info(*row) for row in results]
    except sqlite3.Error as e:
        print(e)
