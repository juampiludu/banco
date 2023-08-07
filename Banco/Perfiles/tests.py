from django.test import TestCase
from django.contrib.auth import get_user_model
from Perfiles.form import RegistroForm

class RegistroFormTest(TestCase):
    def test_form_submission(self):
        form_data = {
            'email': 'juanzakka@gmail.com',
            'first_name': 'Juan',
            'last_name': 'Ludueña',
            'born_date': '08-12-2001',
            'phone': '123456',
            'dni': '222',
            'province': 'cb',
            'localidad': 'Mendiolaza',
            'address': 'Norte 61',
            'password1': 'juanjuan1',
            'password2': 'juanjuan1'
        }
        form = RegistroForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsInstance(user, get_user_model())