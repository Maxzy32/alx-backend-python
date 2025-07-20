class GithubOrgClient:
    # ... other methods ...

    @staticmethod
    def has_license(repo, license_key):
        """Check if repo has a specific license key"""
        return repo.get("license", {}).get("key") == license_key
