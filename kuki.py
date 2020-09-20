import json
import random
import re
import sys
import string
import urllib.parse

import bs4
import requests
import os
import discord
from dotenv import load_dotenv

load_dotenv(dotenv_path = "token.env")
token = os.getenv("DISCORD_TOKEN")

client = discord.Client()

url = 'https://www.pandorabots.com/mitsuku/'
session = requests.Session()

@client.event
async def on_ready():
    print("Kuki has connected to Discord!")

@client.event
async def on_message(message):
        if not message.author == client.user:
            await message.channel.send(tell(message.content))

def new_client():
    client_name = 'kukilp-'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    return client_name

# def new_botkey():
#     main_page = session.get(url).text
#     main_soup = bs4.BeautifulSoup(main_page, 'lxml')
#     botkey = re.search(r'PB_BOTKEY: "(.*)"', main_page).groups()[0]
#     return botkey


def postit(botkey, query, client_name, sessionid):
    data = f'input={query}&botkey={botkey}&client_name={client_name}&sessionid={sessionid}&channel=6'
    return session.post('https://miapi.pandorabots.com/talk', data = data).text

client_name = new_client()
botkey = "n0M6dW2XZacnOgCWTp0FRYUuMjSfCkJGgobNpgPv9060_72eKnu3Yl-o1v2nFGtSXqfwJBG2Ros~"
sessionid = "null"

fail_count = 0

def tell(query):
    global botkey, sessionid, client_name, channel, fail_count

    if fail_count > 2:
        return "Sorry Error Occured"

    session.headers.update({
        'User-Agent': ' '.join(('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2)',
                                'AppleWebKit/537.36 (KHTML, like Gecko)',
                                'Chrome/72.0.3626.119 Safari/537.36')),
        'Referer': url,
        'Content-type': 'application/x-www-form-urlencoded'
    })

    tosend = re.sub(r'\s+', ' ', query).strip()
    tosend = urllib.parse.quote(tosend)
    print('Retrieving response.')

    try:
        response_raw = postit(botkey, tosend, client_name, sessionid)

    except Exception as e:
        print("Error", e)
        fail_count+=1
        return tell(query)

    response_json = json.loads(response_raw)
    sessionid = response_json.get('sessionid')
    response = list(re.sub(r'<.*?>', ' ', i) for i in response_json['responses'][0].split("\u200e"))
    response = '\n'.join(response)

    if len(response)==0:
        print("zero response")
        client_name = new_client()
        fail_count+=1
        return tell(query)

    fail_count = 0
    return response

client.run(token)
