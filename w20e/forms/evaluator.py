"""
Evaluate the given expression
Either use the default python eval() method to evaluate the expression
or use javascript (pyduktape)
"""

import re
from logging import getLogger

import pyduktape2 as pyduktape

LOGGER = getLogger("w20e.form")


def eval_python(expression, _globals, _locals=None):
    """evaluate the expression in python"""
    return eval(expression, _globals, _locals)


def eval_javascript(expression, _globals, _locals=None):
    """try to import pyduktape and eval the expression"""

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

    context = pyduktape.DuktapeContext()

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

    context.set_globals(**_globals)

    # pyduktape doesn's have locals so insert it into the globals instead
    if _locals:
        context.set_globals(**_locals)

    # convert the statement to an expression or the other way around :)
    expression = expression.replace('"', "'")
    # this version of pyduktape doesn't seem to like newlines
    expression = expression.replace("\n", "")

    expression = 'new Function("with(this) { return ' + expression + ' }")()'

    try:
        result = context.eval_js(expression)
    except pyduktape.JSError as err:
        LOGGER.warning("error evaluating js expression: {}".format(expression))
        LOGGER.warning(err)
        result = None

    return result
