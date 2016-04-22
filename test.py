import os
import unittest
import croneJob

class test(unittest.TestCase):
    def changeDate(self,dateString):
        command = 'sudo date "'+dateString+'"'
        print command
        os.system(command)

    def setUp(self):
        self.am9 = "04220900.00"
        self.pm1 = "04221300.00"
        self.pm5 = "04221700.00"
        self.pm9 = "04222100.00"

    def test_at9(self):
        print "9 am"
        self.changeDate(self.am9)
        # croneJob.stop()

    def test_at13(self):
        print "13 pm"
        self.changeDate(self.pm1)
        # croneJob.stop()

    def test_at17(self):
        print "05 pm"
        self.changeDate(self.pm5)
        # croneJob.stop()

    def test_at21(self):
        print "09 pm"
        self.changeDate(self.pm9)
        # croneJob.stop()

if __name__ == "__main__":
    unittest.main()
