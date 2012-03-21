from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PloneRichTextRenderer:
    implements(IControlRenderer)

    _template = ViewPageTemplateFile("templates/plone_wysiwyg.pt")

    def render(self, renderer, form, renderable, out, **kwargs):
        context = kwargs.get('context', None)
        request = kwargs.get('request', None)

        self.request = request
        self.context = context
        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)
        args = {}
        args['context'] = context
        args['id'] = fmtmap.get('id', "default_id")
        args['name'] = renderable.bind
        args['value'] = form.data[renderable.bind] or ""
        args['request'] = request
        result = self._template(**args)

        fmtmap['id'] = "wrapper-%s" % fmtmap['id']
        fmtmap['value'] = form.data[renderable.bind] or ""
        fmtmap['richconfig'] = renderer.opts.get('richconfig', '')
        fmtmap['richclass'] = 'wysiwyg'
        fmtmap['cols'] = renderable.cols or 80
        fmtmap['rows'] = renderable.rows or 3

        # added to guarantee backwards compatibilty (WGH)
        if not 'cols' in fmtmap:
            fmtmap['cols'] = '30'

        print >> out, TEMPLATES['CONTROL_HDR'] % fmtmap
        print >> out, result
        print >> out, TEMPLATES['CONTROL_FTR'] % fmtmap
