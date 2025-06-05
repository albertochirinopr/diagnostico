KNOWLEDGE_BASE = [
    {
        'keywords': ["yellow leaves", "yellowing leaves", "chlorosis"],
        'diagnosis': "Potential nutrient deficiency (e.g., nitrogen, iron) or overwatering.",
        'treatment': "Check soil moisture. If soggy, allow to dry. If dry, consider a balanced fertilizer according to plant needs. Ensure proper drainage."
    },
    {
        'keywords': ["brown tips", "crispy edges", "dry leaves"],
        'diagnosis': "Potential low humidity, underwatering, or salt buildup.",
        'treatment': "Increase humidity around the plant (misting, humidifier). Ensure consistent watering. Flush soil with distilled water if salt buildup is suspected."
    },
    {
        'keywords': ["white spots", "powdery mildew", "white powdery"],
        'diagnosis': "Possible powdery mildew, a fungal disease.",
        'treatment': "Improve air circulation. Reduce humidity if very high. Remove affected leaves. Apply a fungicide if necessary. Avoid wetting foliage."
    },
    {
        'keywords': ["wilting", "drooping"],
        'diagnosis': "Could be underwatering or overwatering, or root rot.",
        'treatment': "Check soil moisture. If dry, water thoroughly. If wet, allow soil to dry out and check roots for rot (mushy, brown). Repot if root rot is present."
    },
    {
        'keywords': ["pests", "insects", "aphids", "spider mites", "mealybugs", "gnats"],
        'diagnosis': "Pest infestation.",
        'treatment': "Identify the pest. Isolate the plant. Treat with appropriate insecticidal soap, neem oil, or manual removal (e.g., wiping with alcohol for mealybugs)."
    },
    {
        'keywords': ["stunted growth", "slow growth"],
        'diagnosis': "Insufficient light, nutrients, or root-bound.",
        'treatment': "Ensure the plant is receiving adequate light for its species. Fertilize if not done recently. Check if the plant needs repotting into a larger container."
    },
    {
        'keywords': ["black spots", "leaf spot"],
        'diagnosis': "Fungal or bacterial leaf spot disease.",
        'treatment': "Remove affected leaves. Improve air circulation. Avoid overhead watering. Apply fungicide/bactericide if severe."
    }
]

def diagnose_plant_symptoms(symptoms_text: str) -> list[dict]:
    """
    Analyzes symptom text and suggests potential diagnoses and treatments
    based on a predefined knowledge base.
    """
    results = []
    if not symptoms_text:
        return results

    symptoms_text_lower = symptoms_text.lower()
    matched_diagnoses = set() # To avoid duplicate diagnosis entries if multiple keywords trigger it

    for rule in KNOWLEDGE_BASE:
        for keyword in rule['keywords']:
            if keyword.lower() in symptoms_text_lower:
                # Use the diagnosis itself as the key for the set to ensure uniqueness
                if rule['diagnosis'] not in matched_diagnoses:
                    results.append({
                        'diagnosis': rule['diagnosis'],
                        'treatment': rule['treatment']
                    })
                    matched_diagnoses.add(rule['diagnosis'])
                break  # Move to the next rule once a keyword from this rule matches
    return results

if __name__ == "__main__":
    print("--- Plant Symptom Diagnoser ---")

    # Example 1
    symptoms_text_example1 = "My fern has yellow leaves and some brown tips. I also saw some white spots that look powdery."
    print(f"\nSymptoms reported: \"{symptoms_text_example1}\"")
    diagnoses1 = diagnose_plant_symptoms(symptoms_text_example1)

    if diagnoses1:
        print("\nBased on the symptoms, here are potential issues and treatments:")
        for diag_item in diagnoses1:
            print(f"- Diagnosis: {diag_item['diagnosis']}")
            print(f"  Treatment: {diag_item['treatment']}")
    else:
        print("No specific diagnosis found based on the provided symptoms. Check general plant care.")

    # Example 2: Different symptoms
    symptoms_text_example2 = "The leaves on my succulent are wilting and it seems to have stunted growth. I also saw some tiny spider mites webbings."
    print(f"\nSymptoms reported: \"{symptoms_text_example2}\"")
    diagnoses2 = diagnose_plant_symptoms(symptoms_text_example2)

    if diagnoses2:
        print("\nBased on the symptoms, here are potential issues and treatments:")
        for diag_item in diagnoses2:
            print(f"- Diagnosis: {diag_item['diagnosis']}")
            print(f"  Treatment: {diag_item['treatment']}")
    else:
        print("No specific diagnosis found based on the provided symptoms. Check general plant care.")

    # Example 3: Symptoms matching no specific rules
    symptoms_text_example3 = "My plant looks generally okay, but I am worried."
    print(f"\nSymptoms reported: \"{symptoms_text_example3}\"")
    diagnoses3 = diagnose_plant_symptoms(symptoms_text_example3)

    if diagnoses3:
        print("\nBased on the symptoms, here are potential issues and treatments:")
        for diag_item in diagnoses3:
            print(f"- Diagnosis: {diag_item['diagnosis']}")
            print(f"  Treatment: {diag_item['treatment']}")
    else:
        print("\nNo specific diagnosis found for these symptoms. Monitor the plant for any changes.")

    # Example 4: Empty symptoms
    symptoms_text_example4 = ""
    print(f"\nSymptoms reported: \"{symptoms_text_example4}\"")
    diagnoses4 = diagnose_plant_symptoms(symptoms_text_example4)
    if diagnoses4:
        print("\nBased on the symptoms, here are potential issues and treatments:")
        for diag_item in diagnoses4:
            print(f"- Diagnosis: {diag_item['diagnosis']}")
            print(f"  Treatment: {diag_item['treatment']}")
    else:
        print("\nNo symptoms provided.")
