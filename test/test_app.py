import sys
sys.path.append("../")
# sys.path.insert(1, "./Rosbag-Analyser/src/app")
# import myapp
# from ..src.app import myapp
from src.app import myapp
from src.utils import bag_content, bag_info, color_gen, convert_time
import json
import unittest
import pandas as pd
import rosbag
import ast
from flask import template_rendered
from contextlib import contextmanager

import urllib
import blinker

# set our application to testing mode
print("STARTING TESTING MODULE...")
print("--------------------------")
print("Imported modules correctly...")
myapp.testing = True


class TestApp(unittest.TestCase):
    """
    This class uses unittest module.
    Performs unit tests for the functionality in app.py.
    Run tests on terminal: python3 test_app.py
    """

    @classmethod
    def setUpClass(cls):
        pass

    # app methods
    def setUp(self):
        # creates a test client
        self.app = myapp.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_home_status_code(self):
        # sends HTTP GET request to the application on the specified path
        result = self.app.get('/')
        
        print(result.status_code)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        # pass
    
    def test_upload_template(self):
        
        @contextmanager
        def captured_templates(app):
            recorded = []
            def record(sender, template, context, **extra):
                recorded.append((template, context))
            template_rendered.connect(record, app)
            try:
                yield recorded
            finally:
                template_rendered.disconnect(record, app)
        
        rv = self.app.get("/upload")
        assert(rv.status_code == 200)
        self.assertIn("Rosbag Analyzer".encode(), rv.data)

        templates = captured_templates(self.app)
        print(templates)
        
        # with self.captured_templates(self.app) as templates:
            # rv = self.app.test_client().get('/upload')
            # print(templates)
            # assert rv.status_code == 200
            # assert len(templates) == 1
            # template, context = templates[0]
            # assert template.name == 'index.html'
            # assert len(context['items']) == 10

    def test_live_template(self):
        rv = self.app.get("/live")
        assert(rv.status_code == 200)
        self.assertIn("Ros Live Visualizer".encode(), rv.data)

    def test_bag_info(self):
        try:
            bag = rosbag.Bag("../data/move_base_WS02_to_WS03.bag")
        except IOError:
            print("Could not find bag file")
        
        df = bag_info(bag)
        df_baseline = pd.DataFrame(columns = ['Color', 'Message', 'Count', 'Connections', 'Frequency'])
        # pd.testing.assert_frame_equal(df, df_baseline)
        self.assertEqual(len(df.columns.intersection(df_baseline.columns)), 5)
    
    def test_bag_content(self):
        """
        To test that bag_content in utils is returning a json with the desired keys
        """
        expected_dict = {"Time":[], "Topic":[], "Message":[], "Color":[]}
        # expected_dict_json = json.dumps(expected_dict)
        
        try:
            bag = rosbag.Bag("../data/move_base_WS02_to_WS03.bag")
        except IOError:
            print("Can not open bag file")
        
        df = bag_info(bag)
        jsonfile = bag_content(bag, df) # this returns a string representation of a dictionary, hence the conversion
        jsonfile = json.loads(jsonfile)
        jsonfile_compare = jsonfile[0]

        K2 = jsonfile_compare.keys() == expected_dict.keys()

        self.assertEqual(K2, True)

    def test_color_gen(self):
        """
        To test lenght of returned array that contains the color information of topics in timeline
        """
        color_array = color_gen(10)
        self.assertEqual(len(color_array), 10)
    
    def test_flask_application_is_up_and_running(self):
        # response = urllib.urlopen(self.get_server_url())
        # response = urllib.request.urlopen(self.get_server_url())
        # self.assertEqual(response.code, 200)
        pass

if __name__ == "__main__":
    unittest.main()