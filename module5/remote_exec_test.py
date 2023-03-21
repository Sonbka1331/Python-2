import unittest
from remote_execution_app import app


class ExecTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.url = "/remote_execution"
        self.data = dict()

    def test_successful_code(self):
        self.data['code'] = "print('Hello')"
        self.data['timeout'] = 2
        response_text = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('success', response_text)

    def test_error_input_code(self):
        self.data['code'] = 123
        self.data['timeout'] = 'str'
        response_text = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Not a valid integer value.', response_text)

    def test_trying_to_shell_true(self):
        self.data['code'] = 'shell=True'
        self.data['timeout'] = 5
        response_text = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn('Not allowed', response_text)

    def test_try_to_send_no_data(self):
        response_text = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn("Invalid input, {'code': ['This field is required.'], 'timeout': ['This field is required.']}",
                      response_text)

    def test_timeout_expired(self):
        self.data['code'] = '''import time;time.sleep(5)'''
        self.data['timeout'] = 1
        response_text = self.app.post(self.url, data=self.data).data.decode()
        self.assertIn("Timeout ends", response_text)


if __name__ == '__main__':
    unittest.main()
