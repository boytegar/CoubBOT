import json
import os
import time
from urllib.parse import parse_qs, unquote
import requests
from datetime import datetime


def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {word}")

class Coub:
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://coub.com/tg-app/",
            "Origin": "https://coub.com",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
        }

    def make_request(self, method, url, header, data=None):
        retry_count = 0
        while True:
            time.sleep(2)
            if method.upper() == "GET":
                response = requests.get(url, headers=header, params=data)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=header)
            else:
                raise ValueError("Invalid method. Only GET and POST are supported.")
            if response.status_code >= 500:
                if retry_count >= 3:
                    print_(f"Status Code : {response.status_code} | Server Down")
                    return None
                retry_count += 1
            elif response.status_code >= 400:
                print_(f"Status Code : {response.status_code}")
                break
            elif response.status_code >= 200:
                return response
    
    def get_rewards(self, token):
        headers = self.headers
        headers["authorization"] = f"Bearer {token}"
        url = "https://rewards.coub.com/api/v2/get_user_rewards"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json() 
        else:
            print_(f"Failed to retrieve user rewards. Status code: {response.status_code}")
            return None
    
    
    def claim_task(self, token, task_id, task_title):
        headers = self.headers
        headers["authorization"] = f"Bearer {token}"
        params = {"task_reward_id": task_id}
        url = "https://rewards.coub.com/api/v2/complete_task"
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            print_(f"ID {task_id} | Task  '{task_title}'  Done")
            return response.json()
        else:
            print_(f"ID {task_id} | Task  '{task_title}'  Failed to claim | error : {response.status_code}")
            return None