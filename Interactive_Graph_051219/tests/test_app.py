import json
import unittest
# from flask.ext.testing import TestCase
from flask_testing import TestCase

import sys
sys.path.insert(0, '/home/hackerman/Documents/Alan-Git-Repositories/Software-Development-Project/Interactive_Graph')

import app

# set our application to testing mode
app.testing = True


class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def test_upload(self):
        self.app.get('/upload')
        self.assert_template_used('SDP_visualize.html')
        # self.assert_context("greeting", "hello")