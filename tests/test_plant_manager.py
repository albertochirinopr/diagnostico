import unittest
import os
import sqlite3
import sys

# Adjust path to import from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import functions from plant_manager and database_setup
import plant_manager
from database_setup import create_table

TEST_DB_FILE = 'test_plant_care.db'

class TestPlantManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set the database file for plant_manager to the test database.
        This is done once for the entire test class.
        """
        cls.original_db_file = plant_manager.DB_FILE
        plant_manager.DB_FILE = TEST_DB_FILE

    @classmethod
    def tearDownClass(cls):
        """
        Restore the original database file path in plant_manager.
        """
        plant_manager.DB_FILE = cls.original_db_file

    def setUp(self):
        """
        Create a fresh test database and table before each test.
        """
        # Ensure no old test db exists
        if os.path.exists(TEST_DB_FILE):
            os.remove(TEST_DB_FILE)
        # Create table in the test_db
        create_table(db_name=TEST_DB_FILE)
        # Verify the db file was created
        self.assertTrue(os.path.exists(TEST_DB_FILE), "Test database file should be created.")


    def tearDown(self):
        """
        Remove the test database file after each test.
        """
        if os.path.exists(TEST_DB_FILE):
            os.remove(TEST_DB_FILE)
        # Verify the db file was removed
        # self.assertFalse(os.path.exists(TEST_DB_FILE), "Test database file should be removed.")


    def test_add_and_get_plant(self):
        plant_data = {'name': 'Test Rose', 'species': 'Rosa testiflora', 'watering_frequency_days': 3}
        plant_id = plant_manager.add_plant(plant_data)
        self.assertIsNotNone(plant_id, "add_plant should return an ID.")

        retrieved_plant = plant_manager.get_plant(plant_id)
        self.assertIsNotNone(retrieved_plant, "get_plant should retrieve the added plant.")
        self.assertEqual(retrieved_plant['name'], plant_data['name'])
        self.assertEqual(retrieved_plant['species'], plant_data['species'])
        self.assertEqual(retrieved_plant['watering_frequency_days'], plant_data['watering_frequency_days'])

    def test_get_nonexistent_plant(self):
        retrieved_plant = plant_manager.get_plant(99999) # Assuming this ID won't exist
        self.assertIsNone(retrieved_plant, "get_plant should return None for a non-existent ID.")

    def test_get_all_plants_empty(self):
        plants = plant_manager.get_all_plants()
        self.assertEqual(len(plants), 0, "get_all_plants should return an empty list when DB is empty.")

    def test_get_all_plants_multiple(self):
        plant_data1 = {'name': 'Fern', 'species': 'Pteridophyta'}
        plant_data2 = {'name': 'Cactus', 'species': 'Cactaceae'}
        plant_manager.add_plant(plant_data1)
        plant_manager.add_plant(plant_data2)

        plants = plant_manager.get_all_plants()
        self.assertEqual(len(plants), 2, "get_all_plants should return all added plants.")
        plant_names = [p['name'] for p in plants]
        self.assertIn('Fern', plant_names)
        self.assertIn('Cactus', plant_names)

    def test_update_plant_existing(self):
        plant_data = {'name': 'Original Name', 'notes': 'Original notes'}
        plant_id = plant_manager.add_plant(plant_data)
        self.assertIsNotNone(plant_id)

        update_data = {'name': 'Updated Name', 'notes': 'Updated notes', 'current_symptoms': 'None'}
        update_result = plant_manager.update_plant(plant_id, update_data)
        self.assertTrue(update_result, "update_plant should return True on successful update.")

        updated_plant = plant_manager.get_plant(plant_id)
        self.assertEqual(updated_plant['name'], 'Updated Name')
        self.assertEqual(updated_plant['notes'], 'Updated notes')
        self.assertEqual(updated_plant['current_symptoms'], 'None')


    def test_update_plant_partial(self):
        plant_data = {'name': 'Lily', 'species': 'Lilium', 'notes': 'Fragrant'}
        plant_id = plant_manager.add_plant(plant_data)
        self.assertIsNotNone(plant_id)

        update_data = {'notes': 'Very fragrant and beautiful'}
        update_result = plant_manager.update_plant(plant_id, update_data)
        self.assertTrue(update_result)

        updated_plant = plant_manager.get_plant(plant_id)
        self.assertEqual(updated_plant['name'], 'Lily') # Should remain unchanged
        self.assertEqual(updated_plant['species'], 'Lilium') # Should remain unchanged
        self.assertEqual(updated_plant['notes'], 'Very fragrant and beautiful') # Should be updated


    def test_update_plant_nonexistent(self):
        update_data = {'name': 'Ghost Plant'}
        update_result = plant_manager.update_plant(88888, update_data) # Non-existent ID
        self.assertFalse(update_result, "update_plant should return False for a non-existent ID.")

    def test_delete_plant_existing(self):
        plant_data = {'name': 'To Be Deleted'}
        plant_id = plant_manager.add_plant(plant_data)
        self.assertIsNotNone(plant_id)

        delete_result = plant_manager.delete_plant(plant_id)
        self.assertTrue(delete_result, "delete_plant should return True on successful deletion.")

        deleted_plant = plant_manager.get_plant(plant_id)
        self.assertIsNone(deleted_plant, "get_plant should return None for a deleted plant.")

    def test_delete_plant_nonexistent(self):
        delete_result = plant_manager.delete_plant(77777) # Non-existent ID
        self.assertFalse(delete_result, "delete_plant should return False for a non-existent ID.")

    def test_add_plant_required_fields(self):
        # Test the NOT NULL constraint on 'name'
        # sqlite3.IntegrityError should be raised by the database if 'name' is not provided
        # and the plant_manager.add_plant function does not catch it internally.
        # If add_plant catches it and returns None, that's also a valid test.

        # Current add_plant implementation in plant_manager.py might raise error or return None
        # based on how it's structured. Let's assume it might print an error and return None
        # or the DB itself will raise IntegrityError which is not caught by add_plant.

        plant_data_no_name = {'species': 'Test Species'}

        # Option 1: If add_plant is expected to raise the IntegrityError
        # with self.assertRaises(sqlite3.IntegrityError):
        #     plant_manager.add_plant(plant_data_no_name)

        # Option 2: If add_plant catches the error and returns None (or similar)
        plant_id = plant_manager.add_plant(plant_data_no_name)
        # This behavior depends on how add_plant is implemented.
        # If add_plant tries to insert and DB fails due to NOT NULL on name,
        # the try-except block in add_plant will catch sqlite3.Error and return None.
        self.assertIsNone(plant_id, "Adding a plant without a required 'name' should fail (return None).")


    def test_update_plant_empty_data(self):
        """Test updating a plant with an empty data dictionary."""
        plant_data = {'name': 'Test Plant', 'species': 'Test Species'}
        plant_id = plant_manager.add_plant(plant_data)
        self.assertIsNotNone(plant_id)

        update_result = plant_manager.update_plant(plant_id, {}) # Empty update data
        # The update_plant function has a check: `if not plant_data: return False`
        self.assertFalse(update_result, "update_plant with empty data should return False and not alter the plant.")

        retrieved_plant = plant_manager.get_plant(plant_id)
        self.assertEqual(retrieved_plant['name'], 'Test Plant', "Plant name should not change on empty update.")
        self.assertEqual(retrieved_plant['species'], 'Test Species', "Plant species should not change on empty update.")


if __name__ == '__main__':
    unittest.main()
