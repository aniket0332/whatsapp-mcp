TOOLS = {}

def register_tool(name, tool):
    TOOLS[name] = tool

def list_tools():
    return [
        {
            "name": name,
            "description": tool["description"],
            "inputSchema": tool["schema"],
        }
        for name, tool in TOOLS.items()
    ]

def call_tool(name, args):
    if name not in TOOLS:
        raise Exception("Tool not found")

    return TOOLS[name]["handler"](args)