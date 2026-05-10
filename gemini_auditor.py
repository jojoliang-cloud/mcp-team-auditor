import os
from google import genai
from google.genai import types
from github_client import GitHubAnalyzer
from scorer import RepoScorer
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ 错误: 未在 .env 文件中找到 GEMINI_API_KEY")
    exit(1)

analyzer = GitHubAnalyzer()
scorer = RepoScorer()

def analyze_github_risk(query: str, limit: int = 3):
    """搜索 GitHub 仓库并评估风险。query 是搜索词，limit 是数量。"""
    print(f"\n[执行工具] 正在查询 GitHub 并分析风险: {query}...")
    try:
        search_results = analyzer.client.search_repositories(query=query, sort="stars", order="desc")
        results = []
        for i, repo in enumerate(search_results):
            if i >= limit: break
            repo_data = analyzer.get_repo_details(repo.full_name)
            analysis = scorer.analyze(repo_data)
            results.append({
                "repo": repo.full_name,
                "risk": analysis["risk_level"],
                "score": analysis["score"],
                "reasons": analysis.get("reason_list", [])
            })
        return str(results)
    except Exception as e:
        return f"查询出错: {str(e)}"

# 初始化客户端
client = genai.Client(api_key=api_key)
model_id = "gemini-2.0-flash"

print("\n✨ Gemini 2.0 风险审计专家已就绪！")

while True:
    user_input = input("\n👤 你 > ")
    if user_input.lower() in ['exit', 'quit']: break

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=user_input,
            config=types.GenerateContentConfig(
                tools=[analyze_github_risk],
                automatic_function_calling={"disable": False}
            )
        )
        print(f"\n🤖 Gemini > {response.text}")
    except Exception as e:
        print(f"❌ 运行中出错: {str(e)}")
