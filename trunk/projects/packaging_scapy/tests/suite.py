#!/usr/bin/python

import unittest
from scapy import *


class MyTestCase(unittest.TestCase):
    def test_getlayer(self):
        a = IP()/TCP()
        self.assertEquals(type(a.getlayer(TCP)), TCP)

if __name__ == "__main__":
    import testoob
    testoob.main()
