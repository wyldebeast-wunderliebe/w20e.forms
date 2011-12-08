from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class StepGroupRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        print >> out, TEMPLATES['STEPGROUP_TPL_HDR'] % \
                renderer.createFormatMap(form, renderable, **kwargs)

        print >> out, "<ul class='stepsnav'>"
        print >> out, TEMPLATES['STEPGROUP_NAV_PREV']

        steps = renderable.getRenderables()

        for i in range(len(steps)):
            cls = (i == 0 and "first" or\
                    (i == len(steps) - 1 and "last" or ""))
            print >> out, """<li class="%s" id="step-%s">%s</li>""" % \
                    (cls, steps[i].id, steps[i].label)
        print >> out, TEMPLATES['STEPGROUP_NAV_NEXT']
        print >> out, TEMPLATES['STEPGROUP_NAV_SAVE']
        print >> out, "</ul>"

        currentpage = kwargs.get('currentpage', None)

        for item in renderable.getRenderables():

            stepgroup_classes = "step"
            if currentpage and item.id == currentpage:
                stepgroup_classes += " active"

            renderer.render(form, item, out,
                    stepgroup_classes=stepgroup_classes, **kwargs)

        print >> out, TEMPLATES['STEPGROUP_TPL_FTR']
