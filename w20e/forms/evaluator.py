"""
Evaluate the given expression
Either use the default python eval() method to evaluate the expression
or use javascript (pyduktape)
"""
try:
    import pyduktape
except ImportError:
    pyduktape = None

# from zope import interface
# from zope.component import getUtility
import threading


# Based on tornado.ioloop.IOLoop.instance() approach.
# See https://github.com/facebook/tornado
class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance


class EvalJSUtil(SingletonMixin):
    def __init__(self):
        # note: need the runtime here, to prevent
        # "Failed to allocate new JSRuntime" error

        if pyduktape:
            self.pyduktape_cx = pyduktape.DuktapeContext()

    def eval(self, expression, _globals, _locals=None):
        """ import pyduktape and eval the expression  """

        if not pyduktape:
            raise ("Pyduktape not available. "
                   "Please install pyduktape")

        self.pyduktape_cx.set_globals(**_globals)

        # pyduktape doesn's have locals so insert it into the globals instead
        if _locals:
            self.pyduktape_cx.set_globals(**_locals)

        result = self.pyduktape_cx.eval_js(expression)

        # clean up globals, so we can reuse the context
        # and work around a potential memory leak

        for k, v in _globals.items():
            self.pyduktape_cx.set_globals(k=None)

        if _locals:
            for k, v in _locals.items():
                self.pyduktape_cx.set_globals(k=None)

        return result


def eval_python(expression, _globals, _locals=None):
    """ evaluate the expression in python """
    return eval(expression, _globals, _locals)


evalJSUtil = EvalJSUtil()


def eval_javascript(expression, _globals, _locals=None):
    """ import pyduktape and eval the expression  """
    return evalJSUtil.eval(expression, _globals, _locals)
