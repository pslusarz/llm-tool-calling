"""
Test module for the App class.
"""
import unittest
from app import App


class TestApp(unittest.TestCase):    

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = App()

    def test_simple_knowledge_question(self):
        """Test question that doesn't require any tools (pure knowledge)."""
        result = self.app.answer("what is the capital of Indonesia?")
        
        # Should mention Jakarta specifically since this is factual knowledge
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn("Jakarta", result)

    def test_single_tool_question(self):
        """Test question requiring single tool call (location only)."""
        result = self.app.answer("what state am I in?")
        
        # Should specifically mention Washington since that's the constant location
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn("Washington", result)

    def test_chained_tools_question(self):
        """Test question requiring tool chaining (location + weather)."""
        result = self.app.answer("what is the temperature outside?")
        
        # Should return specific temperature and mention °F since weather is generated
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn("°F", result)
        # Should mention temperature concept
        self.assertTrue(any(word in result.lower() for word in ["temperature", "degrees"]))

    def test_complex_reasoning_question(self):
        """Test question requiring multiple tools + LLM reasoning."""
        result = self.app.answer("what should I wear today?")
        
        # Should mention King County, Washington and provide clothing recommendations
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        # Should mention the known location
        self.assertTrue(any(location in result for location in ["King County", "Washington"]))
        # Should provide clothing advice
        clothing_terms = ["wear", "clothing", "shirt", "jacket", "temperature", "rain", "outfit"]
        self.assertTrue(any(term in result.lower() for term in clothing_terms))

    def test_impossible_question(self):
        """Test question that cannot be answered with available tools."""
        result = self.app.answer("what do I have in my pocket?")
        
        # Should acknowledge inability to answer
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        # Should indicate lack of information or inability to answer
        inability_terms = ["don't", "can't", "unable", "don't have", "no access", "sorry"]
        self.assertTrue(any(term in result.lower() for term in inability_terms))

    def test_weather_question(self):
        """Test a weather-specific question."""
        result = self.app.answer("is it going to rain today?")
        
        # Should mention King County, Washington and precipitation percentage
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        # Should mention location
        self.assertTrue(any(location in result for location in ["King County", "Washington"]))
        # Should mention precipitation/rain with percentage
        self.assertTrue(any(term in result.lower() for term in ["rain", "precipitation", "%"]))

    def test_location_question(self):
        """Test a location-specific question."""
        result = self.app.answer("where am I located?")
        
        # Should specifically mention King County, Washington
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn("King County", result)
        self.assertIn("Washington", result)

    def test_answer_method_exists(self):
        """Test that the answer method exists and is callable."""
        self.assertTrue(hasattr(self.app, 'answer'))
        self.assertTrue(callable(getattr(self.app, 'answer')))



if __name__ == "__main__":
    unittest.main()
