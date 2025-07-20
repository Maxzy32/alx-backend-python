# #!/usr/bin/env python3
# """
# Unit tests for utils module:
# - access_nested_map
# - get_json
# - memoize
# """

# import unittest
# from unittest.mock import patch, Mock
# from parameterized import parameterized
# from utils import access_nested_map, get_json, memoize


# class TestAccessNestedMap(unittest.TestCase):
#     """Unit tests for the access_nested_map function."""

#     @parameterized.expand([
#         ({"a": 1}, ("a",), 1),
#         ({"a": {"b": 2}}, ("a",), {"b": 2}),
#         ({"a": {"b": 2}}, ("a", "b"), 2)
#     ])
#     def test_access_nested_map(self, nested_map, path, expected):
#         """Test that access_nested_map returns expected value."""
#         self.assertEqual(access_nested_map(nested_map, path), expected)

#     @parameterized.expand([
#         ({}, ("a",)),
#         ({"a": 1}, ("a", "b")),
#     ])
#     def test_access_nested_map_exception(self, nested_map, path):
#         """Test that access_nested_map raises KeyError on missing keys."""
#         with self.assertRaises(KeyError) as cm:
#             access_nested_map(nested_map, path)
#         self.assertEqual(str(cm.exception), f"'{path[-1]}'")


# class TestGetJson(unittest.TestCase):
#     """Unit tests for the get_json function."""

#     def test_get_json(self):
#         """Test that get_json returns the expected result."""
#         test_cases = [
#             ("http://example.com", {"payload": True}),
#             ("http://holberton.io", {"payload": False}),
#         ]

#         for test_url, test_payload in test_cases:
#             with patch("utils.requests.get") as mock_get:
#                 mock_response = Mock()
#                 mock_response.json.return_value = test_payload
#                 mock_get.return_value = mock_response

#                 result = get_json(test_url)
#                 mock_get.assert_called_once_with(test_url)
#                 self.assertEqual(result, test_payload)


# class TestMemoize(unittest.TestCase):
#     """Test case for the memoize decorator."""

#     def test_memoize(self):
#         """Test that a_method is called only once due to memoization."""

#         class TestClass:
#             """A class to test memoization."""

#             def a_method(self):
#                 """Method to be memoized."""
#                 return 42

#             @memoize
#             def a_property(self):
#                 """Memoized property that calls a_method."""
#                 return self.a_method()

#         with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
#             obj = TestClass()
#             self.assertEqual(obj.a_property, 42)
#             self.assertEqual(obj.a_property, 42)
#             mock_method.assert_called_once()


#!/usr/bin/env python3
"""
Unit tests for utils module:
- access_nested_map
- get_json
- memoize
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns expected value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError on missing keys."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        expected_message = f"'{path[-1]}'"
        self.assertEqual(str(cm.exception), expected_message)


class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json function."""

    def test_get_json(self):
        """Test that get_json returns the expected result."""
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            with patch("utils.requests.get") as mock_get:
                mock_response = Mock()
                mock_response.json.return_value = test_payload
                mock_get.return_value = mock_response

                result = get_json(test_url)
                mock_get.assert_called_once_with(test_url)
                self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator."""

    def test_memoize(self):
        """Test that a_method is called only once due to memoization."""

        class TestClass:
            """A class to test memoization."""

            def a_method(self):
                """Method to be memoized."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()

        with patch.object(
            TestClass, 'a_method', return_value=42
        ) as mock_method:
            obj = TestClass()
            # Call the memoized method twice
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            # Ensure a_method was only called once
            mock_method.assert_called_once()