from app.mcp.registry import register_tool

def handler(input_data):
    text = input_data.get("text", "")
    return {"reply": text}

register_tool(
    "echo",
    {
        "description": "Echo back the input text",
        "schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"}
            },
            "required": ["text"]
        },
        "handler": handler
    }
)