import chardet
from chardet.universaldetector import UniversalDetector
from unittest import TestCase


class SampleTest(TestCase):
    def test_detect_char(self):
        test_cases = ["a", "中文", ",", "；"]
        for test_case in test_cases:
            detect_info = chardet.detect(test_case.encode())
            print(detect_info)

    def test_feed_char(self):
        test_cases = ["a", "中文", ",", "；"]
        detector = UniversalDetector()
        for test_case in test_cases:
            detector.feed(test_case.encode())
            if detector.done:
                break
        detector.close()
        print(detector.result)


