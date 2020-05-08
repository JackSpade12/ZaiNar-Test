# encoding: utf-8
# file name : test_customer_details.py
# descrpition : This is a test client for customer_details.py
#               1. test_sanity checks customer Indiana jones on small subset dataset
#               2. test_full checks customer Ava Williams on full dataset
#
#  Author : Ophir Sweiry
#  Date : 4/2/2020
#  Version : 2.0.1


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
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        start_time = time.time()
        _customer_details = customer_details.customer_details([None,"Indiana","Jones"])  
        _customer_details.customer_file_folder = os.path.join(script_dir, 'test_data/customer.txt')
        _customer_details.invoice_file_fodler = os.path.join(script_dir, 'test_data/invoice.txt')
        _customer_details.item_file_folder = os.path.join(script_dir, 'test_data/item.txt')  
        counter_customers, counter_invoices, counter_items, total_amounts =  _customer_details.main()

        self.assertTrue(time.time()- start_time < 4)
        self.assertEqual(counter_customers,1)
        self.assertEqual(counter_invoices,2)
        self.assertEqual(counter_items,18)
        self.assertEqual(total_amounts,1090)


    # function: test_sanity
    # descripton: checks customer Indiana jones on small subset dataset
    def test_full(self):
        start_time = time.time()
        _customer_details = customer_details.customer_details([None,"Indiana","Jones"])    
        counter_customers, counter_invoices, counter_items, total_amounts =  _customer_details.main()
        self.assertTrue(time.time()- start_time < 90)
        self.assertEqual(counter_customers,1)
        self.assertEqual(counter_invoices,2)
        self.assertEqual(counter_items,18)
        self.assertEqual(total_amounts,1090)

if __name__ == '__main__':
    unittest.main()