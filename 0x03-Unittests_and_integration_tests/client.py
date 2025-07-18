
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
