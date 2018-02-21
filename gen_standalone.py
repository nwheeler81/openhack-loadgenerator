import random
import os
import json
import math
import sys
import argparse
import requests
from multiprocessing import Process, Lock
import threading

parser= argparse.ArgumentParser(description='Generate load and post it to http-service')
parser.add_argument('--limit','-l',type=int, help='how many raitings shoud be generated')
parser.add_argument('--url','-u',help='URL')
parser.add_argument('--type','-t',help='Type of load, raitings or receipts')
parser.add_argument('--debug','-d', help='Debuging mode')
parser.add_argument('--pool','-p',type=int, help='Set the size of pool for basic parallelism')
args = parser.parse_args()
url = args.url
count = args.limit
words = [word.strip() for word in open('/usr/share/dict/words').readlines()]

print "Parameters:"
print " Rows:", args.limit
print " Service:", args.url
print " Type of load:",args.type
print " Pool size:", args.pool 
print " Total rows:", args.pool*args.limit 

debug = args.debug
print debug

def main(): 
    print "*"*10,"Start","*"*10
    for identifier in range(1, count + 1):
        store_id = math.trunc(random.uniform(0,100))
        if args.type == "raitings":
            raiting = math.trunc(random.uniform(0, 5))
            price = random.uniform(0,1000)
            content = {
            "product_name": random.choice(words),
            "raiting_by_user": raiting,
            "price": "%.2f" % price, 
            "store_id": store_id
        }
        elif args.type == "receipts":
            amount = random.uniform(1.0, 1000.0)
            content = {
            "topic": random.choice(words),
            "value": "%.2f" % amount,
            "store_id": store_id
        }
        else:
            print "Bad parameters"
            break
        req = requests.post(url, json=content)
        if debug=="True":
            print req.status_code, ' content ', req.json()

    print "*"*10,"Done","*"*10

if __name__ == "__main__":
    for i in range(args.pool):
        Process(target=main).start()
