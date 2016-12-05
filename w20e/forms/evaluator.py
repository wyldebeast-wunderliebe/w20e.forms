"""
Evaluate the given expression
Either use the default python eval() method to evaluate the expression
or use javascript (pyduktape)
"""

import pyduktape
import threading


threadLocal = threading.local()


def eval_python(expression, _globals, _locals=None):
    """ evaluate the expression in python """
    return eval(expression, _globals, _locals)


def eval_javascript(expression, _globals, _locals=None):
    """ try to import pyduktape and eval the expression  """

    result = None

    # there's a memory leak when a duktapecontext is removed from the scope.
    # the garbagecollection doesn't work as expected.
    # workaround is to have one duktapecontext per thread
    # (we can't have 1 global, since pyduktape will raise a
    # DuktapeThreadError, so we get around this using a threadlocal)
    context = getattr(threadLocal, 'context', None)
    if context is None:
        context = pyduktape.DuktapeContext()
        threadLocal.context = context

    context.set_globals(**_globals)

    # pyduktape doesn's have locals so insert it into the globals instead
    if _locals:
        context.set_globals(**_locals)

    # not that the expression sometimes comes in as unicode. pyduktape
    # doesn't seem t like this, so make it a bytestring instead
    if isinstance(expression, unicode):
        expression = expression.encode('utf-8')


    # convert the statement to an expression or the other way around :)
    expression = 'new Function("with(this) { return ' + expression + ' }")()'

    result = context.eval_js(expression)

    # clean up globals (since it's being reused in threadlocal)
    # there is no way to unset a global variable so just set all to null
    for k, v in _globals.items():
        context.set_globals(k=None)

    if _locals:
        for k, v in _locals.items():
            context.set_globals(k=None)

    return result
