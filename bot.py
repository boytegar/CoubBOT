import base64
import json
import os
import random
import time
from urllib.parse import parse_qs, unquote
import requests
from datetime import datetime

from coub import Coub

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {word}")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_query():
    try:
        with open('coub_query.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File coub_query.txt not found.")
        return [  ]
    except Exception as e:
        print("Failed get Query :", str(e))
        return [  ]

def load_task():
     data = json.loads(open("task.json").read())
    #  task = data.strip().split('\n')
     return data

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def main():

    while True:
        coub = Coub()
        queries = load_query()
        tasks = load_task()
        sum = len(queries)
        delay = int(24 * random.randint(3600, 3650))
        # generate_token()
        start_time = time.time()
        for index, query in enumerate(queries, start=1):
            list_id = []
            user = parse_query(query).get('user')
            username = user.get('username','')
            print_(f"====== Account {index}/{sum} | {username} ======")
            token = coub.login(query)
            data_reward = coub.get_rewards(token=token)
            for data in data_reward:
                id = data.get('id',0)
                list_id.append(id)
            for task in tasks:
                id = task.get('id')
                if id in list_id:
                    print_(f"{task.get('title')} Done...")
                else:
                    time.sleep(2)
                    print_(f"{task.get('title')} Starting task...")
                    coub.claim_task(token, task.get('id'), task.get('title'))
            
        end_time = time.time()
        total = delay - (end_time-start_time)
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        print_(f"[ Restarting In {int(hours)} Hours {int(minutes)} Minutes {int(seconds)} Seconds ]")
        if total > 0:
            time.sleep(total)


if __name__ == "__main__":
     main()

