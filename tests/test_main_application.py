import unittest
from unittest.mock import patch
from dummy_project import main


class TestMainApp(unittest.TestCase):
    def setUp(self):
        self.my_app = main.MainApp()

    def test_name(self):
        self.assertEqual(self.my_app.name, "My Application")

if __name__ == '__main__':
    unittest.main()
