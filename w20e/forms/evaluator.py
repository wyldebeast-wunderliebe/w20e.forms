"""
Evaluate the given expression
Either use the default python eval() method to evaluate the expression
or use javascript
"""

import javascript
from logging import getLogger
import re


LOGGER = getLogger("w20e.form")


def eval_python(expression, _globals, _locals=None):
    """evaluate the expression in python"""
    return eval(expression, _globals, _locals)


def eval_javascript(expression, _globals, _locals=None):
    """try to eval the expression with javascript"""

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

    # in some edge cases a number is larger then javascript's max number
    # for those cases just convert them to a string and hope for the best..
    safe_data = {}
    JS_MAX_NUM = 9007199254740991  # math.pow(2, 53) -1
    for k, v in _globals["data"].as_dict().items():
        if isinstance(v, int) and not -JS_MAX_NUM < v < JS_MAX_NUM:
            safe_data[k] = str(v)
        else:
            safe_data[k] = v
    _globals["data"] = safe_data

    eval_context = {}
    eval_context.update(_globals)
    eval_context.update(_locals)

    maskedEval = javascript.require('./masked-eval.js')

    try:
        result = maskedEval.evaluateExpression(expression, eval_context)
    except javascript.JavaScriptError as err:
        LOGGER.warning("error evaluating js expression: {}".format(expression))
        LOGGER.warning(err)

    return result
