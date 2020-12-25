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

from googletrans import Translator
from indictrans import Transliterator

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

client = discord.Client()
kaushik = re.compile('Kaushik( Sivashankar)?',re.IGNORECASE)
pandora = re.compile('Pandorabots',re.IGNORECASE)
translator = Translator()


@client.event
async def on_ready():
    print("Kuki has connected to Discord!")


@client.event
async def on_message(message):
    if str(message.channel) == 'chat-with-kuki' and message.author != client.user:
        print(message.content)
        if message.content[0] != '/':
            if '>' in message.content:
                await message.channel.send('I do not support quoted messages and users for now, sorry!')

            else:
                translateResponse = False

                print(message.content)

                if translator.detect(message.content).lang == 'hi':
                    message.content = translator.translate(message.content).text
                    translateResponse = True

                new_message = kaushik.sub('Pandorabots', message.content)
                response = pandora.sub('Kaushik',tell_kuki(new_message))

                if translateResponse:
                    response = translator.translate(response,src='en',dest='hi').text
                    trn = Transliterator(source='hin', target='eng', build_lookup=True)
                    response = trn.transform(response).replace('kowshik','Kaushik')

                await message.channel.send(response)


def new_client():
    try:
        driver.get(url)

        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pb-widget__description__chat-now__button"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "pb-widget-input-field"))).send_keys("Hey"+Keys.ENTER)

        browser_log = str(driver.get_log('performance'))
        client_name = re.search(r'kukilp-.{10}', browser_log)[0]
        driver.quit()

    except:
        driver.quit()
        print("Could not forge client, making a random one instead")
        client_name = 'kukilp-'+''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(10))

    return client_name


def postit(botkey, query, client_name, sessionid):
    data = f'input={query}&sessionid={sessionid}&channel=6&botkey={botkey}&client_name={client_name}'
    return requests.post('https://miapi.pandorabots.com/talk', data=data, headers=headers).text


def tell_kuki(query):
    global botkey, sessionid, client_name, channel, fail_count

    if fail_count > 2:
        fail_count = 0
        return "An Error occured, because Kaushik sucks, restarting..."


    tosend = re.sub(r'\s+', ' ', query).strip()
    tosend = urllib.parse.quote(tosend)
    print('Retrieving response.')

    try:
        response_raw = postit(botkey, tosend, client_name, sessionid)

    except Exception as e:
        print("Error", e)
        fail_count += 1
        return tell_kuki(query)

    response_json = json.loads(response_raw)
    sessionid = response_json.get('sessionid')
    # response = list(re.sub(r'<.*?>', ' ', i) for i in response_json['responses'][0].split("\u200e"))
    response = '\n'.join(response_json['responses'][0].split("\u200e"))

    fail_count = 0

    return response


if __name__ == "__main__":
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options, desired_capabilities=caps)
    wait = WebDriverWait(driver, 20)

    url = 'https://www.pandorabots.com/mitsuku/'

    headers = {
        'host': 'miapi.pandorabots.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept':'*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': url,
        'Content-type': 'application/x-www-form-urlencoded'
    }

    client_name = new_client()
    botkey = "n0M6dW2XZacnOgCWTp0FRYUuMjSfCkJGgobNpgPv9060_72eKnu3Yl-o1v2nFGtSXqfwJBG2Ros~"
    sessionid = "null"

    fail_count = 0

    load_dotenv(dotenv_path=os.path.join(sys.path[0], "token.env"))
    token = os.getenv("DISCORD_TOKEN")
    client.run(token)
