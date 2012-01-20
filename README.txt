The w20e.forms package provides a powerful API for creating and
handling electronic forms. The package is loosely based on XForms
concepts (and Socrates QE, a Java implementation). The package intends
to provide a drop-in alternative for standard plone, pyramid and
django solutions, but is useable in any framework (or without a
framework...).


Core concepts
=============

The core concepts are as follows (so you can quickly decide whether
you like this approach or not):

A form is a container for/composition of four things:

1. data
2. model
3. view
4. submission

This clearly separates the data, the data's properties (datatype,
whether something is required or not, etc.) and the renderable part of
the form. This is also the main difference between this API and other
solutions (afaik...). Where the usual approach is to define a form
based on a *Schema* or other data-centered notion, like so::

  foo = String("id", "label", validator=somefunction)

the approach of w20e.forms is to define::

  foo = Field("fid")
  props = FieldProperties("pid", ["fid"], required=True, datatype=int)
  ctrl = Input("cid", "label", bind="fid")

where the properties and control are *bound* to the variable. This
enables controls in your form that are not bound to any data you wish
to collect, sharing of properties, etc.

Another important difference is that the API provides a structured way
of defining properties for data, instead of having to define your own
validation. See section 1.2 for details.


Data
----

The data holds the variables you wish to collect with this form. A
variable simply has an id, and if you like a default value.


Model
-----

The model holds all properties for a given form, like readonly-ness,
requiredness, datatyping for variables, relevance, etc. All these
properties are calculated from expressions, in this case Python
expressions, so requiredness is not just true or false, it can be
calculated based on an expression that can include other variables in
your data. All variables from the form data are available in
expressions via the 'data' dict, so if variable 'foo' would be
required if variable 'bar' was set to 666, this can be expressed like
so in the properties bound to foo:

 ... required="data['bar'] == 666" ...

In general, all expressions are eval-ed to something true or
false. The model offers the following properties:

* required: is a variable required or not?
* relevant: is the variable relevant? Like maiden name would be irrelevant
  when gender is male. In general, the related control/widget for irrelevant 
  variables would not be shown.
* readonly: can a person change the value of a variable?
* calculate: in stead of letting a person set the value of a variable, the
  variable is calculated.
* constraint: check whether the expression evaluates to True.
* datatype: datatype for the variable, like int, string, or more complex
  variables.

Properties are bound to variables by a bind attribute. A set of
properties can be bound to a series of variables.


View
----

The view (or FormView) is the actual visible part (or audible for that
matter) of the form. The view can be rendered and holds a collection
of widgets or controls, that are bound to variables. More than one
control can bind to the same variable. Controls can be grouped in
groups for layout purposes, like flow layout or card layout (tabs).

In label and hint texts of controls you can use lexical values of
variables by using the expression ${<var name>}. This way you can refer to
values given in other variables from your labels and hints.


Basic use
=========

Ok, enough theory, let's do something for real.

A form is produced by hand, or by using a factory: this should take
care of producing a form holding the necessary stuff.

Let's get the imports over with...

      >>> import sys
      >>> from interfaces import *
      >>> from zope.interface import implements
      >>> from formdata import FormData
      >>> from formview import FormView
      >>> from formmodel import FormModel
      >>> from data.field import Field
      >>> from model.fieldproperties import FieldProperties
      >>> from rendering.control import Input, Select, Option
      >>> from rendering.group import FlowGroup
      >>> from form import Form, FormValidationError
      >>> from rendering.html.renderer import HTMLRenderer
      >>> from submission.attrstorage import AttrStorage

Creating a form
---------------

Now let us create a factory class

      >>> class FormFactory():
      ...   implements(IFormFactory)
      ...   def createForm(self):
      ...     data = FormData()
      ...     data.addField(Field("field0"))
      ...     data.addField(Field("field1", "foo"))
      ...     data.addField(Field("field2", "bar"))
      ...     data.addField(Field("field3"))
      ...     view = FormView()
      ...     grp = FlowGroup("grp0", label="Group 0")
      ...     grp.addRenderable(Input("input2", "Input 2", bind="field0"))
      ...     view.addRenderable(Input("input0", "First name", bind="field0"))
      ...     view.addRenderable(Input("input1", "Last name", bind="field1"))
      ...     view.addRenderable(Select("select0", "Select me!", options=[], bind="field2", with_empty=True))
      ...     view.addRenderable(grp)
      ...     model = FormModel()
      ...     model.addFieldProperties(FieldProperties("prop0", ["field0"], required="True"))
      ...     model.addFieldProperties(FieldProperties("prop1", ["field1", "field2"], relevant="data['field0']"))
      ...     submission = AttrStorage(attr_name="_data")
      ...     return Form("test", data, model, view, submission)

      >>> ff = FormFactory()
      >>> form = ff.createForm()

