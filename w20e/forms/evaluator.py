from .pyduktape_evaluator import eval_javascript as pyduktape_eval_javascript

# from .quickjs_evaluator import eval_javascript as quickjs_eval_javascript


def eval_python(expression, _globals, _locals=None):
    """Evaluate the expression using Python's eval"""
    return eval(expression, _globals, _locals)


def eval_javascript(expression, _globals, _locals=None):
    """Evaluate a JavaScript expression using quickjs"""
    return pyduktape_eval_javascript(expression, _globals, _locals)
