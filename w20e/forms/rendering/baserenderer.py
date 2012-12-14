import re
from w20e.forms.registry import Registry


# Expression for variable subsitution in labels and hints
VAREXP = re.compile('\$\{[^\}]+\}')


def cache(func):
    def get_renderer(self, renderableType, rendererType):
        key = "%s::%s" % (renderableType, rendererType)
        renderer = self._v_registry.get(key, None)
        if renderer is None:
            renderer = func(self, renderableType, rendererType)
            self._v_registry[key] = renderer
        return renderer
    return get_renderer

class BaseRenderer:

    def __init__(self, **kwargs):

        """ Initialize renderer, given global options """

        self.opts = {}
        self.opts.update(kwargs)
        self._v_registry = {}

    @cache
    def getRendererForType(self, renderableType, rendererType):

        clazz = Registry.get_renderer(renderableType, rendererType)
        return clazz()

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
                if var and var.endswith(":lexical"):
                    var = var[:-len(":lexical")]
                    value = form.getFieldValue(var, lexical=True) or ''
                else:
                    value = form.getFieldValue(var) or ''

                if not isinstance(value, unicode):
                    if not hasattr(value, "decode"):
                        value = str(value)
                    value = value.decode('utf-8')
                return value
            except:
                return match.group()

        # process labels and hints
        if 'label' in fmtmap:
            fmtmap['label'] = VAREXP.sub(replaceVars, fmtmap['label'])
        if 'hint' in fmtmap:
            fmtmap['hint'] = VAREXP.sub(replaceVars, fmtmap['hint'])
        if 'text' in fmtmap:
            fmtmap['text'] = VAREXP.sub(replaceVars, fmtmap['text'])
        if 'placeholder' in fmtmap:
            fmtmap['placeholder'] = VAREXP.sub(replaceVars,
                    fmtmap['placeholder'])

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