By now, we should have a form where field0 is required, and field1 and
field2 are only relevant if field0 is filled in.

      >>> print len(form.data.getFields())
      4

      >>> props = form.model.getFieldProperties("field0")
      >>> props[0].id
      'prop0'

      >>> len(props)
      1

      >>> field0 = form.data.getField("field0")
      >>> field0.id
      'field0'

      >>> field0.value

In the meanwhile, field1 and field2 should be irrelevant, given that field0
has no value

      >>> form.model.isRelevant("field1", form.data)
      False
      >>> form.model.isRelevant("field2", form.data)
      False

Validation should fail, given that field0 is required.

      >>> try:
      ...   form.validate()
      ... except FormValidationError:
      ...   print sys.exc_info()[1].errors['field0']
      ['required']

      >>> form.data.getField("field0").value = "pipo"
      >>> form.validate()
      True

      >>> field0.value
      'pipo'

By now, field1 and field2 should also be relevant

      >>> form.model.isRelevant("field1", form.data)
      True
      >>> form.model.isRelevant("field2", form.data)
      True

Display
-------

The following section will assume rendering to HTML. This will most
likely cover nigh 100% of the use cases...
Now for some display parts. An irrelevant control should
not have a class 'relevant', otherwise it should have it... This
enables specific styling, like 'display: none'.

      >>> form.data.getField('field0').value = None
      >>> field = form.view.getRenderable('input1')
      >>> renderer = HTMLRenderer()
      >>> renderer.render(form, field, sys.stdout)
      <div id="input1" class="control input ">
      <label for="input-input1">Last name</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-input1" type="text" name="input1" value="foo" size="20"/>
      </div>

      >>> form.data.getField('field0').value = 'pipo'
      >>> field = form.view.getRenderable('input1')
      >>> renderer = HTMLRenderer()
      >>> renderer.render(form, field, sys.stdout)
      <div id="input1" class="control input relevant">
      <label for="input-input1">Last name</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-input1" type="text" name="input1" value="foo" size="20"/>
      </div>

      >>> field = form.view.getRenderable('input0')
      >>> renderer.render(form, field, sys.stdout)
      <div id="input0" class="control input relevant required">
      <label for="input-input0">First name</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-input0" type="text" name="input0" value="pipo" size="20"/>
      </div>
      
How 'bout those extra classes...

      >>> renderer.render(form, field, sys.stdout, extra_classes="card")
      <div id="input0" class="control input card relevant required">
      <label for="input-input0">First name</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-input0" type="text" name="input0" value="pipo" size="20"/>
      </div>

      >>> select = form.view.getRenderable('select0')
      >>> renderer.render(form, select, sys.stdout)
      <div id="select0" class="control select relevant">
      <label for="input-select0">Select me!</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <select id="input-select0" name="select0"  size="1">
      <option value="" >Maak een keuze</option>
      </select>
      </div>

Do we actually get grouped controls?

      >>> nested_input = form.view.getRenderable('input2')
      >>> nested_input.id
      'input2'

Submission
----------

Finally when the form is rendered, filled in by someone, and
validated, the data should normally go somewhere. This is by way of
submission. We defined submission to be AttrStorage, something that
stores the data in an attribute on some context. This is a case that
could be used in many frameworks, at least plone and pyramid.

Let's see what it does:

      >>> class Context:
      ...   """ some context """
      >>> ctx = Context()
      >>> form.submission.submit(form, ctx)

The context now should hold the data in an attribute. We specified the
name of the attribute to be '_data', so let's check:

     >>> ctx._data.getField('field0').value
     'pipo'


Beyond the basics
=================

