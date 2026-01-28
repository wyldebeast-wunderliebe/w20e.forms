"""
Evaluate the given expression
Either use the default Python eval() method or evaluate using JavaScript (via quickjs)
"""

import json
import re
import logging
from quickjs import Context, JSException

LOGGER = logging.getLogger("w20e.form")

JS_MAX_NUM = 9007199254740991  # 2^53 - 1


def eval_javascript(expression, _globals, _locals=None, timeout_ms=1000):
    """Evaluate a JavaScript expression using quickjs"""

    result = None

    # Shortcuts for common constant expressions
    shortcuts = {
        "1": 1,
        "true": True,
        "0": 0,
        "false": False,
    }
    if expression in shortcuts:
        return shortcuts[expression]

    # Simple regex optimizations
    patterns = [
        (
            r'^ *data\[[\'"](\w+)[\'"]\] *== *(\d+) *$',
            lambda d, m: d.get(m[1]) == int(m[2]),
        ),
        (
            r'^ *data\[[\'"](\w+)[\'"]\] *=== *(\d+) *$',
            lambda d, m: d.get(m[1]) == int(m[2]),
        ),
        (
            r'^ *data\[[\'"](\w+)[\'"]\] *== *[\'"](\w+)[\'"] *$',
            lambda d, m: str(d.get(m[1])) == m[2],
        ),
        (
            r'^ *data\[[\'"](\w+)[\'"]\] *=== *[\'"](\w+)[\'"] *$',
            lambda d, m: str(d.get(m[1])) == m[2],
        ),
        (r'^ *data\[[\'"](\w+)[\'"]\] *$', lambda d, m: d.get(m[1])),
    ]
    for pattern, func in patterns:
        match = re.match(pattern, expression)
        if match:
            return func(_globals["data"], match)

    # Fallback to JS evaluation
    context = Context()
    context.set_time_limit(timeout_ms)

    raw_data = _globals["data"].as_dict()
    data = {}

    # Sanitize JS-incompatible numbers
    for k, v in raw_data.items():
        if isinstance(v, int) and not -JS_MAX_NUM < v < JS_MAX_NUM:
            data[k] = str(v)
        else:
            data[k] = v

    js_data = json.dumps(data)
    context.eval(f"var data = {js_data};")

    # Add other globals if needed
    # for k, v in (_globals or {}).items():
    #     if k != "data":
    #         context.set(k, v)
    # if _locals:
    #     for k, v in _locals.items():
    #         context.set(k, v)

    # JS prefers single quotes; strip newlines to avoid syntax errors
    expression = expression.replace('"', "'").replace("\n", "")
    wrapped = f'new Function("with(this) {{ return {expression} }}")()'

    try:
        result = context.eval(wrapped)
    except JSException as err:
        LOGGER.warning("Error evaluating JS expression: %s", expression)
        LOGGER.warning(err)
        result = None

    return result
