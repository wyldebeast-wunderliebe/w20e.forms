from zope.interface import Interface, Attribute


class IForm(Interface):

    """ The form is the core concept of this API. A form holds at
    least four components that make up the complete form:
    
     * data
     * model
     * view
     * submission
     
    Data is an IFormData instance, that holds the actual form fields
    (variables). The Model (IFormModel) holds properties for fields,
    liek requiredness, relevance, datatype, etc. The view is the
    renderable part of the form. The submission finally, holds the way
    to store and retrieve the form data. FormModel and FormView should
    be stateless, the FormData is the only statefull class for a given
    form.
    """

    id = Attribute(""" Unique identifier for form """)

    data = Attribute(""" The form data """)

    model = Attribute(""" The form model """)

    view = Attribute(""" The form view """)

    submission = Attribute(""" The submission handler """)    
    


class IFormFactory(Interface):

    """ Factory to create a full form """

    def createForm(*args, **kwargs):

        """ Create an IForm instance. """


# The form data
#
class IFormData(Interface):

    """ Container for fields """

    def getFields():

        """ return all field names """
    
    def getField(id):

        """ return field by id """


class IField(Interface):
    
    """
    Basic field definition.
    """

    id = Attribute(""" Unique id """)

    value = Attribute(""" field's value """)


class IFormModel(Interface):

    """ Hold model for form """

    def getAllFieldProperties(self):

        """ Return all properties contained by this model. """


    def getFieldProperties(self, binding):

        """ Return the properties that bind to the given id. """


class IFieldProperties(Interface):

    """ Hold properties for field(s). The FieldProperties is contained
    in the Model and may be bound to several fields, to enable reuse.
    """

    def evalValue(value):

        """ evaluate given value against all properties """


    dataType = Attribute(""" Datatype for field. """)

    required = Attribute(""" Expression for requiredess of field. """)

    relevant = Attribute(""" Expression for relevane of field. """)

    readonly = Attribute(""" Expression for readonly-ness of field. """)

    calculate = Attribute(""" Expression for value of field. """)

    constraint = Attribute(""" Expression constraints on a field. """)    

    bind = Attribute(""" bind to the given (list of) variables """)


# Interfaces used for the view part of forms.
#
class IFormView(Interface):

    """ Form representation. May be HTML but also PDF or even audio. """

    renderer = Attribute(""" The renderer used for this view """)

    def render(form, **kwargs):

        """ Render the form to whatever you wish... The context should
        be the form, to provide context like data, model, etc.
        """


class IRenderable(Interface):

    def render(form):

        """ Render the given item. Any component in a form view needs to
        renderable. """

    id = Attribute(""" Unique id for renderable """)


class IControl(IRenderable):

    """ Control implementation. A control is an actual input
    component. Think 'Select', 'Input', etc.  Controls are bound to
    fields in the form data. The provided value should be set on the
    bound field. Controls may do some processing on the user given
    value, to transform it into something less lexical, say a date.
    """

    def processInput(data=None):

        """ Process user given input into the value to be used
        for the instance.
        """

    def lexVal(value):

        """ Return lexical value for this control, that is, the value that
        can be rendered.
        """

    type = Attribute(""" Type of the control, like 'select', 'input', etc.""")

    label = Attribute(""" Label (question?) """)

    hint = Attribute(""" Hint """)

    help = Attribute(""" Extra help """)

    alert = Attribute(""" Alert shown on errors """)    

    bind = Attribute(""" Bind to given variable """)


class IControlGroup(IRenderable):

    """ Grouping view component. Several layouts may be used, like
    flow, grid, etc.
    """

    label = Attribute(""" Label (legend? title?) """)
