import unittest
import os
from unittest.mock import patch


def myfunction():
    return "no mock"


class DemoTest(unittest.TestCase):
    def test_b(self):
        with open("aa.txt", "w") as fp:
            fp.write("data")

    @patch("__main__.myfunction")
    def test_c(self, mock_function):
        mock_function.return_value = "mock"
        response = myfunction()
        print(response)

    def test_d(self):
        with open("aa.txt", "r") as fp:
            print(fp.read())

    def test_a(self):
        print("a")

    @classmethod
    def tearDownClass(cls):
        os.remove("aa.txt")


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(DemoTest("test_b"))
    test_suite.addTest(DemoTest("test_d"))
    test_suite.addTest(DemoTest("test_c"))
    test_suite.addTest(DemoTest("test_a"))
    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite())