import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "budget_tracker.db"


def get_connection():


    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection

def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            app_name TEXT NOT NULL,
            earnings REAL NOT NULL,
            hours REAL NOT NULL,
            trips INTEGER NOT NULL,
            miles REAL DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            due_date TEXT,
            allocation_percentage REAL NOT NULL,
            saved_amount REAL DEFAULT 0,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bill_allocations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER NOT NULL,
            session_id INTEGER,
            amount REAL NOT NULL,
            allocation_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (bill_id)
                REFERENCES bills(id)
                ON DELETE CASCADE,

            FOREIGN KEY (session_id)
                REFERENCES work_sessions(id)
                ON DELETE SET NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            setting_key TEXT PRIMARY KEY,
            setting_value TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_work_session(
    date,
    app_name,
    earnings,
    hours,
    trips,
    miles=0,
    notes=""
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO work_sessions (
            date,
            app_name,
            earnings,
            hours,
            trips,
            miles,
            notes
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        date,
        app_name,
        earnings,
        hours,
        trips,
        miles,
        notes
    ))

    session_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return session_id


def get_all_work_sessions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM work_sessions
        ORDER BY date DESC, id DESC
    """)

    sessions = cursor.fetchall()

    connection.close()

    return [
        dict(session)
        for session in sessions
    ]


def get_work_session(session_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM work_sessions
        WHERE id = ?
    """, (session_id,))

    session = cursor.fetchone()

    connection.close()

    if session:
        return dict(session)

    return None


def update_work_session(
    session_id,
    date,
    app_name,
    earnings,
    hours,
    trips,
    miles,
    notes=""
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE work_sessions

        SET
            date = ?,
            app_name = ?,
            earnings = ?,
            hours = ?,
            trips = ?,
            miles = ?,
            notes = ?

        WHERE id = ?
    """, (
        date,
        app_name,
        earnings,
        hours,
        trips,
        miles,
        notes,
        session_id
    ))

    connection.commit()
    connection.close()


def delete_work_session(session_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM work_sessions
        WHERE id = ?
    """, (session_id,))

    connection.commit()
    connection.close()


def get_sessions_between_dates(
    start_date,
    end_date
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM work_sessions

        WHERE date BETWEEN ? AND ?

        ORDER BY date ASC, id ASC
    """, (
        start_date,
        end_date
    ))

    sessions = cursor.fetchall()

    connection.close()

    return [
        dict(session)
        for session in sessions
    ]


def get_sessions_for_date(
    selected_date
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM work_sessions

        WHERE date = ?

        ORDER BY id ASC
    """, (selected_date,))

    sessions = cursor.fetchall()

    connection.close()

    return [
        dict(session)
        for session in sessions
    ]


def add_bill(
    name,
    amount,
    due_date,
    allocation_percentage
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO bills (
            name,
            amount,
            due_date,
            allocation_percentage
        )

        VALUES (?, ?, ?, ?)
    """, (
        name,
        amount,
        due_date,
        allocation_percentage
    ))

    bill_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return bill_id


def get_all_bills(
    active_only=True
):

    connection = get_connection()
    cursor = connection.cursor()

    if active_only:

        cursor.execute("""
            SELECT *
            FROM bills

            WHERE active = 1

            ORDER BY
                CASE
                    WHEN due_date IS NULL THEN 1
                    ELSE 0
                END,
                due_date ASC,
                id ASC
        """)

    else:

        cursor.execute("""
            SELECT *
            FROM bills

            ORDER BY
                active DESC,
                due_date ASC,
                id ASC
        """)

    bills = cursor.fetchall()

    connection.close()

    return [
        dict(bill)
        for bill in bills
    ]


def get_bill(bill_id):
    """
    Return one bill by ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM bills
        WHERE id = ?
    """, (bill_id,))

    bill = cursor.fetchone()

    connection.close()

    if bill:
        return dict(bill)

    return None


def update_bill(
    bill_id,
    name,
    amount,
    due_date,
    allocation_percentage
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE bills

        SET
            name = ?,
            amount = ?,
            due_date = ?,
            allocation_percentage = ?

        WHERE id = ?
    """, (
        name,
        amount,
        due_date,
        allocation_percentage,
        bill_id
    ))

    connection.commit()
    connection.close()


def delete_bill(bill_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM bills
        WHERE id = ?
    """, (bill_id,))

    connection.commit()
    connection.close()


def deactivate_bill(bill_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE bills

        SET active = 0

        WHERE id = ?
    """, (bill_id,))

    connection.commit()
    connection.close()

def add_bill_allocation(
    bill_id,
    session_id,
    amount,
    allocation_date
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO bill_allocations (
                bill_id,
                session_id,
                amount,
                allocation_date
            )

            VALUES (?, ?, ?, ?)
        """, (
            bill_id,
            session_id,
            amount,
            allocation_date
        ))

        cursor.execute("""
            UPDATE bills

            SET saved_amount =
                saved_amount + ?

            WHERE id = ?
        """, (
            amount,
            bill_id
        ))

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


def get_allocations_for_bill(
    bill_id
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            bill_allocations.*,
            work_sessions.app_name,
            work_sessions.earnings

        FROM bill_allocations

        LEFT JOIN work_sessions
            ON bill_allocations.session_id =
               work_sessions.id

        WHERE bill_allocations.bill_id = ?

        ORDER BY
            bill_allocations.allocation_date DESC,
            bill_allocations.id DESC
    """, (bill_id,))

    allocations = cursor.fetchall()

    connection.close()

    return [
        dict(allocation)
        for allocation in allocations
    ]


def get_allocations_for_session(
    session_id
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            bill_allocations.*,
            bills.name AS bill_name

        FROM bill_allocations

        JOIN bills
            ON bill_allocations.bill_id =
               bills.id

        WHERE bill_allocations.session_id = ?

        ORDER BY bill_allocations.id ASC
    """, (session_id,))

    allocations = cursor.fetchall()

    connection.close()

    return [
        dict(allocation)
        for allocation in allocations
    ]


def session_has_allocations(
    session_id
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS allocation_count

        FROM bill_allocations

        WHERE session_id = ?
    """, (session_id,))

    result = cursor.fetchone()

    connection.close()

    return (
        result["allocation_count"] > 0
    )

def get_total_bill_amount():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(amount),
                0
            ) AS total

        FROM bills

        WHERE active = 1
    """)

    result = cursor.fetchone()

    connection.close()

    return float(result["total"])


def get_total_saved_for_bills():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(saved_amount),
                0
            ) AS total

        FROM bills

        WHERE active = 1
    """)

    result = cursor.fetchone()

    connection.close()

    return float(result["total"])

def save_setting(
    setting_key,
    setting_value
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO settings (
            setting_key,
            setting_value
        )

        VALUES (?, ?)

        ON CONFLICT(setting_key)

        DO UPDATE SET
            setting_value =
                excluded.setting_value
    """, (
        setting_key,
        str(setting_value)
    ))

    connection.commit()
    connection.close()


def get_setting(
    setting_key,
    default=None
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT setting_value

        FROM settings

        WHERE setting_key = ?
    """, (setting_key,))

    result = cursor.fetchone()

    connection.close()

    if result:

        return result[
            "setting_value"
        ]

    return default


def get_all_settings():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM settings

        ORDER BY setting_key
    """)

    settings = cursor.fetchall()

    connection.close()

    return {
        setting["setting_key"]:
        setting["setting_value"]

        for setting in settings
    }

initialize_database()