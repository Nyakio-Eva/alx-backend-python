
#!/usr/bin/env python3
from utils import get_json

class GithubOrgClient:
    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self):
        return self.org["repos_url"]
    
    def public_repos(self):
        return [
            repo["name"] for repo in get_json(self._public_repos_url)
        ]

    """Client to interact with GitHub Organization API."""
    @staticmethod
    def has_license(repo: dict, license_key: str) -> bool:
        """
        Checks if a repository has a specific license key.
        """
        return repo.get("license", {}).get("key") == license_key