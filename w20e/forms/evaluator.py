"""
Evaluate the given expression
Either use the default python eval() method to evaluate the expression
or use javascript (pyduktape)
"""


def eval_python(expression, _globals, _locals=None):
    """ evaluate the expression in python """
    return eval(expression, _globals, _locals)


def eval_javascript(expression, _globals, _locals=None):
    """ try to import pyduktape and eval the expression  """

    import pyduktape
    context = pyduktape.DuktapeContext()

    context.set_globals(**_globals)

    # pyduktape doesn's have locals so insert it into the globals instead
    if _locals:
        context.set_globals(**_locals)

    return context.eval_js(expression)
