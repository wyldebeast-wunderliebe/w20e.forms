from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class StepGroupRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):


        print >> out, TEMPLATES['STEPGROUP_TPL_HDR'] % renderer.createFormatMap(form, renderable, **kwargs)

        print >> out, "<ul>"
        print >> out, TEMPLATES['STEPGROUP_NAV_PREV']

        steps = renderable.getRenderables()

        for i in range(len(steps)):
            cls = (i == 0 and "first" or (i == len(steps) - 1 and "last" or ""))
            print >> out, """<li class="%s" id="step-%s">%s</li>""" % (cls, steps[i].id, steps[i].label)
        print >> out, TEMPLATES['STEPGROUP_NAV_NEXT']
        print >> out, TEMPLATES['STEPGROUP_NAV_SAVE']      
        print >> out, "</ul>"

        for item in renderable.getRenderables():

            renderer.render(form, item, out, extra_classes="step", **kwargs)

        print >> out, TEMPLATES['STEPGROUP_TPL_FTR']
