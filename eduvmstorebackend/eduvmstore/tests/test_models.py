import unittest

from eduvmstore.db.models import AppTemplate
from eduvmstore.db import SessionLocal

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


class AppTemplateTest(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()
        self.template = AppTemplate(name='Test Template', description='A test', image='test.png')
        self.db.add(self.template)
        self.db.commit()

    def test_template_creation(self):
        template = self.db.query(AppTemplate).filter_by(name='Test Template').first()
        self.assertEqual(template.description, 'A test')


if __name__ == '__main__':
    unittest.main()
