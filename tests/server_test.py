import unittest
from app import app


class FlaskUnitTests(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_index_content_loads(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertTrue(b'Home' in response.data)

if __name__ == '__main__':
    unittest.main()
