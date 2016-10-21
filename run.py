# -*- coding: utf-8 -*-

import os
import time
import telepot
import hangoutLinker

token = os.getenv('TELEHANGBOT_TELEGRAM_TOKEN')
commands = [u'/потрындеть',u'/перетереть',u'/takeacall',u'/tac',u'/попиздеть',u'/поговорить',u'/беседа',u'/переговоры']

def command_handler(msg):
    """
    handle chat messages
    """
    chat_id = msg['chat']['id']
    command = msg['text']
    
    try:
        print('Got command: %s' % command.encode('ascii', 'ignore').decode('ascii', 'ignore'))
    except Exception: 
        pass
    
    if command in commands:
        bot.sendMessage(chat_id, hangoutLinker.getlink())

#main
#take some time to start selenium server
time.sleep(30)

hangoutLinker.sepUpAndLogin()

bot = telepot.Bot(token)
bot.message_loop(command_handler)

print('bot started')
#keep running
while 1:
	time.sleep(10)
