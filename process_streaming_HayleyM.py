"""

Streaming Process: Uses port 9999

Create a fake stream of data. 
Use temperature data from the batch process.

Reverse the order of the rows to read OLDEST data first.

Important! 

We'll stream forever - or until we read the end of the file. 
Use use Ctrl-C to stop. (Hit Control key and c key at the same time.)

Explore more at 
https://wiki.python.org/moin/UdpCommunication

"""

# Import from Python Standard Library

import csv
import socket
import time
import random

# Set up basic configuration for logging

# Define all key items
HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
INPUT_FILE_NAME = "Hourly_Gasoline_Prices.csv"
OUTPUT_FILE_NAME = "out9.txt"

# Define function to create message from f string from the csv rows
def prepare_message_from_row(row):
    return f"{','.join(row)}\n".encode()

# Define function to stream data from input file, ie csv file using socket
# Use time sleep from time import and random for random import to sleep between 1 or 3 seconds
def stream_data(input_file_name, output_file_name, address_tuple):
    with open(input_file_name, "r") as input_file, open(output_file_name, "w") as output_file:
        reader = csv.reader(input_file)
        header = next(reader)
        output_file.write(','.join(header) + '\n')

        sock_object = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for row in reader:
            message = prepare_message_from_row(row)
            sock_object.sendto(message, address_tuple)
            output_file.write(','.join(row) + '\n')
            time.sleep(random.uniform(1, 3))  

if __name__ == "__main__":
    try:
        print("Starting data streaming.")
        stream_data(INPUT_FILE_NAME, OUTPUT_FILE_NAME, ADDRESS_TUPLE)
        print("Streaming complete!")
    except Exception as e:
        print(f"An error occurred: {e}")