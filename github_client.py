import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

class GitHubAnalyzer:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        self.client = Github(token) if token else Github()
        if token:
            print("✅ GitHub Token 加载成功！")
        else:
            print("⚠️ 未检测到 Token，使用匿名模式。")

    def get_repo_details(self, repo_name):
        repo = self.client.get_repo(repo_name)
        has_license = False
        try:
            repo.get_license()
            has_license = True
        except:
            pass
            
        return {
            "full_name": repo.full_name,
            "stars": repo.stargazers_count,
            "open_issues": repo.open_issues_count,
            "last_updated": repo.updated_at,
            "has_license": has_license,
            "forks": repo.forks_count
        }
