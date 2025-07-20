#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map
from utils import get_json


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Tests access_nested_map returns expected value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")    


     
class TestGetJson(unittest.TestCase):
    """
    Unit tests for get_json
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')  # ✅ This is the required decorator
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that get_json returns expected payload from given URL
        and mock was called exactly once with the URL
        """
        # Setup the mock response
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Assertions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)
