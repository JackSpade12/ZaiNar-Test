# encoding: utf-8
# file name : customer_details.py
# descrpition : This python code retrieves all cusomter purchased item and total purchased items 
#               based on matching customer name 
#               from the following data files:
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


class customer_details: 
    # Global parametes  
    ###################
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    customer_file_folder = os.path.join(script_dir, './customer.txt')
    invoice_file_folder = os.path.join(script_dir, './invoice.txt') 
    item_file_folder = os.path.join(script_dir, './item.txt')
    log_file_name = os.path.join(script_dir,'./customer_details.log')
    invoice_file = None
    item_file = None
    file_read_mode = 'r'
    UTF_encoding = 'utf-8'
    customer_fullname_format = "{}||{}"
    prev_invoice = ""
    prev_item = ""
    customer_first_name = ""
    customer_last_name = ""

    # Execution counters 
    ######################
    counter_customers = 0
    counter_invoices = 0
    counter_items = 0
    total_amounts = 0

    # Logger
    ##################
    FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=log_file_name,filemode='w',level=logging.DEBUG,format=FORMAT)

    # Printing functions
    #####################
    def print_customer(self,customer_id,customer_fname, customer_lname):
        print ("============================")
        print ("Customer ID: {}, Customer name : {} {}".format(customer_id,customer_fname,customer_lname))
        print ("--------")
        print ("INVOICE_ID,ITEM_ID,AMOUNT,QUANTITY")

    def print_execution_results (self,ts,counter_customers,counter_invoices,counter_items,total_amounts):
        print ("============================")
        print ("=== Execution Parameters ===")
        print ("Execution time - {0:.2f} seconds".format(time.time() - ts))
        print ("Number of customers: {}".format(counter_customers))
        print ("Number of invoices: {}".format(counter_invoices))
        print ("Number of items: {}".format(counter_items))
        print ("Total Amount across all customers: {}".format(total_amounts))

    def print_total_customer_purchase (self,total_customer_purchase):
        # Print total amount purchased for customer
        print ("Total customer pucrhases ${0:.2f}".format(total_customer_purchase))

    # Logic
    #####################

    # function name: val_lambda_customer_key
    # description: Retive the customer ID as an int e.g. "CUST00499999" -> 499999
    def val_lambda_customer_key (self,x): 
        x = int(x[5:]) if x[5:].isdigit() else 0
        return x

    # function name: val_lambda_invoice_key
    # description: retive the invoice ID as an int e.g. "IN00499999" -> 499999
    def val_lambda_invoice_key (self,x): 
        x = int(x[3:]) if x[3:].isdigit() else 0
        return x


    # function name: clean_up_row
    # description: Takes a line from the file and transforms it to a string list
    #
    def clean_up_row(self,data_row):
        data_row=data_row.replace('“','"').replace('”','"')
        return next(csv.reader( [ data_row ] ))


    # function name: customer_name_key
    # description: create a customer key from the user first name and last name  -> "first name||last name"
    def customer_name_key(self,customer_row):
        customer_row = self.clean_up_row(customer_row)
        return self.customer_fullname_format.format(customer_row[1],customer_row[2])


    # function name: read_customers
    # description: Iterate on the customer file to get all customers that match first name and last name
    #
    def read_customers(self,first_name,last_name):
        # created a key from first name and last name  ->  "fname||lname"
        customer_fullname_key = self.customer_fullname_format.format(first_name,last_name)
        # search for customer 
        with open(self.customer_file_folder, mode=self.file_read_mode,encoding=self.UTF_encoding) as customers:
            return filter(lambda x: self.customer_name_key(x) == customer_fullname_key, list(customers))

    # function name: main
    # description Main function to control the logic
    # 1. Print all customers, Invoices, and Items for provided args [0] first name and arg [1] family name
    # 2. Aggregate total purchased amount of a customer
    # 3. Report on execution counters.
    #
    def customer_worker (self,customer):
        total_customer_purchase = 0.0
        self.counter_customers +=1

        #get the customer integer ID
        customer_id = customer[0]
        customer_id = self.val_lambda_customer_key(customer_id)

        #print customer
        self.print_customer(customer_id,customer[1],customer[2])

        # check previous run latest invoice record if exists
        if self.prev_invoice != "" :
            invoice_customer_id = self.invoice_get_customer_id (self.prev_invoice)
            if (invoice_customer_id == customer_id) :
                invoice_amount = self.invoice_worker(self.prev_invoice)
                total_customer_purchase += invoice_amount 

        # iterate on invoices 
        for invoice in self.invoices_file:
            invoice = self.clean_up_row(invoice)
            self.prev_invoice = invoice
            invoice_customer_id = self.invoice_get_customer_id (invoice)
            # escape invoices iterator if no more invoices for this customer ID since invoices are sorted by customer ID
            if (invoice_customer_id > customer_id) :
                break

            # if there is a match process items
            if (invoice_customer_id == customer_id) :
                invoice_amount = self.invoice_worker(invoice)
                total_customer_purchase += invoice_amount
        
        # print total amounts for a customer
        self.print_total_customer_purchase (total_customer_purchase)
        self.total_amounts+= total_customer_purchase 

    # function: invoice_get_customer_id
    # desciption: Get the cusotmer ID of and invoice
    #
    def invoice_get_customer_id (self,invoice):
        # read invoice
        line_customer_id=self.val_lambda_customer_key(invoice[0])
        return line_customer_id 

    # function name: invoice_worker
    # description: Atomic worker to process a customer record
    # 1. Find the matching items for the invoice by iterating on the item file 
    # 2. When a match is found, send the matched item to the atomic invoice worker for further processing
    # 3, Stop when it reaches an item that the item invoice ID is bigger than the invoice ID
    # 4. Store the last fetched item from the file so it won't be skipped in the next iteration
    #
    def invoice_worker (self,invoice):
        invoice_id=self.val_lambda_invoice_key(invoice[1])
        # set counters
        total_invoice_items_amount = 0 
        self.counter_invoices += 1
        

        # check previous run latest item record if exists
        if self.prev_item != "" :
            item_invoice_id = self.item_get_invoice_id (self.prev_item)
            if item_invoice_id == invoice_id:
                total_invoice_items_amount+= self.item_worker(self.prev_item)

        # iterate on items from item file  
        for item in self.items_file:
            item = self.clean_up_row(item)
            self.prev_item = item
            item_invoice_id = self.item_get_invoice_id (item)

             # escape item iterator if no more items for this invoice
            if item_invoice_id > invoice_id:
                break
            elif item_invoice_id == invoice_id:
                total_invoice_items_amount+= self.item_worker(item)

        #return item amount
        return total_invoice_items_amount

    # function: item_get_invoice_id
    # desciption: Get the invoice ID of an item
    #
    def item_get_invoice_id (self,item):
        # read item
        line_invoice_id = self.val_lambda_invoice_key(item[0])
        return line_invoice_id

    # function name: item_worker
    # description: Atomic worker to process an item
    # simply prints the item and returns its amount
    #
    def item_worker (self,item):
        self.counter_items += 1

        # print items
        print(item)

        #extract the amount
        item_amount = float(item[2])
        return item_amount

    
    # function name: main
    # description Main function to control the logic
    # 1. Print all customers, Invoices and Items for provided args [0] first name and arg [1] family name
    # 2. Agregate total purchased amount of a customer
    # 3. Report on execution counters.
    #
    def main(self):
        logging.info('App Started')

        # set executino indicators 
        start_time = time.time()
        
        try: 
            self.invoices_file = open(self.invoice_file_folder, mode=self.file_read_mode,encoding=self.UTF_encoding)
            self.items_file = open(self.item_file_folder, mode=self.file_read_mode,encoding=self.UTF_encoding)
            
            # iterate on customers 
            for customer in self.read_customers(self.customer_first_name ,self.customer_last_name):
                customer = self.clean_up_row(customer) 
                self.customer_worker(customer)
        except:
            exit ("failed with error {}".format(sys.exc_info()[0]))

        finally:
            try:
                #try to properly close the files
                self.invoices_file.close()
                self.items_file.close()
            except:
                pass

        # if no customer was found exit with failure message
        if (self.counter_customers == 0):
            exit ("{} {} is not a customer".format(self.customer_first_name ,self.customer_last_name))

        # print execution results   
        self.print_execution_results (start_time,self.counter_customers,self.counter_invoices,self.counter_items,self.total_amounts)
        logging.info('App Finished')
        return  self.counter_customers, self.counter_invoices, self.counter_items, self.total_amounts
    
    def __init__ (self,args):
        if len(args) < 3:
            exit("You need to provide the first and last name of a customer as arguments")
        self.customer_first_name = args[1]
        self.customer_last_name = args[2]


if __name__ == '__main__':
        if len(sys.argv) < 3:
            exit("You need to provide the first and last name of a customer as arguments")
        _customer_details = customer_details(sys.argv)    
        _customer_details.main()