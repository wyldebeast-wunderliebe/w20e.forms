import re
from w20e.forms.registry import Registry


# Expression for variable subsitution in labels and hints
VAREXP = re.compile('\$\{[^\}]+\}')


class BaseRenderer:

    def __init__(self, **kwargs):

        """ Initialize renderer, given global options """

        self.opts = {}
        self.opts.update(kwargs)

    def getRendererForType(self, renderableType, rendererType):

        return Registry.get_renderer(renderableType, rendererType)

    def getType(self, renderable):

        """ Return the renderable's type (or class) """

        if hasattr(renderable, 'type'):

            return renderable.type

        return renderable.__class__.__name__

    def createFormatMap(self, form, renderable, **extras):

        """ Create a dict out of the renderable's properties """

        fmtmap = renderable.__dict__.copy()
        fmtmap.update(extras)

        def replaceVars(match):

            try:
                var = match.group()[2:-1]
                value = form.getFieldValue(var) or ''
                return str(value) # TODO: propably utf-8 issues here..
            except:
                return match.group()

        # process labels and hints
        if 'label' in fmtmap:
            fmtmap['label'] = VAREXP.sub(replaceVars, fmtmap['label'])
        if 'hint' in fmtmap:
            fmtmap['hint'] = VAREXP.sub(replaceVars, fmtmap['hint'])
        if 'text' in fmtmap:
            fmtmap['text'] = VAREXP.sub(replaceVars, fmtmap['text'])

        # defaults
        extra_classes = {'relevant': True, 'required': False,
                'readonly': False, 'error': False}

        # Let's see whether we got properties here...
        try:
            if hasattr(renderable, 'bind') and renderable.bind:
                # Requiredness
                if form.model.isRequired(renderable.bind, form.data):
                    extra_classes["required"] = True

                if not form.model.isRelevant(renderable.bind, form.data):
                    extra_classes["relevant"] = False

                # Read only
                if form.model.isReadonly(renderable.bind, form.data):
                    extra_classes["readonly"] = True

            elif hasattr(renderable, 'getRenderables') and \
                    callable(renderable.getRenderables):

                # Group relevance
                if not form.model.isGroupRelevant(renderable, form.data):
                    extra_classes["relevant"] = False

        except:
            pass

        if extras.get("errors", None) and \
               extras['errors'].get(renderable.bind, None):

            extra_classes['error'] = True

            if getattr(renderable, 'alert', ''):
                fmtmap['alert'] = renderable.alert
            else:
                fmtmap['alert'] = "; ".join(extras['errors'][renderable.bind])

        else:

            fmtmap['alert'] = ''

        if "extra_classes" in fmtmap:
            fmtmap['extra_classes'] = " ".join([fmtmap['extra_classes']] + \
                    [key for key in extra_classes.keys()
                        if extra_classes[key]])
        else:
            fmtmap['extra_classes'] = " ".join([key for key in
                extra_classes.keys() if extra_classes[key]])

        fmtmap['type'] = self.getType(renderable)

        return fmtmap
