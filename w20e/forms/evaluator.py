"""
Evaluate the given expression
Either use the default python eval() method to evaluate the expression
or use javascript (spidermonkey)
"""
try:
    import spidermonkey
except ImportError:
    spidermonkey = None

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

    """ There seems to be a memory leak issue with spidermonkey
    context creation. So wrapping this in a util class and
    ceating a single context which is reused solves the issue I hope
    """

    def __init__(self):
        # note: need the runtime here, to prevent
        # "Failed to allocate new JSRuntime" error

        if spidermonkey:
            self.spidermonkey_rt = spidermonkey.Runtime()
            self.spidermonkey_cx = self.spidermonkey_rt.new_context()

    def eval(self, expression, _globals, _locals=None):
        """ import spidermonkey and eval the expression  """

        if not spidermonkey:
            raise ("Spidermonkey not available. "
                   "Please install python-spidermonkey")

        for k, v in _globals.items():
            self.spidermonkey_cx.add_global(k, v)

        if _locals:
            for k, v in _locals.items():
                self.spidermonkey_cx.add_global(k, v)

        result = self.spidermonkey_cx.execute(expression)

        # clean up globals, so we can reuse the context
        # and work around the memory leak
        for k, v in _globals.items():
            self.spidermonkey_cx.rem_global(k)

        if _locals:
            for k, v in _locals.items():
                self.spidermonkey_cx.rem_global(k)

        return result


def eval_python(expression, _globals, _locals=None):
    """ evaluate the expression in python """
    return eval(expression, _globals, _locals)


evalJSUtil = EvalJSUtil()


def eval_javascript(expression, _globals, _locals=None):
    """ import spidermonkey and eval the expression  """

    return evalJSUtil.eval(expression, _globals, _locals)
