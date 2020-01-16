from app import myapp
from utils import *
import json
import unittest
import pandas as pd
import rosbag
import ast

# set our application to testing mode
print("STARTING TESTING MODULE...")
print("--------------------------")
print("Imported modules correctly...")
myapp.testing = True


class TestApp(unittest.TestCase):
    """
    This class uses unittest module.
    Performs unit tests for the functionality in app.py.
    Run tests on terminal: python -m unittest test_app.
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
        # result = self.app.get('/')
        # assert the status code of the response
        # self.assertEqual(result.status_code, 200)
        pass

    def test_upload_template(self):
        # result = self.app.get('/upload')
        # self.assertEqual(result ,"SDP_visualize.html")
        pass 

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

        # compare json keys and check they are the same
        # def compare_keys(json1, json2):
            # return json1.keys() == json2.keys()
        
        K2 = jsonfile_compare.keys() == expected_dict.keys()

        self.assertEqual(K2, True)

    def test_color_gen(self):
        """
        To test lenght of returned array that contains the color information of topics in timeline
        """
        color_array = color_gen(10)
        self.assertEqual(len(color_array), 10)


if __name__ == "__main__":
    unittest.main()