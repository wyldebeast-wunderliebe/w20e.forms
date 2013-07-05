# -*- coding: utf-8 -*-
from w20e.forms.xml.factory import XMLFormFactory
from w20e.forms.utils import find_file
import datetime


class TestBaseModel(object):

    def setup_class(self):
        xml = find_file('test_xml_form.xml', __file__)
        self.form = XMLFormFactory(xml).create_form()

    def teardown_class(self):
        pass

    def test_validation(self):

        data = {
           'name':'piëbe',
           'text':'<html>hi</html>',
           'w20e.forms.process':1
        }

        # test string type validation
        status, errors = self.form.view.handle_form(self.form, data)
        assert status == 'completed'
        assert len(errors) == 0

        # test if unicode validates as stringtype
        data['name'] = u'åbçḑȩ'
        status, errors = self.form.view.handle_form(self.form, data)
        assert status == 'completed'
        assert len(errors) == 0

        # test to see if datestring will be validated
        data['date'] = '31-12-2013'
        status, errors = self.form.view.handle_form(self.form, data)
        assert status == 'completed'
        assert len(errors) == 0

        # test to see if datetime will be validated
        data['date'] = datetime.datetime.now()
        status, errors = self.form.view.handle_form(self.form, data)
        assert status == 'completed'
        assert len(errors) == 0

        # test to see if an integer won't validate as date
        data['date'] = 666
        status, errors = self.form.view.handle_form(self.form, data)
        assert status == 'error'
        assert 'date' in errors
        assert 'datatype' in errors['date']

