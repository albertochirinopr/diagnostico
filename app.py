import os  # Moved import os to top
import plant_manager
from diagnostics import diagnose_plant_symptoms


def get_integer_input(prompt: str) -> int | None:
    """Safely gets an integer input from the user."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:  # Allow empty input for optional fields
                return None
            return int(value)
        except ValueError:
            print(
                "Invalid input. Please enter a whole number or leave blank "
                "if optional."
            )


def get_string_input(prompt: str, required: bool = True) -> str | None:
    """Safely gets a string input from the user."""
    while True:
        value = input(prompt).strip()
        if not value and required:
            print("This field is required.")
        else:
            return value if value else None


def get_plant_data_from_user(is_update: bool = False) -> dict:
    """Prompts user for plant information and returns it as a dictionary."""
    print(
        "\nEnter plant details (leave blank if not applicable or "
        "no change for update):"
    )
    data = {}
    name = get_string_input("Name: ", required=not is_update)
    if name or not is_update:
        data['name'] = name

    species = get_string_input("Species: ", required=False)
    # Allow empty string if user wants to clear it
    if species or (not is_update and species is not None):
        data['species'] = species

    acquisition_date = get_string_input(
        "Acquisition Date (YYYY-MM-DD): ", required=False
    )
    if acquisition_date or \
       (not is_update and acquisition_date is not None):
        data['acquisition_date'] = acquisition_date

    # For updates, only add to dict if user provides new value.
    # For adds, we take Nones for optional fields.
    watering_frequency = get_integer_input("Watering Frequency (days): ")
    if watering_frequency is not None:
        data['watering_frequency_days'] = watering_frequency
    elif not is_update:
        data['watering_frequency_days'] = None

    last_watered = get_string_input(
        "Last Watered Date (YYYY-MM-DD): ", required=False
    )
    if last_watered or (not is_update and last_watered is not None):
        data['last_watered_date'] = last_watered

    sunlight = get_string_input(
        "Sunlight Preference (e.g., direct, indirect, low): ",
        required=False
    )
    if sunlight or (not is_update and sunlight is not None):
        data['sunlight_preference'] = sunlight

    fertilizing_frequency = get_integer_input(
        "Fertilizing Frequency (days): "
    )
    if fertilizing_frequency is not None:
        data['fertilizing_frequency_days'] = fertilizing_frequency
    elif not is_update:
        data['fertilizing_frequency_days'] = None

    last_fertilized = get_string_input(
        "Last Fertilized Date (YYYY-MM-DD): ", required=False
    )
    if last_fertilized or (not is_update and last_fertilized is not None):
        data['last_fertilized_date'] = last_fertilized

    notes = get_string_input("Notes: ", required=False)
    if notes or (not is_update and notes is not None):
        data['notes'] = notes

    # current_symptoms only directly asked on add,
    # otherwise through dedicated menu
    if not is_update:
        symptoms = get_string_input("Current Symptoms: ", required=False)
        if symptoms or (not is_update and symptoms is not None):
            data['current_symptoms'] = symptoms

    # Filter out Nones for updates unless explicitly set to None by user
    return {
        k: v for k, v in data.items()
        if v is not None or (is_update and v is None)
    }


def get_plant_id_from_user() -> int | None:
    """Prompts the user for a plant ID and ensures it's an integer."""
    return get_integer_input("Enter Plant ID: ")


def display_plant_details(plant: dict):
    """Prints plant details in a readable format."""
    if not plant:
        print("Plant details are not available.")
        return
    print("\n--- Plant Details ---")
    for key, value in plant.items():
        display_key = key.replace('_', ' ').capitalize()
        display_value = value if value is not None else 'N/A'
        print(f"{display_key}: {display_value}")
    print("--------------------")


