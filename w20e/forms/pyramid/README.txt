Pyramid
=======

The pyramid package provides a simple means of using w20e.forms for pyramid
apps. The package provides a specific 'file' field for pyramid, to enable
extracting filename and contents from a file in a POST/GET request, and a base
view.

Would you wish to use w20e.forms, then:

 * add w20e.forms to the eggs dependencies of your app (duh...)

 * for the view that you wish to show the actual form, override
   w20e.forms.pyramid.pyramidformview. Let's do some imports
   first. Please note that it is more convenient to use the XML
   implementation, as shown later on. Also, if you insist on using the
   Pythonic implementation, it is better to make a factory create the
   form, so you can just call the factory from your view. Anyway,
   let's go for the not-so-smart way:

      >>> from w20e.forms.form import Form
      >>> from w20e.forms.formdata import FormData
      >>> from w20e.forms.formmodel import FormModel
      >>> from w20e.forms.formview import FormView
      >>> from w20e.forms.submission.attrstorage import AttrStorage
      >>> from w20e.forms.data.field import Field
      >>> from w20e.forms.rendering.control import Input
      >>> from w20e.forms.pyramid.formview import formview as pyramidformview
      >>> import lxml.html.usedoctest
      >>> import lxml.html

   Phew, that was a load of imports. Now do the actual view
   class. It's a pretty simple form, but you should get the picture.

      >>> class yourformview(pyramidformview):
      ...   def __init__(self, context, request):
      ...     data = FormData()
      ...     data.addField(Field("foo", "some default value"))
      ...     data.addField(Field("bar"))
      ...     model = FormModel()
      ...     view = FormView()
      ...     # We'll leave the poperties out for now, check the main
      ...     # README for details
      ...     view.addRenderable(Input("input0", "Input foo", bind="foo"))
      ...     view.addRenderable(Input("input1", "Input bar here", bind="bar"))
      ...     submission = AttrStorage(attr_name="_data")
      ...     form = Form("test", data, model, view, submission)
      ...     pyramidformview.__init__(self, context, request, form)

   Now, a view for pyramid just takes a context, and a request, so let's
   create the view instance:

      >>> class Context:
      ...  """ nothing needed here, but we'll store the data in here """
      >>> class Request:
      ...   def __init__(self, params=None):
      ...     self.params = params
      >>> ctx = Context()
      >>> req = Request()
      >>> view = yourformview(ctx, req)

   Ok, we're ready for some action now. Let's try to render the form.

      >>> out = view.renderform()
      >>> html = lxml.html.fromstring(out)
      >>> print lxml.html.tostring(html)
      <form class="w20e-form" method="post" action="" id="test" enctype="multipart/form-data">
      <input type="hidden" name="w20e.forms.process" value="1"><input type="hidden" name="w20e.forms.page" value="input0"><!-- Control definition --><div id="input0" class="control input relevant">
        <div class="control-info">
          <label class="control-label" for="input-input0">Input foo</label>
          <div class="alert"></div>
        </div>
        <div class="control-widget">
            <input id="input-input0" type="text" name="input0" value="" size="20"></div>
      </div>
      <!-- Control definition -->
      <div id="input1" class="control input relevant">
        <div class="control-info">
          <label class="control-label" for="input-input1">Input bar here</label>
          <div class="alert"></div>
        </div>
        <div class="control-widget">
            <input id="input-input1" type="text" name="input1" value="" size="20"></div>
      </div>
      </form>


   Nice. Now let's give the request some content, and let the view handle the
   submission. This should result in the context having the form data stored
   in the _data attribute. formprocess is the marker used by w20e.forms
   to assume that the form is posted.

      >>> req = Request({'w20e.forms.process': 1, 'input0': 6, 'input1': 'whatever'})
      >>> view = yourformview(ctx, req)
      >>> view()
      {'status': 'completed', 'errors': {}}
      >>> ctx._data['foo']
      '6'
      >>> ctx._data['bar']
      'whatever'


XML implementation
------------------

   Using the XML implementation makes life even easier::

     from w20e.forms.pyramid.formview import xmlformview as pyramidformview
     from w20e.forms.xml.formfile import FormFile

     class yourformview(pyramidformview):

       def __init__(self, context, request):
           pyramidformview.__init__(self, context, request, FormFile("forms/yourform.xml"))

   where you have a directory 'forms' containing the XML definition
   called yourform.xml. Check the w20e.forms.xml module for details
   on XML definitions.


 * Create a template (form.pt for example) that calls the render
   method of the view::

     <p tal:content="structure python:view.renderform()"></p>


 * Wire the stuff into zcml (assuming you use that), like so::

     <view
       context=".models.YourModel"
       view=".views.yourformview"
       renderer="templates/form.pt"
       name="yourform"
       />
