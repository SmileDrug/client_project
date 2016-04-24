import os
import unittest

class test(unittest.TestCase):
    def changeDate(self,dateString):
        command = 'sudo date "'+dateString+'"'
        print command
        os.system(command)

    def setUp(self):
        self.am9 = "04230900.00"
        self.pm1 = "04231300.00"
        self.pm5 = "04231700.00"
        self.pm9 = "04232100.00"

    def test_at9(self):
        print "9 am"
        self.changeDate(self.am9)
        os.system('python job.py')

    def test_at13(self):
        print "13 pm"
        self.changeDate(self.pm1)
        os.system('python job.py')

    def test_at17(self):
        print "05 pm"
        self.changeDate(self.pm5)
        os.system('python job.py')

    def test_at21(self):
        print "09 pm"
        self.changeDate(self.pm9)
        os.system('python job.py')

if __name__ == "__main__":
    unittest.main()
