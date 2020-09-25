import json
import random
import re
import sys
import string
import urllib.parse

import requests
import os
import discord
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

client = discord.Client()

@client.event
async def on_ready():
    print("Kuki has connected to Discord!")

@client.event
async def on_message(message):
    if str(message.channel)=='chat-with-kuki' and not (message.author == client.user  or str(message.author)=='k4u5h1k#8653'):
        response = tell(message.content)
        response = response.replace('Steve Worswick','Kaushik Sivashankar')
        await message.channel.send(response)


def new_client():
    try:
        driver.get("https://pandorabots.com/mitsuku/")

        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pb-widget__description__chat-now__button"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "pb-widget-input-field"))).send_keys("Hey"+Keys.ENTER)

        browser_log = str(driver.get_log('performance'))
        client_name = re.search(r'kukilp-.{10}',browser_log)[0]
        driver.quit()

    except:
        driver.quit()
        print("Could not forge client, making a random one instead")
        client_name = 'kukilp-'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

    return client_name

def postit(botkey, query, client_name, sessionid):
    data = f'input={query}&botkey={botkey}&client_name={client_name}&sessionid={sessionid}&channel=6'
    return session.post('https://miapi.pandorabots.com/talk', data = data).text


def tell_kuki(query):
    global botkey, sessionid, client_name, channel, fail_count

    if fail_count > 2:
        fail_count = 0
        return "An Error occured, because Cosec cannot code, restarting..."

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
        return tell_kuki(query)

    response_json = json.loads(response_raw)
    sessionid = response_json.get('sessionid')
    response = list(re.sub(r'<.*?>', ' ', i) for i in response_json['responses'][0].split("\u200e"))
    response = '\n'.join(response)

    if len(response)==0:
        print("zero response")
        print(response_json)
        client_name = new_client()
        fail_count+=1
        return tell_kuki(query)

    fail_count = 0

    return response

if __name__ == "__main__":
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options = chrome_options, desired_capabilities=caps)
    wait = WebDriverWait(driver, 20)

    url = 'https://www.pandorabots.com/mitsuku/'
    session = requests.Session()
    client_name = new_client()
    botkey = "n0M6dW2XZacnOgCWTp0FRYUuMjSfCkJGgobNpgPv9060_72eKnu3Yl-o1v2nFGtSXqfwJBG2Ros~"
    sessionid = "null"

    fail_count = 0

    load_dotenv(dotenv_path = "token.env")
    token = os.getenv("DISCORD_TOKEN")
    client.run(token)
