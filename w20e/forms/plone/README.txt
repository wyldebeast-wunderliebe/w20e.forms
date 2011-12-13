w20e.forms for Plone
====================

Basic forms
-----------

Needs more documentation, examples and tests... 


Archetypes
----------
This directory contains classes needed to enable ATCT content to use the
w20e.forms stuff. This is basically only a base class and a submission
implementation.

To make your ATCT class use this API, you'll need to extend the base
class, like so:


from w20e.forms.atct.baseobject import ATCTBaseObject
from Products.Archetypes.atapi import *


class MyContentType(BaseContent, ATCTBaseObject):

    """ My class using w20e.forms """

    # We boldly assume you'll also create this marker interface...
    #
    implements(interfaces.IMyContentType)

    def __init__(self, oid, **kwargs):

        BaseContent.__init__(self, oid, **kwargs)
        ATCTBaseObject.__init__(self)


Now, also you need to create a factory for the form for this class:

  <adapter
    factory=".myform.MyForm"
    provides="w20e.forms.interfaces.IForm"
    for=".interfaces.IMyContentType"
  />


The factory can be something like shown in the README.txt in the main
dir. Now make your own view and edit actions. The edit is simply:

configure.zcml:

  <browser:page
    for="..content.interfaces.IMyContentType"
    name="my_edit"
    class=".myedit.MyEdit"
    permission="zope2.View"
  />

view class:

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView


class MyEdit(BrowserView):

    template = ViewPageTemplateFile('myedit.pt')


    def __call__(self):
        
        return self.template()

template (snippet):

    <metal:main fill-slot="main">
      <tal:main-macro metal:define-macro="main">

        <div tal:replace="structure context/render"/>

      </tal:main-macro>
    </metal:main>

and finally, the edit in your MyContentType.xml type registration:

  <alias from="edit" to="@@my_edit"/>


This should get you somewhere...
