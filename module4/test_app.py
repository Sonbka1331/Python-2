import unittest
from app import app


class TestView(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.url = "/registration"
        self.data = {
            'phone': '9876543210',
            'name': 'Test',
            'email': 'test@test.ru',
            'address': 'Address',
            'index': '112233',
            'comment': 'Comment'
        }

    def test_phone_field(self):
        response = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Successfully', response)

    def test_phone_field_with_error(self):
        self.data['phone'] = 'error_phone'
        response = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Successfully', response)

    def test_name_field(self):
        response = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Successfully', response)

    def test_name_field_with_error(self):
        self.data['name'] = 34404
        response = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Successfully', response)

    def test_email_field(self):
        response = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Successfully', response)

    def test_email_field_with_error(self):
        self.data['email'] = 'erroremailru'
        response = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Successfully', response)

    def test_address_field(self):
        response = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Successfully', response)

    def test_address_field_with_error(self):
        self.data['address'] = 34404
        response = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Successfully', response)

    def test_index_field(self):
        response = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Successfully', response)

    def test_index_field_with_error(self):
        self.data['index'] = 'error index'
        response = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Successfully', response)

    # comment cant raise error
