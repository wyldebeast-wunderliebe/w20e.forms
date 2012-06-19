from chameleon import PageTemplateFile
from w20e.forms.utils import find_file


TEMPLATES = {}


TEMPLATES['INPUT'] = PageTemplateFile(
    find_file("templates/input.pt", __file__))

TEMPLATES['TEXTAREA'] = PageTemplateFile(
    find_file("templates/textarea.pt", __file__))

TEMPLATES['SELECT_COMPACT'] = PageTemplateFile(
    find_file("templates/select.pt", __file__))

TEMPLATES['SELECT_FULL'] = PageTemplateFile(
    find_file("templates/select_full.pt", __file__))

TEMPLATES['HIDDEN'] = PageTemplateFile(
    find_file("templates/hidden.pt", __file__))

TEMPLATES['CONTROL_HDR'] ="""<div id="%(id)s" class="control %(type)s %(extra_classes)s">
<div class="control-info">
<label class="control-label" for="input-%(id)s">%(label)s</label>
<div class="alert">%(alert)s</div>
<div class="hint">%(hint)s</div>
</div><div class="control-widget">"""

TEMPLATES['CONTROL_FTR'] ="""</div></div>"""

TEMPLATES['CONTROL_HDR_PLAIN'] ="""<div id="%(id)s" class="control %(type)s %(extra_classes)s">"""
TEMPLATES['CONTROL_FTR_PLAIN'] ="""</div>"""

TEMPLATES['CARDGROUP_TPL_HDR'] = """<fieldset id="%(id)s" class="cards %(extra_classes)s">
<div class="legend">%(label)s</div>"""
TEMPLATES['CARDGROUP_TPL_FTR'] ="""</fieldset>"""

TEMPLATES['STEPGROUP_TPL_HDR'] = """<fieldset id="%(id)s" class="steps %(extra_classes)s">
<div class="legend">%(label)s</div>"""
TEMPLATES['STEPGROUP_TPL_FTR'] ="""</fieldset>"""
TEMPLATES['STEPGROUP_NAV_PREV'] ="""<li class="stepsnav previous disabled">
</li>"""
TEMPLATES['STEPGROUP_NAV_NEXT'] ="""<li class="stepsnav next">
</li>"""
TEMPLATES['STEPGROUP_NAV_SAVE'] ="""<li class="stepsnav save">
<input type="submit" value=""/>
</li>"""

TEMPLATES['FLOWGROUP_TPL_HDR'] = """<fieldset id="%(id)s"
class="flow %(orientation)s %(extra_classes)s %(stepgroup_classes)s">
<div class="legend">%(label)s</div>"""
TEMPLATES['FLOWGROUP_TPL_FTR'] ="""</fieldset>"""

TEMPLATES['TEXT_TPL'] = """<div class="text %(extra_classes)s" id="%(id)s">%(text)s</div>"""

TEMPLATES['SELECT_ALL_HDR_TPL'] = """"""
TEMPLATES['SELECT_ALL_FTR_TPL'] = """<input class="all" type="checkbox"
name="all_%(id)s"/><label class="after">Alles</label><br/>"""

TEMPLATES['SELECT_HDR_TPL'] = """<select id="input-%(id)s" name="%(id)s" %(multiple)s size="%(size)s">"""

TEMPLATES['SELECT_FTR_TPL'] = """</select>"""

TEMPLATES['CHECK_TPL'] = """<input type="hidden" value="" name="%(id)s"/><input type="checkbox" id="input-%(id)s" value="%(value)s"
%(checked)s
name="%(id)s"/><label class="after"
for="input-%(id)s">%(label)s</label><br/>"""

TEMPLATES['RADIO_TPL'] = """<input type="radio" id="input-%(id)s-%(value)s" value="%(value)s"
%(checked)s
name="%(id)s"/><label class="after"
for="input-%(id)s-%(value)s">%(label)s</label>"""

TEMPLATES['OPTION_TPL'] = """<option value="%(value)s" %(selected)s>%(label)s</option>"""

TEMPLATES['COLORPICKER_TPL'] = """<input id="input-%(id)s" type="text"
name="%(id)s" value="%(value)s"/><div class="colorpicker"></div>"""

TEMPLATES['SUBMIT_TPL'] = PageTemplateFile(find_file("templates/submit.pt", __file__))

TEMPLATES['CANCEL_TPL'] = PageTemplateFile(find_file("templates/cancel.pt", __file__))

TEMPLATES['RICHTEXT_TPL'] = """<textarea id="input-%(id)s"
  cols="%(cols)s"
  rows="%(rows)s"
  class="%(richclass)s"
  title='%(richconfig)s'
name="%(id)s">%(value)s</textarea>
"""
