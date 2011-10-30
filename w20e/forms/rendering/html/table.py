from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


CELL_TPL = """<td><input id="input-%(id)s-%(row)s-%(col)s" type="text" name="%(id)s_%(row)s_%(col)s" value="%(value)s"/></td>"""



class TableRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Table to HTML """

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        value = form.getFieldValue(renderable.bind)
            
        print >> out, TEMPLATES['CONTROL_HDR'] % fmtmap
    
        print >> out, "<table><thead>"

        for col in renderable.col_headers.split(","):
            print >> out, "<th>%s</th>" % col

        print >> out, "</thead><tbody>"

        for row in range(int(renderable.rows)):

            print >> out, "<tr>"

            for col in range(int(renderable.cols)):
                
                cell_value = ''

                try:
                    cell_value = value.get((row, col), '')
                except:
                    pass

                print >> out, CELL_TPL % {'id': renderable.id,
                                  'col': col,
                                  'row': row,
                                  'value': cell_value
                                  }

            print >> out, "</tr>"

        print >> out, "</tbody></table>"
                   
        print >> out, TEMPLATES['CONTROL_FTR']
