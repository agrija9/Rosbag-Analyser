from app import myapp
from utils import bag_content, bag_info
import json
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
import rosbag

# set our application to testing mode
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
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print("...passed test_home_status_code()")

    def test_upload_template(self):
        # result = self.app.get('/upload')
        # self.assertEqual(result ,"SDP_visualize.html")
        # print("assert template passed!")
        # self.assert_context("greeting", "hello")
        pass

    # util methods
    def test_bag_pandas_df(self):
        target_df = pd.DataFrame(columns = ['Topic', 'Color', 'Message', 'Count', 'Connections', 'Frequency'])
        bag = rosbag.Bag("./data/turtle_simulation.bag")
        obtained_df = bag_info(bag)
        # obtained_df = obtained_df.set_index("Topic") 
        assert_frame_equal(obtained_df, target_df, check_dtype=False)


if __name__ == "__main__":
    unittest.main()