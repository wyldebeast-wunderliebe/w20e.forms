class Registry:

    """ Global registry for forms """

    submission_types = {}
    rendering_types = {}
    renderers = {}
    vocabs = {}
    funcs = {}
    html_tpl_path = []
    converters = {}
    validators = {}

    @staticmethod
    def set_html_template_path(name):

        Registry.html_tpl_path = [name]

    @staticmethod
    def add_html_template_path(name):

        Registry.html_tpl_path.append(name)

    @staticmethod
    def get_html_template_path():

        return Registry.html_tpl_path

    @staticmethod
    def register_submission(name, factory):

        Registry.submission_types[name] = factory

    @staticmethod
    def get_submission(name):

        return Registry.submission_types.get(name, None)

    @staticmethod
    def register_renderable(name, factory):

        Registry.rendering_types[name] = factory

    @staticmethod
    def get_renderable(name):

        return Registry.rendering_types.get(name, None)

    @staticmethod
    def get_registered_renderables():

        return Registry.rendering_types.keys()

    @staticmethod
    def register_renderer(name, tpe, factory):
        Registry.renderers[(name, tpe)] = factory

    @staticmethod
    def get_renderer(name, tpe):
        return Registry.renderers.get((name, tpe), None)

    @staticmethod
    def register_vocab(name, factory):

        Registry.vocabs[name] = factory

    @staticmethod
    def get_vocab(name):

        return Registry.vocabs.get(name, None)

    @staticmethod
    def register_expr_context(name, context):

        Registry.funcs[name] = context

    @staticmethod
    def register_converter(name, converter):

        Registry.converters[name] = converter

    @staticmethod
    def get_converter(name):

        if name in Registry.converters:
            return Registry.converters[name]

    @staticmethod
    def register_validator(name, validator):

        Registry.validators[name] = validator

    @staticmethod
    def get_validator(name):

        if name in Registry.validators:
            return Registry.validators[name]
