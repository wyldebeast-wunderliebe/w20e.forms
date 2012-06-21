""" Being there """

from control import *
#from group import Group
from renderables import *
from w20e.forms.registry import Registry


Registry.register_renderable('input', Input)
Registry.register_renderable('hidden', Hidden)
Registry.register_renderable('password', Password)
Registry.register_renderable('select', Select)
Registry.register_renderable('range', Range)
Registry.register_renderable('group', None)
Registry.register_renderable('text', Text)
Registry.register_renderable('richtext', RichText)
Registry.register_renderable('file', File)
Registry.register_renderable('submit', Submit)
Registry.register_renderable('cancel', Cancel)
Registry.register_renderable('checkbox', Checkbox)
