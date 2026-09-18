"""
Tools available to the GAIA agent.
Each tool is a plain function: str -> str.
"""

import ast
import operator
import requests

try:
    from ddgs import DDGS  # pip install ddgs
except ImportError:
    from duckduckgo_search import DDGS  # fallback older package name


def web_search(query: str) -> str:
    """Search the web and return short snippets from the top results."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    if not results:
        return "No results found."
    lines = []
    for r in results:
        title = r.get("title", "")
        body = r.get("body", "")
        href = r.get("href", "")
        lines.append(f"- {title}: {body} ({href})")
    return "\n".join(lines)


def wikipedia_lookup(query: str) -> str:
    """Look up a Wikipedia page summary."""
    resp = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 1,
        },
        timeout=15,
    )
    resp.raise_for_status()
    hits = resp.json().get("query", {}).get("search", [])
    if not hits:
        return "No Wikipedia page found."
    title = hits[0]["title"]

    summary_resp = requests.get(
        f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}",
        timeout=15,
    )
    summary_resp.raise_for_status()
    data = summary_resp.json()
    return f"{data.get('title')}: {data.get('extract', 'No summary available.')}"


_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Safely evaluate a basic arithmetic expression, e.g. '(3 + 4) * 2'."""
    try:
        tree = ast.parse(expression, mode="eval")
        return str(_eval_node(tree.body))
    except Exception as e:
        return f"Could not evaluate expression: {e}"


def read_text_file(path: str) -> str:
    """Read and return the contents of a downloaded text/CSV file."""
    if not path:
        return "No file was provided for this task."
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()[:4000]
    except Exception as e:
        return f"Could not read file: {e}"


TOOLS = {
    "web_search": web_search,
    "wikipedia": wikipedia_lookup,
    "calculator": calculator,
    "read_file": read_text_file,
}

TOOL_DESCRIPTIONS = """\
- web_search[query]: search the web, returns a few short result snippets
- wikipedia[topic]: get a Wikipedia summary for a topic
- calculator[expression]: evaluate a basic arithmetic expression
- read_file[path]: read the text content of a local file (use for downloaded task files)
"""
