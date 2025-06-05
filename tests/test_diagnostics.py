import unittest
import sys
import os

# Adjust path to import from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from diagnostics import diagnose_plant_symptoms, KNOWLEDGE_BASE # KNOWLEDGE_BASE for reference if needed

class TestDiagnostics(unittest.TestCase):

    def test_single_diagnosis(self):
        """Symptoms match one rule."""
        symptoms = "My plant has yellowing leaves." # More direct match for "yellowing leaves" keyword
        expected_diagnosis = "Potential nutrient deficiency (e.g., nitrogen, iron) or overwatering."
        results = diagnose_plant_symptoms(symptoms)
        self.assertEqual(len(results), 1, f"Expected 1 diagnosis for '{symptoms}', got {len(results)}")
        self.assertEqual(results[0]['diagnosis'], expected_diagnosis)

    def test_multiple_diagnoses(self):
        """Symptoms match multiple rules."""
        symptoms = "The plant has yellow leaves and some brown tips."
        results = diagnose_plant_symptoms(symptoms)
        self.assertEqual(len(results), 2)
        diagnoses_found = [r['diagnosis'] for r in results]
        self.assertIn("Potential nutrient deficiency (e.g., nitrogen, iron) or overwatering.", diagnoses_found)
        self.assertIn("Potential low humidity, underwatering, or salt buildup.", diagnoses_found)

    def test_no_diagnosis(self):
        """Symptoms match no rules."""
        symptoms = "The plant looks perfectly healthy and vibrant."
        results = diagnose_plant_symptoms(symptoms)
        self.assertEqual(len(results), 0)

    def test_case_insensitivity(self):
        """Keywords match regardless of case."""
        symptoms = "My plant has YELLOW LEAVES and some BROWN TIPS."
        results = diagnose_plant_symptoms(symptoms)
        self.assertEqual(len(results), 2)
        diagnoses_found = [r['diagnosis'] for r in results]
        self.assertIn("Potential nutrient deficiency (e.g., nitrogen, iron) or overwatering.", diagnoses_found)
        self.assertIn("Potential low humidity, underwatering, or salt buildup.", diagnoses_found)

    def test_empty_symptoms(self):
        """Input is an empty string."""
        symptoms = ""
        results = diagnose_plant_symptoms(symptoms)
        self.assertEqual(len(results), 0)

    def test_none_symptoms(self):
        """Input is None. (diagnose_plant_symptoms should handle this gracefully)"""
        # The current implementation of diagnose_plant_symptoms checks `if not symptoms_text:`
        # which handles both None and empty string.
        symptoms = None
        results = diagnose_plant_symptoms(symptoms)
        self.assertEqual(len(results), 0)

    def test_partial_keyword_match(self):
        """
        Ensure partial keyword matches within a larger word don't falsely trigger
        unless intended by keyword design.
        Example: "low" should not match "yellow" or "flower".
        """
        # This test depends on the KNOWLEDGE_BASE keywords.
        # Let's test with "powdery mildew" vs "powder"
        symptoms_specific = "I see powdery mildew on the leaves."
        results_specific = diagnose_plant_symptoms(symptoms_specific)

        found_powdery_mildew = any(r['diagnosis'] == "Possible powdery mildew, a fungal disease." for r in results_specific)
        self.assertTrue(found_powdery_mildew, "Should detect 'powdery mildew'")

        symptoms_general_powder = "There is some white powder near the pot, not on leaves."
        results_general_powder = diagnose_plant_symptoms(symptoms_general_powder)
        found_powdery_mildew_general = any(r['diagnosis'] == "Possible powdery mildew, a fungal disease." for r in results_general_powder)
        # Assuming "powder" alone is not a keyword for powdery mildew
        self.assertFalse(found_powdery_mildew_general, "Should not detect 'powdery mildew' from 'powder' alone if 'powder' is not a specific keyword for it.")

        # Test for "stunted growth" vs "growth"
        symptoms_stunted = "The plant has stunted growth."
        results_stunted = diagnose_plant_symptoms(symptoms_stunted)
        found_stunted_growth_diag = any(r['diagnosis'] == "Insufficient light, nutrients, or root-bound." for r in results_stunted)
        self.assertTrue(found_stunted_growth_diag, "Should detect 'stunted growth'")

        # If "growth" alone is NOT a keyword for the "stunted growth" diagnosis rule:
        symptoms_just_growth = "The plant shows good growth."
        results_just_growth = diagnose_plant_symptoms(symptoms_just_growth)
        # Check if the "Insufficient light..." diagnosis is triggered by "growth" alone.
        # This depends on KNOWLEDGE_BASE. 'stunted growth' and 'slow growth' are keywords for one rule.
        # 'growth' alone is not.
        found_stunted_diag_for_growth_alone = any(r['diagnosis'] == "Insufficient light, nutrients, or root-bound." for r in results_just_growth)
        self.assertFalse(found_stunted_diag_for_growth_alone, "Should not trigger 'Insufficient light...' from 'growth' alone.")


    def test_keyword_uniqueness_in_rule(self):
        """
        If multiple keywords from the SAME rule match, the diagnosis should only be added once.
        """
        symptoms = "The plant has yellowing leaves, which is a form of chlorosis." # "yellowing leaves" and "chlorosis" are in the same rule
        results = diagnose_plant_symptoms(symptoms)
        self.assertEqual(len(results), 1, "Should only return one diagnosis for multiple keywords from the same rule.")
        self.assertEqual(results[0]['diagnosis'], "Potential nutrient deficiency (e.g., nitrogen, iron) or overwatering.")


if __name__ == '__main__':
    unittest.main()