Well, this is all very simple, and it is quite likely that you would
wish for something a bit more usefull. All parts of the form are there
to be extended. Take for instance the FormView. A developer (or end
user) should be able to:

 * create a full HTML form;
 * use a generated HTML form (this is wat the base implementation does);
 * create a PDF form.

The factory is also an important part of the form process. A factory
can be imagined to be one of the following:

 * produced from a Schema (content type);
 * produced from an XML definition, for example an XForms instance from
   OpenOffice.

Forms in general should be:

 * submitable to a range of handlers, like email, database storage,
   content type storage;
 * easy to validate 'live;
 * enable multi-page.

More detailed tests:

We'd like to check whether lookup of a control by bind works, so as to
be able to process values into lexical values. This is especially
interesting when using selects: we'd expect to see the label not the
value in lexical space.

      >>> data = FormData()
      >>> data.addField(Field("f0", "opt0"))
      >>> view = FormView()
      >>> opts = [Option("opt0", "Option 0"), Option("opt1", "Option 1")]
      >>> view.addRenderable(Select("sel0", "Select 0", bind="f0", options=opts))
      >>> ctl = view.getRenderableByBind("f0")
      >>> ctl.lexVal("opt0")
      'Option 0'


Can we use variable substitution in labels and hints? Yes, we can!

      >>> data = FormData()
      >>> data.addField(Field("f0", "Pipo"))
      >>> data.addField(Field("f1"))
      >>> view = FormView()
      >>> view.addRenderable(Input("in0", "First name", bind="f0"))
      >>> view.addRenderable(Input("in1", "Last name for ${f0}", bind="f1"))
      >>> model = FormModel()
      >>> form = Form("test", data, model, view, None)
      >>> renderer = HTMLRenderer()
      >>> field = form.view.getRenderable('in1')
      >>> renderer.render(form, field, sys.stdout)
      <div id="in1" class="control input relevant">
      <label for="input-in1">Last name for Pipo</label>
      <div class="alert"></div>
      <div class="hint"></div>
      <input id="input-in1" type="text" name="in1" value="" size="20"/>
      </div>

Let's delve into input processing a bit...
A simple input should just return it's own value

  >>> data = {'pipo': 'lala'}
  >>> ctl = Input("pipo", "f0", "Some input")
  >>> ctl.processInput(data)
  'lala'


Registering your own stuff
==========================

w20e.forms is not a complete library for forms, and it will never be
this, since most people have very specific needs, like a specific
widget, a custom version of an input field, etc. The API facilitates
in this by using a global registry to register extensions.

The global registry is available like so:

  >>> from w20e.forms.registry import Registry

and offers a number of class methods to register stuff. 

Let's for exampe register a new renderer for an input:


Vocabularies
------------

w20e.forms enables use of vocabularies to limit possible answers to a
given list. This is a feature that is generally used with select
widgets. A vocabulary is a 'named' factory that creates a list of
options. 

Register like so:

>>> def make_vocab():
...   return [Option('0', 'Opt 0'), Option('1', 'Opt 1')]
... Registry.register_vocab('foovocab', make_vocab)
... sel = Select("select0", "Select me!", vocab=make_vocab,
...   bind="field2", with_empty=True))


Required, Relevant, Readonly
----------------------------

In a form you'll usually want to say things like: this control need
only be shown whan the answer to that question is 'x', or that
question is required whenever the answer to somethind else is 'y'.

w20e.forms enables this using expressions. The epxressions are set as
properties in variables, by their 'bind' attribute. So in the form
model you may have a property set named 'req', that makes
variable 'foo' required like so:

  model.addFieldProperties(FieldProperties("req", ["foo"], required="True"))

Obviously in general you want something a bit more flexible than that,
like checking for other data that has been entered. All form data is
made available to the expression within the 'data' variable, that is a
dict. So checking upon some other variable, goes like this:

  model.addFieldProperties(FieldProperties("req", ["foo"],
    required="data['bar'] == 42"))

So only if the answer to 'bar' is 42, 'foo' is required. Relevance,
requiredness and readonly-ness all work like this.

You may even add your own expression context to the engine, to call
methods on objects, etc.

Go like this, assuming your object is obj:

>>> registry.register_expr_context('mycontext', obj)
... model.addFieldProperties(FieldProperties("req", ["foo"],
...   relevant="mycontext.some_method())
