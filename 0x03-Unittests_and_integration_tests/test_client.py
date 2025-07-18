#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """
    Defines test cases for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct result
        and get_json is called once with the right URL.
        """
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"org": org_name}

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"org": org_name})
        
        
    def test_public_repos_url(self):
        """Test _public_repos_url property returns expected repos_url"""
        payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, payload["repos_url"])
            mock_org.assert_called_once()
            
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repo names and calls correct methods"""
        # Mock repo payload
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        # Patch _public_repos_url contextually
        with patch.object(GithubOrgClient, "_public_repos_url", new="https://api.github.com/orgs/testorg/repos") as mock_url:
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # Assertions
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")        
            
    """
    Unit tests for GithubOrgClient.has_license.
    """    
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test has_license returns True only if license key matches.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
        
    @parameterized_class([
        {
            "org_payload": fixtures.ORG_PAYLOAD,
            "repos_payload": fixtures.REPOS_PAYLOAD,
            "expected_repos": fixtures.EXPECTED_REPOS,
            "apache2_repos": fixtures.APACHE2_REPOS
        }
    ])    
    @classmethod
    def setUpClass(cls):
        """Set up a mock for requests.get with side effects from fixtures."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Configure .json() to return correct payloads per URL
        mock_get.return_value = Mock()
        mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher after tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected list of repo names."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos with license filter returns expected repos."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
        
@parameterized_class([
    {
        "org_payload": fixtures.ORG_PAYLOAD,
        "repos_payload": fixtures.REPOS_PAYLOAD,
        "expected_repos": fixtures.EXPECTED_REPOS,
        "apache2_repos": fixtures.APACHE2_REPOS,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get to return mock payloads."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        mock_get.return_value = Mock()
        mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
