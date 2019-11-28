from app import myapp
import json
# from flask_testing import TestCase
# from Interactive_Graph import app
import unittest

# set our application to testing mode
print("Imported modules correctly...")
myapp.testing = True

# TODO:
# testing render_template
# testing return json
# user management: login/logout functionality

class TestMyApp(unittest.TestCase):
    """
    This class uses unittest module.
    Performs unit tests for the functionality in app.py.
    Run tests on terminal: python -m unittest test_app.
    """

    def setUp(self):
        self.app = myapp.test_client()

    def test_index(self):
        # self.app.get('/')
        rv = self.app.get('/')
        # print(rv.data)
        self.assertIn("index", rv.data)
        # self.assert_template_used("index.html")

    def test_upload(self):
        self.app.get('/upload')
        self.assert_template_used("SDP_visualize.html")
        # print("assert template passed!")
        # self.assert_context("greeting", "hello")

    # def test_404(self):
        # rv = self.app.get('/other')
        # self.assertEqual(rv.status, '404 NOT FOUND')


if __name__ == "__main__":
    unittest.main()