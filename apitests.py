import unittest
import api

class apitest(unittest.TestCase):
    def setUp(self):
        self.runner = api.app.test_client()
    def test_getstats(self):
        response=self.runner.get('/getstats')
        print response.data

if __name__ == "__main__":
    unittest.main()
