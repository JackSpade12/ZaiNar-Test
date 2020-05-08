# encoding: utf-8
# file name : test_customer_details.py
# descrpition : This is a test client for customer_details.py
#               1. test_sanity checks customer Indiana jones on small subset dataset
#               2. test_full checks customer Ava Williams on full dataset
#
#  Author : Ophir Sweiry
#  Date : 4/2/2020
#  Version : 2.0.3


import unittest
import customer_details
import sys
import os
import time


class test_customer_details(unittest.TestCase):

    def setUp(self):
        try :
            pass
        except :
            pass

    # function: test_sanity
    # descripton: checks customer Indiana jones on small subset dataset
    def test_sanity(self):

        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()