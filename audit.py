import sys
import json
from github_client import GitHubAnalyzer

def main():
    # 让脚本接收命令行参数，如果没有参数，默认搜 agent
    query = sys.argv[1] if len(sys.argv) > 1 else "topic:agent stars:>1000"
    analyzer = GitHubAnalyzer()
    
    # 打印给 Gemini 看的日志
    print(f"✅ 执行自定义审计: {query}", file=sys.stderr)
    
    search_results = analyzer.client.search_repositories(query=query, sort="updated", order="desc")
    results = []
    for i, repo in enumerate(search_results):
        if i >= 5: break
        results.append({
            "full_name": repo.full_name,
            "stars": repo.stargazers_count,
            "open_issues": repo.open_issues_count,
            "url": repo.html_url
        })
    print(json.dumps(results))

if __name__ == "__main__":
    main()
