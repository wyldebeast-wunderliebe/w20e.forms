""" Being there """

from w20e.forms.registry import Registry
from attrstorage import AttrStorage
from attrsstorage import AttrsStorage
from pyramidsession import PyramidSessionStorage
from methodcall import MethodCall
from none import NoSubmission

Registry.register_submission('attr', AttrStorage)
Registry.register_submission('attrs', AttrsStorage)
Registry.register_submission('methodcall', MethodCall)
Registry.register_submission('none', NoSubmission)
Registry.register_submission('pyramidsession', PyramidSessionStorage)


try:
  from emailsubmission import EmailSubmission
  Registry.register_submission('email', EmailSubmission)
except:
  pass
