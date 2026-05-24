from fastapi import FastAPI, Request
from app.mcp.registry import list_tools, call_tool
import app.tools.echo

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/mcp")
async def mcp(request: Request):
    body = await request.json()

    method = body.get("method")
    params = body.get("params", {})
    req_id = body.get("id")

    try:
        if method == "tools/list":
            result = list_tools()

        elif method == "tools/call":
            result = call_tool(
                params.get("name"),
                params.get("arguments", {})
            )

        else:
            raise Exception("Unknown method")

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": result
        }

    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32000,
                "message": str(e)
            }
        }