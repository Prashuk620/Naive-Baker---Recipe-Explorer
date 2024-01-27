import unittest
import requests

class EdamamAPITest(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://api.edamam.com/search"
        self.app_id = "7aa516a5"
        self.app_key = "dc836a223fb788b11ae390504d9e97ce"
        self.final_search_value = "chicken"  # Replace with your actual search value
        self.limit = 10  # Replace with your actual limit
        self.url = f"{self.base_url}?q={self.final_search_value}&app_id={self.app_id}&app_key={self.app_key}&from=0&to={self.limit}"

    def test_api_response_status(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")

    def test_api_response_content(self):
        response = requests.get(self.url)
        self.assertTrue(response.json(), "Response content is empty")

    def test_api_response_structure(self):
        response = requests.get(self.url)
        data = response.json()
        self.assertIn("hits", data, "Expected 'hits' key in the response")
        self.assertIn("q", data, "Expected 'q' key in the response")
    def test_api_response_hits_not_empty(self):
        response = requests.get(self.url)
        data = response.json()
        self.assertTrue(data.get("hits"), "Expected 'hits' to be a non-empty list")

    def test_api_response_hit_structure(self):
        response = requests.get(self.url)
        data = response.json()
        hits = data.get("hits", [])
        if hits:
            first_hit = hits[0]
            self.assertIn("recipe", first_hit, "Expected 'recipe' key in the hit structure")
            recipe = first_hit.get("recipe", {})
            self.assertIn("label", recipe, "Expected 'label' key in the recipe structure")

    def test_api_response_invalid_search_value(self):
        invalid_search_value = "@#$%^&*"
        invalid_url = f"{self.base_url}?q={invalid_search_value}&app_id={self.app_id}&app_key={self.app_key}&from=0&to={self.limit}"
        response = requests.get(invalid_url)
        self.assertEqual(response.status_code, 200, f"Expected status code 200 for an invalid search value, but got {response.status_code}")
        data = response.json()
        self.assertEqual(data.get("q"), invalid_search_value, "Expected 'q' value to be the same as the invalid search value")

    def test_api_response_empty_result(self):
        empty_search_value = "xyz123456789"  # Assuming this won't return any results
        empty_url = f"{self.base_url}?q={empty_search_value}&app_id={self.app_id}&app_key={self.app_key}&from=0&to={self.limit}"
        response = requests.get(empty_url)
        self.assertEqual(response.status_code, 200, f"Expected status code 200 for an empty result, but got {response.status_code}")
        data = response.json()
        self.assertFalse(data.get("hits"), "Expected 'hits' to be an empty list for an empty result")


    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()