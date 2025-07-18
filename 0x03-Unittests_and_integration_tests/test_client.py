#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


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