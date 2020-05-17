# encoding: utf-8
# file name : check_files_are_sorted.py 
# descrpition : This python code checks if the following files are sorted 
#               1) customer.txt
#               2) invoice.txt
#               3) item.txt
#  Author : Ophir Sweiry
#  Date : 4/2/2020
#  Version : 2.0.1

import sys
import os
import csv
import logging
import time

val_lambda_customer_key = (lambda x: int(x[5:]) if x[5:].isdigit() else 0)
val_lambda_invoice_key = (lambda x: int(x[3:]) if x[3:].isdigit() else 0)
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in


## function to check if file are sorted, if not it prints the record
##
def check_sorted (file_name,get_key_lambda):
    with open(os.path.join(script_dir, file_name), mode='r',encoding='utf-8') as f:
        prev_customer_key = -1
        index = 0 
        for line in f:
            index = index +1
            line=line.replace('“','"').replace('”','"')
            line = next(csv.reader( [ line ] ))
            customer_key =get_key_lambda(line[0])
            if customer_key < prev_customer_key:
                print (file_name+ " not sorted  ID :{} Row Number {} ".format(customer_key,index))
            prev_customer_key = customer_key

check_sorted('./customer.txt',val_lambda_customer_key)
check_sorted('./invoice.txt',val_lambda_invoice_key)
check_sorted('./item.txt',val_lambda_invoice_key)
