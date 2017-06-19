from chameleon import PageTemplateFile
from w20e.forms.utils import find_file
from w20e.forms.registry import Registry
import os


TPL_CACHE = {}


def get_template(tpl_type):

    """ Return a template for the given type. If template path is set, try
    that, but fall back on default template."""

    if tpl_type in list(TPL_CACHE.keys()):
        return TPL_CACHE[tpl_type]

    tpl_paths = Registry.get_html_template_path()

    tpl = None

    for  tpl_path in tpl_paths:
        if tpl_path and not tpl_path.startswith("."):
            tpl = "%s/%s.pt" % (tpl_path, tpl_type)
        else:
            tpl = find_file("templates/%s/%s.pt" % (tpl_path, tpl_type), __file__)

        if os.path.isfile(tpl):
            break

    if not (tpl and os.path.isfile(tpl)):
        tpl = find_file("templates/%s.pt" % tpl_type, __file__)

    tpl = PageTemplateFile(tpl, encoding="utf-8")

    TPL_CACHE[tpl_type] = tpl

    return tpl
