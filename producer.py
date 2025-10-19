
# producer.py -- Transaction simulator (prints JSON events)
import json, random, time
from datetime import datetime
users = ['U1','U2','U3','U4','U5','U6','U7','U8']
merchants = ['Amazon','Flipkart','Uber','Swiggy','Zara','Myntra','BigBasket','Nykaa']
locations = ['Delhi','Mumbai','Kolkata','Chennai','Bangalore','Hyderabad']
def gen_txn():
    return {
        "txn_id": f"TXN{random.randint(100000,999999)}",
        "user_id": random.choice(users),
        "amount": round(random.uniform(10, 30000),2),
        "merchant": random.choice(merchants),
        "location": random.choice(locations),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
if __name__ == '__main__':
    try:
        while True:
            event = gen_txn()
            print(json.dumps(event))
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped")
