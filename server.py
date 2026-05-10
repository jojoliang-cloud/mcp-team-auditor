import uvicorn
import os
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from main import mcp 

app = Starlette()
sse = SseServerTransport("/messages")

async def handle_sse(request):
    async with sse.connect_session(
        request.scope, 
        request.receive, 
        request._send
    ) as session:
        await mcp.handle_sse_session(session)

app.add_route("/sse", handle_sse, methods=["GET"])
app.add_route("/messages", sse.handle_post_message, methods=["POST"])

if __name__ == "__main__":
    # Railway 会自动注入 PORT 环境变量
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 MCP Server starting on port {port}...")
    # 必须监听 0.0.0.0 才能让云端网关访问到
    uvicorn.run(app, host="0.0.0.0", port=port)
