from chameleon import PageTemplateFile
from w20e.forms.utils import find_file
from w20e.forms.registry import Registry


def get_template(tpl_type):

    """ Return a template for the given type. If template path is set, try
    that, but fall back on default template."""

    tpl_path = Registry.get_html_template_path()

    if tpl_path and not tpl_path.startswith("."):
        try:
            return PageTemplateFile("%s/%s.pt" % (tpl_path, tpl_type))
        except:
            pass

    return PageTemplateFile(find_file("templates/%s/%s.pt" % (tpl_path,
                                                              tpl_type),
                                      __file__))


TEMPLATES = {}

TEMPLATES['CONTROL_HDR'] ="""<div id="%(id)s" class="control %(type)s %(extra_classes)s">
<div class="control-info">
<label class="control-label" for="input-%(id)s">%(label)s</label>
<div class="alert">%(alert)s</div>
<div class="hint">%(hint)s</div>
</div><div class="control-widget">"""

TEMPLATES['CONTROL_FTR'] ="""</div></div>"""

TEMPLATES['CONTROL_HDR_PLAIN'] ="""<div id="%(id)s" class="control %(type)s %(extra_classes)s">"""
TEMPLATES['CONTROL_FTR_PLAIN'] ="""</div>"""

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

TEMPLATES['SELECT_ALL_HDR_TPL'] = """"""
TEMPLATES['SELECT_ALL_FTR_TPL'] = """<input class="all" type="checkbox"
name="all_%(id)s"/><label class="after">Alles</label><br/>"""
