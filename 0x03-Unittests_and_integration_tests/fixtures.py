#!/usr/bin/env python3
"""Mocked payloads for integration testing"""

TEST_PAYLOAD = {
    "org_payload": {
        "login": "google",
        "id": 1,
        "url": "https://api.github.com/orgs/google",
        "repos_url": "https://api.github.com/orgs/google/repos"
    },
    "repos_payload": [
        {
            "id": 1,
            "name": "repo1",
            "license": {"key": "apache-2.0"}
        },
        {
            "id": 2,
            "name": "repo2",
            "license": {"key": "mit"}
        },
    ],
    "expected_repos": ["repo1", "repo2"],
    "apache2_repos": ["repo1"]
}
