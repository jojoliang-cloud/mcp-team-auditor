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

# 注意这里：改成 handle_post_message (去掉了末尾的 s)
app.add_route("/sse", handle_sse, methods=["GET"])
app.add_route("/messages", sse.handle_post_message, methods=["POST"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 MCP SSE 服务器正在启动...")
    print(f"📡 SSE Endpoint: http://localhost:{port}/sse")
    uvicorn.run(app, host="0.0.0.0", port=port)
