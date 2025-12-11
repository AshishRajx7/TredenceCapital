from app.engine.registry import register_tool

@register_tool("extract_functions")
def extract_functions(state: dict, **kwargs):
    """
    naive extraction: find function names in a single string code field
    for demo we simply split on 'def ' occurrences
    """
    code = state.get("code", "")
    funcs = []
    for part in code.split("def "):
        head = part.strip().split("(")[0]
        if head:
            funcs.append(head)
    state["functions"] = funcs
    return state

@register_tool("check_complexity")
def check_complexity(state: dict, **kwargs):
    """
    naive complexity measure: number of lines per function
    store a complexity dict and overall_complexity as average
    """
    code = state.get("code", "")
    lines = [l for l in code.splitlines() if l.strip()]
    count = len(lines)
    funcs = state.get("functions", [])
    complexity = {}
    per = max(1, len(funcs))
    complexity_score = min(100, int(count / per))
    state["complexity"] = {"per_function": complexity_score, "raw_lines": count}
  
    state["quality_score"] = state.get("quality_score", 50) - int(complexity_score / 10)
    return state

@register_tool("detect_issues")
def detect_issues(state: dict, **kwargs):
    """
    simple heuristics to detect issues: long lines and TODOs
    """
    code = state.get("code", "")
    issues = []
    for i, line in enumerate(code.splitlines(), start=1):
        if len(line) > 120:
            issues.append({"type": "long_line", "line": i})
        if "TODO" in line or "FIXME" in line:
            issues.append({"type": "todo", "line": i})
    state["issues"] = issues
    state["quality_score"] = state.get("quality_score", 50) - len(issues) * 5
    return state

@register_tool("suggest_improvements")
def suggest_improvements(state: dict, **kwargs):
    """
    propose changes based on issues and complexity
    increments quality_score
    """
    issues = state.get("issues", [])
    suggestions = []
    if issues:
        for issue in issues:
            if issue["type"] == "long_line":
                suggestions.append("wrap long lines or refactor function")
            elif issue["type"] == "todo":
                suggestions.append("address TODO items")
    else:
        suggestions.append("no issues found")

    state.setdefault("suggestions", []).extend(suggestions)
    state["quality_score"] = min(100, state.get("quality_score", 0) + 20)
    return state
