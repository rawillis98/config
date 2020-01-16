#!/usr/bin/env python3
import requests
from func_timeout import func_set_timeout
import random


class color:
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def get_url(id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
    return url

def get_item(id):
    url = get_url(id)
    item = requests.get(get_url(id)).json()
    return item

def get_new_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    ids = requests.get(url).json()
    return ids

@func_set_timeout(2)
def print_random_new_story():
    new_ids = get_new_stories()
    id = random.sample(new_ids, 1)[0]
    item = get_item(id)

    print(color.BOLD + item['title'] + color.END)
    print(f"Score: {item['score']}")
    if 'url' in item:
        print(item['url'])

try:
    print_random_new_story()
except Exception as e:
    print("Couldn't connect to hacker news.")


    
