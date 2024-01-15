"""
Evaluate the given expression
Either use the default python eval() method to evaluate the expression
or use javascript
"""

import json
import os
import re
from logging import getLogger

import requests
from zope.component import getSiteManager

LOGGER = getLogger("w20e.form")
dir_path = os.path.dirname(os.path.realpath(__file__))


def eval_python(expression, _globals, _locals=None):
    """evaluate the expression in python"""
    return eval(expression, _globals, _locals)


def eval_javascript(expression, context, function_registry=None):
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
        left = context["data"][match.group(1)]
        right = match.group(2)
        return left == right or str(left) == str(right)

    # like: data['somefield']===1
    match = re.match(r'^ *data\[[\'"](\w+)[\'"]\] *=== *(\d+) *$', expression)
    if match:
        left = context["data"][match.group(1)]
        right = match.group(2)
        return left == right or str(left) == str(right)

    # like: data['somefield']=='value'
    match = re.match(r'^ *data\[[\'"](\w+)[\'"]\] *== *[\'"](\w+)[\'"] *$', expression)
    if match:
        left = context["data"][match.group(1)]
        right = match.group(2)
        return left == right or str(left) == str(right)

    # like: data['somefield']==='value'
    match = re.match(r'^ *data\[[\'"](\w+)[\'"]\] *== *[\'"](\w+)[\'"] *$', expression)
    if match:
        left = context["data"][match.group(1)]
        right = match.group(2)
        return left == right or str(left) == str(right)

    # expressions like: data['somefield']
    match = re.match(r'^ *data\[[\'"](\w+)[\'"]\] *$', expression)
    if match:
        return context["data"][match.group(1)]

    # in some edge cases a number is larger then javascript's max number
    # for those cases just convert them to a string and hope for the best..
    safe_data = {}
    JS_MAX_NUM = 9007199254740991  # math.pow(2, 53) -1
    for k, v in context["data"].as_dict().items():
        if isinstance(v, int) and not -JS_MAX_NUM < v < JS_MAX_NUM:
            safe_data[k] = str(v)
        else:
            safe_data[k] = v
    context["data"] = safe_data

    eval_context = {}
    eval_context.update(context)

    data = {
        "expression": expression,
        "context": eval_context,
    }

    headers = {'Content-Type': 'application/json'}

    sm = getSiteManager()
    node_eval_server_url = sm.settings.get(
        'ws.engine.node_eval_server_url', 'http://localhost:3000/evaluate'
    )

    response = requests.post(
        node_eval_server_url, data=json.dumps(data), headers=headers
    )
    if not response.ok:
        LOGGER.warn(f"Could not evaluate expression: {expression}")
        LOGGER.warn(response.json()['error'])
    else:
        result = response.json()['result']
    print(f"{expression}  =>  {result}")
    return result
