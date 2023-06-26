"""
Evaluate the given expression
Either use the default python eval() method to evaluate the expression
or use javascript (pyduktape)
"""

import js2py
from logging import getLogger
import re


LOGGER = getLogger("w20e.form")


def eval_python(expression, _globals, _locals=None):
    """evaluate the expression in python"""
    return eval(expression, _globals, _locals)


def eval_javascript(expression, _globals, _locals=None):
    """use js2py to eval the JS expression"""

    result = None

    # first some fast shortcuts which don't require a JS parser
    shortcuts = {
        "1": 1,
        "true": True,
        "0": 0,
        "false": False,
    }
    if expression in shortcuts:
        return shortcuts[expression]

    # now for some other frequent occuring expressions
    # like: data['somefield']==1
    match = re.match(r'^ *data\[[\'"](\w+)[\'"]\] *== *(\d+) *$', expression)
    if match:
        left = _globals["data"][match.group(1)]
        right = match.group(2)
        return left == right or str(left) == str(right)

    # like: data['somefield']===1
    match = re.match(r'^ *data\[[\'"](\w+)[\'"]\] *=== *(\d+) *$', expression)
    if match:
        left = _globals["data"][match.group(1)]
        right = match.group(2)
        return left == right or str(left) == str(right)

    # like: data['somefield']=='value'
    match = re.match(r'^ *data\[[\'"](\w+)[\'"]\] *== *[\'"](\w+)[\'"] *$', expression)
    if match:
        left = _globals["data"][match.group(1)]
        right = match.group(2)
        return left == right or str(left) == str(right)

    # like: data['somefield']==='value'
    match = re.match(r'^ *data\[[\'"](\w+)[\'"]\] *== *[\'"](\w+)[\'"] *$', expression)
    if match:
        left = _globals["data"][match.group(1)]
        right = match.group(2)
        return left == right or str(left) == str(right)

    # expressions like: data['somefield']
    match = re.match(r'^ *data\[[\'"](\w+)[\'"]\] *$', expression)
    if match:
        return _globals["data"][match.group(1)]

    safe_data = {}
    JS_MAX_NUM = 9007199254740991  # math.pow(2, 53) -1
    for k, v in _globals["data"].as_dict().items():
        if isinstance(v, int) and not -JS_MAX_NUM < v < JS_MAX_NUM:
            safe_data[k] = str(v)
        else:
            safe_data[k] = v
    _globals["data"] = safe_data

    context = js2py.EvalJs({**_globals, **_locals})

    try:
        result = context.eval(expression)
    except Exception as err:
        LOGGER.warning("error evaluating js expression: {}".format(expression))
        LOGGER.warning(err)
        result = None

    return result
