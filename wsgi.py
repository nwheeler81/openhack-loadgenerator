import random
import os
import json
import math
import sys
import requests
from flask import Flask

application = Flask(__name__)

url = os.environ.get('WS_URL')
recs = int(os.environ.get('RECS'))
type_load = os.environ.get('TYPE_LOAD')
words = [word.strip() for word in open('words').readlines()]

print url, type_load

@application.route("/")
def main(): 
    for identifier in range(1, recs + 1):
        store_id = math.trunc(random.uniform(0,100))
        if type_load == "raitings":
            raiting = math.trunc(random.uniform(0, 5))
            price = random.uniform(0,1000)
            content = {
            "product_name": random.choice(words),
            "raiting_by_user": raiting,
            "price": "%.2f" % price, 
            "store_id": store_id
        }
        elif type_load == "receipts":
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
    return "Sent: %s requests" % recs

if __name__ == "__main__":
    application.run(port=5000)
