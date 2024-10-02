import unittest
from rest_framework.test import APITestCase

class AppTemplateAPITest(APITestCase):
    def test_list_templates(self):
        response = self.client.get('/api/app-templates/')
        self.assertEqual(response.status_code, 200)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
