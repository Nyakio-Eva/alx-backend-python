
#!/usr/bin/env python3
from utils import get_json


class GithubOrgClient:
    """
    Client for fetching organization data from GitHub.
    """

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    @property
    def org(self):
        """
        Fetch organization details.
        """
        return get_json(f"https://api.github.com/orgs/{self.org_name}")
