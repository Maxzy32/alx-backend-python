#!/usr/bin/env python3
"""Unittests for client.GithubOrgClient.org"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')  # <-- patching correctly if get_json is imported in client.py
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value and calls get_json once"""

        # Arrange
        expected_payload = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected_payload

        # Act
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert
        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()


from unittest.mock import PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    # ... previous tests ...

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected repos_url from org property"""

        expected_url = "https://api.github.com/orgs/google/repos"
        payload = {"repos_url": expected_url}

        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, expected_url)