def main_menu():
    """Displays the main menu and handles user choices."""
    while True:
        print("\n--- Plant Care Main Menu ---")
        print("1. Add New Plant")
        print("2. View Plant Details")
        print("3. View All Plants")
        print("4. Update Plant")
        print("5. Delete Plant")
        print("6. Diagnose Plant (and update symptoms)")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            print("\n--- Add New Plant ---")
            plant_data = get_plant_data_from_user()
            if not plant_data.get('name'):
                print("Plant name is required. Aborting add plant.")
                continue
            plant_id = plant_manager.add_plant(plant_data)
            if plant_id:
                print(
                    f"Plant '{plant_data['name']}' added successfully "
                    f"with ID: {plant_id}"
                )
            else:
                print(
                    f"Failed to add plant '{plant_data.get('name', 'Unknown')}'."
                )

        elif choice == '2':
            print("\n--- View Plant Details ---")
            plant_id = get_plant_id_from_user()
            if plant_id is not None:
                plant = plant_manager.get_plant(plant_id)
                if plant:
                    display_plant_details(plant)
                else:
                    print(f"Plant with ID {plant_id} not found.")
            else:
                print("Invalid Plant ID entered.")

        elif choice == '3':
            print("\n--- All Plants ---")
            plants = plant_manager.get_all_plants()
            if plants:
                for plant_item in plants:  # Renamed var to avoid conflict
                    summary = (
                        f"ID: {plant_item['plant_id']}, "
                        f"Name: {plant_item['name']}, "
                        f"Species: {plant_item.get('species', 'N/A')}"
                    )
                    print(summary)
            else:
                print("No plants found in the database.")

        elif choice == '4':
            print("\n--- Update Plant ---")
            plant_id = get_plant_id_from_user()
            if plant_id is not None:
                existing_plant = plant_manager.get_plant(plant_id)
                if existing_plant:
                    display_plant_details(existing_plant)
                    print(
                        "\nEnter new details (leave blank to keep current "
                        "value):"
                    )
                    update_data = get_plant_data_from_user(is_update=True)
                    if update_data:  # Ensure there's something to update
                        if plant_manager.update_plant(plant_id, update_data):
                            print(f"Plant ID {plant_id} updated successfully.")
                        else:
                            print(f"Failed to update plant ID {plant_id}.")
                    else:
                        print("No changes specified. Update cancelled.")
                else:
                    print(f"Plant with ID {plant_id} not found.")
            else:
                print("Invalid Plant ID entered.")

        elif choice == '5':
            print("\n--- Delete Plant ---")
            plant_id = get_plant_id_from_user()
            if plant_id is not None:
                # Optional: Confirm before deleting
                confirm_prompt = (
                    f"Are you sure you want to delete plant ID {plant_id}? "
                    "(yes/no): "
                )
                confirm = input(confirm_prompt).lower()
                if confirm == 'yes':
                    if plant_manager.delete_plant(plant_id):
                        print(f"Plant ID {plant_id} deleted successfully.")
                    else:
                        print(
                            f"Failed to delete plant ID {plant_id}. "
                            "It might not exist."
                        )
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid Plant ID entered.")

        elif choice == '6':
            print("\n--- Diagnose Plant ---")
            plant_id = get_plant_id_from_user()
            if plant_id is None:
                print("Invalid Plant ID entered.")
                continue

            plant = plant_manager.get_plant(plant_id)
            if not plant:
                print(f"Plant with ID {plant_id} not found.")
                continue

            plant_name = plant.get('name', 'N/A')
            print(f"\nPlant: {plant_name}")
            current_symptoms = plant.get('current_symptoms', '')
            symptom_display = current_symptoms if current_symptoms else 'None'
            print(f"Current recorded symptoms: \"{symptom_display}\"")

            symptoms_for_diagnosis = current_symptoms
            prompt_new_symptoms = (
                "Do you want to use these symptoms or provide new/updated "
                "ones for this diagnosis? (use/new): "
            )
            choice_new_symptoms = input(prompt_new_symptoms).strip().lower()

            if choice_new_symptoms == 'new':
                new_symptoms_text = get_string_input(
                    "Enter new/updated symptoms: ", required=False
                )
                if new_symptoms_text is None:  # User entered blank
                    new_symptoms_text = ""

                symptoms_for_diagnosis = new_symptoms_text

                save_choice_prompt = (
                    "Do you want to save these new symptoms to the plant's "
                    "record? (yes/no): "
                )
                save_new_symptoms_choice = input(save_choice_prompt)
                save_new_symptoms_choice = save_new_symptoms_choice.strip().lower()  # noqa E501
                if save_new_symptoms_choice == 'yes':
                    update_payload = {'current_symptoms': new_symptoms_text}
                    if plant_manager.update_plant(plant_id, update_payload):
                        print(f"New symptoms saved for plant ID {plant_id}.")
                    else:
                        print(
                            "Failed to save new symptoms for plant ID "
                            f"{plant_id}."
                        )

            if not symptoms_for_diagnosis:
                print("No symptoms provided or recorded. Cannot diagnose.")
                continue

            diag_symptoms_display = symptoms_for_diagnosis
            print(
                "\nDiagnosing based on symptoms: "
                f"\"{diag_symptoms_display}\""
            )
            diagnoses_results = diagnose_plant_symptoms(symptoms_for_diagnosis)

            if diagnoses_results:
                print("\n--- Diagnosis Results ---")
                for result in diagnoses_results:
                    print(f"  - Potential Issue: {result['diagnosis']}")
                    print(f"    Suggested Treatment: {result['treatment']}")
                print("-------------------------")
            else:
                print(
                    "No specific diagnosis found based on the provided "
                    "symptoms. Ensure symptoms are descriptive or try "
                    "rephrasing."
                )

        elif choice == '7':
            print("Exiting Plant Care application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    # Ensure database exists before starting app
    # This could also be a separate setup step for the user
    if not os.path.exists(plant_manager.DB_FILE):
        print(f"Database file {plant_manager.DB_FILE} not found.")
        print(
            "Please run database_setup.py first to create the database and "
            "table."
        )
        # Alternatively, you could call the setup function here:
        # import database_setup
        # print("Running initial database setup...")
        # database_setup.create_table()
    else:
        main_menu()
