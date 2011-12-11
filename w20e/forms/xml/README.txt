XML
===

The xml namespace of the w20e.forms package provides an XML based
implementation of the w20e.forms API. This enables definition from
and serialization to XML files. Provided is the DTD used for defining
the w20e.forms as XML. This is quite similar to xForms.

Using XML as definition of forms provides a more declarative way of
creating forms, not unlike the way you create a form in HTML. Also, XML is a format that is easily stored and transported.


Start using the XML factory

      >>> from factory import XMLFormFactory

Now let us create a factory class

      >>> xml = """
      ... <form id="test">
      ...
      ...   <!-- The data part, a.k.a. the variables you wish to collect -->
      ...   <data>
      ...     <foo/>
      ...     <bar value="666"/>
      ...   </data>
      ...
      ...   <model>
      ...     <properties id="required">
      ...       <bind>foo</bind>
      ...	<bind>bar</bind>
      ...	<required>True</required>
      ...     </properties>
      ...     <properties id="int">
      ...       <bind>bar</bind>
      ...	<datatype>int</datatype>
      ...     </properties>
      ...   </model>
      ...
      ...   <view>
      ...     <input id="fooctl" bind="foo">
      ...       <label>Foo?</label>
      ...       <hint>Well, foo or no?</hint>
      ...     </input>
      ...     <select id="barctl" bind="bar">
      ...       <property name="multiple">False</property>
      ...       <label>Bar</label>
      ...       <option value="1">One</option>
      ...       <option value="2">Two</option>
      ...     </select>
      ...     <select bind="bar" id="barctl2">
      ...       <label>Bar2</label>
      ...       <option value="3">Three</option>
      ...       <option value="4">Four</option>
      ...     </select>
      ...     <select bind="bar" id="barctl3">
      ...       <property name="vocab">some_vocab</property>
      ...       <label>Bar3</label>
      ...     </select>
      ...     <group layout="flow" id="groupie">
      ...       <label>GruppoSportivo</label>
      ...       <text id="txt">Moi</text>
      ...     </group>
      ...   </view>
      ...
      ...   <submission type="none">
      ...     <property name="action">@@save</property>
      ...   </submission>
      ...
      ... </form>"""

      We are using a vocab in the xml, so register it...
      >>> from w20e.forms.registry import Registry
      ... def some_vocab():
      ...   return [Option(0, 0), Option(1, 1)]
      ... Registry.register_vocab('some_vocab', some_vocab)

      >>> xmlff = XMLFormFactory(xml)
      >>> form = xmlff.create_form()
      >>> print len(form.data.getFields())
      2

      >>> print form.data.getField("foo").id
      foo

      >>> print form.data.getField("bar").value
      666

      Set the value 

      >>> form.data.getField("bar").value = 777
      >>> print form.data.getField("bar").value
      777

      Okido, so far so good. Now let's see what properties we have.
      
      >>> props = form.model.getFieldProperties("bar")
      >>> len(props)
      2

      >>> intprop = [prop for prop in props if prop.id == "int"][0]
      >>> reqprop = [prop for prop in props if prop.id == "required"][0]
      >>> reqprop.getRequired()
      'True'
      
      >>> intprop.getDatatype()
      'int'

      Finally, check the viewable part, or the controls
      >>> ctrl = form.view.getRenderable("fooctl")
      >>> ctrl.label
      'Foo?'

      >>> ctrl.__class__.__name__
      'Input'

      >>> ctrl.hint
      'Well, foo or no?'

      >>> ctrl.id
      'fooctl'

      >>> ctrl.bind
      'foo'

      >>> ctrl = form.view.getRenderable("barctl")
      >>> ctrl.multiple
      'False'

      >>> len(ctrl.options)
      2

Do we get the nested stuff?
      >>> ctrl = form.view.getRenderable("txt")
      >>> ctrl.id
      'txt'


Serialization
-------------

You can easily serilialize the form back into XML. Let's try...

      >>> from serializer import XMLSerializer
      >>> serializer = XMLSerializer()
      >>> print serializer.serialize(form)
      <form id="test">
        <data>
          <foo/>
          <bar value="777"/>
        </data>
        <model>
          <properties id="int">
            <bind>bar</bind>
      	    <datatype>int</datatype>
          </properties>
          <properties id="required">
            <bind>foo</bind>
     	    <bind>bar</bind>
      	    <required>True</required>
          </properties>
        </model>
	<view>
      	  <input bind="foo" id="fooctl">
            <label>Foo?</label>
            <hint>Well, foo or no?</hint>
          </input>
          <select bind="bar" id="barctl">
            <label>Bar</label>
            <property name="multiple">False</property>
	    <option value="1">One</option>
	    <option value="2">Two</option>
          </select>
          <select bind="bar" id="barctl2">
            <label>Bar2</label>
	    <option value="3">Three</option>
	    <option value="4">Four</option>
          </select>
          <flowgroup id="groupie">
            <label>GruppoSportivo</label>
            <text id="txt"/>
          </flowgroup>
        </view>
        <submission type="none">
	  <property name="action">@@save</property>
	</submission>
      </form>
      <BLANKLINE>

Note that variable foo now holds the value 777. Sadly, it is hard to
guarantee that all XML will be exactely the same as the input XML.
