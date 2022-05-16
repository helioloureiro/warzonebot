#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

## Static constants
HOMEDIR = os.environ.get('HOME')
# mv ~/.warzonebotrc ~/.config/warzonebot/config
CONFIGFILE = f'{HOMEDIR}/.config/warzonebot/config'
STATUSDATA = 'https://support.activision.com/services/apexrest/web/oshp/landingpage/'

import sys, re, time
import configparser

import json
try:
    import requests
except ImportError:
    print("Install requests: pip3 install requests")
    raise Exception("Missing module requests")
try:
    from colorama import init, Fore, Back, Style
except ImportError:
    print("Install colorama: pip3 install colorama")
    raise Exception("Missing module colorama")
init()

try:
    import telebot
except ImportError:
    print(Style.BRIGHT + Fore.WHITE + "Install pyTelegramBotAPI: pip3 install pyTelegramBotAPI")
    print("https://github.com/eternnoir/pyTelegramBotAPI")
    raise Exception(Fore.RED + "Missing pyTelegramBotAPI" + Style.RESET_ALL)

def greenMsg(message):
    return Fore.GREEN + message + Fore.RESET

def redMsg(message):
    return Fore.RED + message + Fore.RESET

def whiteMsg(message):
    return Fore.WHITE + message + Fore.RESET

def blueMsg(message):
    return Fore.BLUE + message + Fore.RESET

def brightMsg(message):
    return Style.BRIGHT + message + Style.RESET_ALL

def log(message, *args):
    timestamp = time.ctime(time.time())
    print(f"[{timestamp}] {message}", args)

def GetToken():
    with open(CONFIGFILE) as stream:
        config = configparser.ConfigParser()
        config.read_file(stream)
    return config.get("TELEGRAM", "TOKEN")

token = GetToken()
bot = telebot.TeleBot(token)

def startBot():
    global bot
    print("Starting WarzoneBot")
    print(redMsg('That\'s gas you don\'t wanna brief'))

    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        bot.stop_polling()
        sys.exit(0)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    log("New /start or /help requested:", message.from_user.username)
    print(message)
    bot.reply_to(message, 'Use /status to check Warzone network status')

def GetStatusJson():
    req = requests.get(STATUSDATA)
    return req.text
'''
{
  "updatedTime": "2022-05-14T14:31:02.294Z",
  "serverStatuses": [
    {
      "status": null,
      "platform": "All platforms",
      "gameTitle": "Call of Duty: Warzone",
      "eventId": "10856",
      "alertId": "a0i4P00000TyvnlQAB"
    },
    {
      "status": null,
      "platform": "All platforms",
      "gameTitle": "Call of Duty: Vanguard",
      "eventId": "10780",
      "alertId": "a0i4P00000T6CnGQAV"
    },
    {
      "status": null,
      "platform": "All platforms",
      "gameTitle": "Call of Duty: Black Ops Cold War",
      "eventId": "10834",
      "alertId": "a0i4P00000TyrEIQAZ"
    },
    {
      "status": null,
      "platform": "PlayStation 3",
      "gameTitle": "Call of Duty: Black Ops II",
      "eventId": "10852",
      "alertId": "a0i4P00000Tyv6MQAR"
    },
'''

@bot.message_handler(commands=['status'])
def send_status(message):
    log("New /status requested by", message.from_user.username)
    print(message)
    dataJson = GetStatusJson()
    data = json.loads(dataJson)
    if 'serverStatuses' in data:
        print(json.dumps(data['serverStatuses'], indent=4))
    else:
        print(json.dumps(data, indent=4))
    current_time = data['updatedTime']
    log(f"Report time: {current_time}")

    platform = None
    status = None
    for service in data['serverStatuses']:
        if service['gameTitle'] != 'Call of Duty: Warzone':
            continue
        print(service)

        platform = service['platform']
        status = service['status']

        log("Platform:", platform, type(platform))
        if platform is not None: 
            platform.lower()
        log(" * status:", status, type(status))
        if status is not None: 
            status.lower()

        if status is None:
            status = "on line"
    
        status_log = status
        if status == "on line":
            status_log =  greenMsg(status)
        msg = f'Current status is {status_log} for {platform}.'
        log(msg)
        msg = f'Current status is {status} for {platform}.'
        bot.reply_to(message, msg)


if __name__ == '__main__':
    startBot()
