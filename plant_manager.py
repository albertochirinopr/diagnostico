import sqlite3

DB_FILE = 'plant_care.db'

def add_plant(plant_data: dict) -> int | None:
    """Adds a new plant to the database.

    Args:
        plant_data: A dictionary containing the plant's details.

    Returns:
        The lastrowid of the inserted plant, or None if an error occurs.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        columns = ', '.join(plant_data.keys())
        placeholders = ', '.join('?' for _ in plant_data)
        sql = f"INSERT INTO plants ({columns}) VALUES ({placeholders})"

        cursor.execute(sql, list(plant_data.values()))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error adding plant: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_plant(plant_id: int) -> dict | None:
    """Retrieves a specific plant from the database by its ID.

    Args:
        plant_id: The ID of the plant to retrieve.

    Returns:
        A dictionary representing the plant if found, else None.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM plants WHERE plant_id = ?", (plant_id,))
        plant_row = cursor.fetchone()

        if plant_row:
            return dict(plant_row)
        return None
    except sqlite3.Error as e:
        print(f"Error getting plant: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_plants() -> list[dict]:
    """Retrieves all plants from the database.

    Returns:
        A list of dictionaries, where each dictionary represents a plant.
        Returns an empty list if an error occurs or no plants are found.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM plants ORDER BY name")
        plant_rows = cursor.fetchall()

        return [dict(row) for row in plant_rows]
    except sqlite3.Error as e:
        print(f"Error getting all plants: {e}")
        return []
    finally:
        if conn:
            conn.close()

def update_plant(plant_id: int, plant_data: dict) -> bool:
    """Updates an existing plant in the database.

    Args:
        plant_id: The ID of the plant to update.
        plant_data: A dictionary containing the fields to update and their new values.

    Returns:
        True if the update was successful, False otherwise.
    """
    conn = None
    if not plant_data:
        print("No data provided for update.")
        return False
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        set_clause = ', '.join(f"{key} = ?" for key in plant_data)
        sql = f"UPDATE plants SET {set_clause} WHERE plant_id = ?"

        values = list(plant_data.values())
        values.append(plant_id)

        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error updating plant: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_plant(plant_id: int) -> bool:
    """Deletes a plant from the database.

    Args:
        plant_id: The ID of the plant to delete.

    Returns:
        True if the deletion was successful, False otherwise.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM plants WHERE plant_id = ?", (plant_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error deleting plant: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    # Ensure database_setup.py has been run once before this.

    print("Plant Manager Script")

    # 1. Add a new plant
    plant1_data = {
        'name': 'Snake Plant',
        'species': 'Sansevieria trifasciata',
        'acquisition_date': '2023-01-15',
        'watering_frequency_days': 14,
        'last_watered_date': '2024-07-10',
        'sunlight_preference': 'Indirect light',
        'fertilizing_frequency_days': 60,
        'last_fertilized_date': '2024-06-01',
        'notes': 'Hardy and low maintenance.',
        'current_symptoms': ''
    }
    plant1_id = add_plant(plant1_data)
    if plant1_id:
        print(f"\nAdded plant '{plant1_data['name']}' with ID: {plant1_id}")
    else:
        print(f"\nFailed to add plant '{plant1_data['name']}'")

    plant2_data = {
        'name': 'Spider Plant',
        'species': 'Chlorophytum comosum',
        'acquisition_date': '2023-03-20',
        'watering_frequency_days': 7,
        'last_watered_date': '2024-07-15',
        'sunlight_preference': 'Bright, indirect light',
        'notes': 'Produces spiderettes.'
    }
    plant2_id = add_plant(plant2_data)
    if plant2_id:
        print(f"Added plant '{plant2_data['name']}' with ID: {plant2_id}")
    else:
        print(f"Failed to add plant '{plant2_data['name']}'")

    # 2. Get all plants
    print("\n--- All Plants ---")
    all_plants = get_all_plants()
    if all_plants:
        for plant in all_plants:
            print(f"- ID: {plant['plant_id']}, Name: {plant['name']}, Species: {plant['species']}")
    else:
        print("No plants found or error retrieving them.")

    # 3. Get a specific plant
    if plant1_id:
        print(f"\n--- Details for Plant ID {plant1_id} ---")
        plant_detail = get_plant(plant1_id)
        if plant_detail:
            for key, value in plant_detail.items():
                print(f"  {key}: {value}")
        else:
            print(f"Plant with ID {plant1_id} not found.")

    # 4. Update a plant
    if plant1_id:
        update_data = {'notes': 'Actually quite resilient.', 'current_symptoms': 'Slightly yellowing leaves'}
        print(f"\n--- Updating Plant ID {plant1_id} ---")
        if update_plant(plant1_id, update_data):
            print(f"Plant ID {plant1_id} updated successfully.")
            updated_plant_detail = get_plant(plant1_id)
            if updated_plant_detail:
                print(f"  New notes: {updated_plant_detail['notes']}")
                print(f"  New symptoms: {updated_plant_detail['current_symptoms']}")
        else:
            print(f"Failed to update plant ID {plant1_id}.")

    # 5. Get all plants again to see changes
    print("\n--- All Plants After Update ---")
    all_plants_after_update = get_all_plants()
    if all_plants_after_update:
        for plant in all_plants_after_update:
            print(f"- ID: {plant['plant_id']}, Name: {plant['name']}, Notes: {plant.get('notes')}")
    else:
        print("No plants found or error retrieving them.")

    # 6. Delete a plant
    if plant2_id:
        print(f"\n--- Deleting Plant ID {plant2_id} ---")
        if delete_plant(plant2_id):
            print(f"Plant ID {plant2_id} deleted successfully.")
        else:
            print(f"Failed to delete plant ID {plant2_id}.")

    # 7. Get all plants again
    print("\n--- All Plants After Deletion ---")
    all_plants_after_deletion = get_all_plants()
    if all_plants_after_deletion:
        for plant in all_plants_after_deletion:
            print(f"- ID: {plant['plant_id']}, Name: {plant['name']}")
    else:
        print("No plants found or error retrieving them.")

    # Clean up the test plant if it exists
    if plant1_id:
        delete_plant(plant1_id)
        print(f"\nCleaned up test plant ID {plant1_id}.")
