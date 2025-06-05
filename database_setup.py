import sqlite3


def create_table(db_name='plant_care.db'):
    """
    Creates the 'plants' table in the specified database if it doesn't
    already exist.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plants (
                plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                species TEXT,
                acquisition_date TEXT,
                watering_frequency_days INTEGER,
                last_watered_date TEXT,
                sunlight_preference TEXT,
                fertilizing_frequency_days INTEGER,
                last_fertilized_date TEXT,
                notes TEXT,
                current_symptoms TEXT
            )
        ''')

        conn.commit()
        # Suppress print during tests or normal operation unless verbose mode
        # print(
        #   f"Database '{db_name}' and table 'plants' "
        #   "checked/created successfully."
        # )

    except sqlite3.Error as e:
        print(f"Error creating table in {db_name}: {e}")
        raise  # Reraise for testing purposes if needed
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_table()  # Creates plant_care.db by default
    print(
        "Default database 'plant_care.db' and table 'plants' "
        "checked/created successfully."
    )
