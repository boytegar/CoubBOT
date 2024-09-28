import base64
import json
import os
import time
from urllib.parse import parse_qs, unquote
import requests
from datetime import datetime


def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {word}")

def make_request(method, url, headers, json=None, params=None, data=None):
    retry_count = 0
    while True:
        time.sleep(2)
        if method.upper() == "GET":
            if params:
                response = requests.get(url, headers=headers, params=params)
            elif json:
                response = requests.get(url, headers=headers, json=json)
            else:
                response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            if json:
                response = requests.post(url, headers=headers, json=json)
            elif data:
                response = requests.post(url, headers=headers, data=data)
            else:
                response = requests.post(url, headers=headers)
        elif method.upper() == "PUT":
            if json:
                response = requests.put(url, headers=headers, json=json)
            elif data:
                response = requests.put(url, headers=headers, data=data)
            else:
                response = requests.put(url, headers=headers)
        else:
            raise ValueError("Invalid method. Only GET, PUT and POST are supported.")
        if response.status_code >= 500:
            if retry_count >= 4:
                print_(f"Status Code : {response.status_code} | Server Down/Something")
                return None
            retry_count += 1
        elif response.status_code >= 400:
            print_(f"Status Code : {response.status_code} | Failed to get Coin")
            return None
        elif response.status_code >= 200:
            return response.json()

class Coub:
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://coub.com",
            "Referer": "https://coub.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }


    
    def login(self, query):
        header = self.headers
        url = 'https://coub.com/api/v2/sessions/login_mini_app'
        
        response = make_request('post', url, header, data=query)
        if response is not None:
            print_("Getting Token")
            api_token = response.get('api_token',"")
            token = self.get_token(api_token=api_token)
            if token is not None:
                return token
        return None

    def get_token(self, api_token):
        header = self.headers
        header['x-auth-token'] = api_token
        url = 'https://coub.com/api/v2/torus/token'
        response = make_request('post', url, header)
        if response is not None:
            access_token = response.get('access_token','')
            expires_in = response.get('expires_in','')
            print_(f"Token Created, Expired in {round(expires_in/3600)} Hours")
            return access_token
        return None
        

    def get_rewards(self, token):
        headers = self.headers
        headers["authorization"] = f"Bearer {token}"
        url = "https://rewards.coub.com/api/v2/get_user_rewards"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json() 
        else:
            print(response.text)
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
    
    def encode_to_base64(input_string):
        # Encode the input string to bytes
        input_bytes = input_string.encode('utf-8')
        
        # Encode the bytes to base64
        base64_bytes = base64.b64encode(input_bytes)
        
        # Convert the base64 bytes back to string
        base64_string = base64_bytes.decode('utf-8')
        print(base64_string)
        
        return base64_string
