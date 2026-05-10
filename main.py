import os
from mcp.server.fastmcp import FastMCP
from github_client import GitHubAnalyzer
from scorer import RepoScorer

# 初始化 FastMCP
mcp = FastMCP("repo-auditor")
analyzer = GitHubAnalyzer()
scorer = RepoScorer()

@mcp.tool()
def analyze_repos(query: str, limit: int = 3) -> str:
    """
    搜索 GitHub 仓库并进行业务风险分析。
    参数 query: 搜索关键词（如 'stars:>1000 language:python'）
    参数 limit: 分析的数量
    """
    try:
        search_results = analyzer.client.search_repositories(query=query, sort="stars", order="desc")
        
        results = []
        for i, repo in enumerate(search_results):
            if i >= limit:
                break
            
            # 获取详情与打分
            repo_data = analyzer.get_repo_details(repo.full_name)
            analysis = scorer.analyze(repo_data)
            
            results.append({
                "repo": repo.full_name,
                "risk_level": analysis["risk_level"],
                "score": analysis["score"],
                "reasons": ", ".join(analysis["reason_list"]) if analysis["reason_list"] else "Safe"
            })
        
        return str(results)
    except Exception as e:
        return f"Error during analysis: {str(e)}"

if __name__ == "__main__":
    mcp.run()
