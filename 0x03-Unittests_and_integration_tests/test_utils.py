#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map
from utils import get_json
from unittest.mock import patch, Mock
import utils 





 class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator"""

    def test_memoize(self):
        """Test that a_method is called only once due to memoization"""

        class TestClass:
            """A class to test memoization"""

            def a_method(self):
                """Method to be memoized"""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method"""
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()