# -*- coding: utf-8 -*-

import os
import time
import uuid
import asyncio
import telepot
import telepot.aio
import hangoutLinker

token = os.getenv('TELEHANGBOT_TELEGRAM_TOKEN')
commands = [u'/потрындеть',u'/перетереть',u'/takeacall',u'/tac',u'/попиздеть',u'/поговорить',u'/беседа',u'/переговоры']
link_by_user = dict()

async def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    if content_type != 'text':
        return

    command = msg['text'].lower()
    if command in commands:
        await bot.sendMessage(chat_id, hangoutLinker.getlink())


async def on_inline_query(msg):
    async def compute_answer():
            query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
            print('Inline Query:', query_id, from_id, query_string)

            uri = link_by_user.get(from_id)

            if uri is None:
                #generate link and put in cache to avoid link generation on each query_string
                uri = hangoutLinker.getlink()
                link_by_user[from_id] = uri

            articles = [{
                    'type': 'article',
                    'id': str(uuid.uuid4()), 
                    'thumb_url': 'http://zags.interfacetesting.ru/lavrov.jpg',
                    'title': 'Начать сложные переговоры с шутки: ' + query_string, 
                    'message_text': query_string + '\r\n' + uri
                }]

            return articles

    result = await compute_answer()
    await bot.answerInlineQuery(msg['id'], result, 1)


def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)
    #remove link from cache
    if link_by_user.get(from_id) is not None:
        link_by_user.pop(from_id)   

#take some time to start selenium server
time.sleep(30)
hangoutLinker.sepUpAndLogin()

bot = telepot.aio.Bot(token)
answerer = telepot.aio.helper.Answerer(bot)
loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop({'chat': on_chat_message,
                                   'inline_query': on_inline_query,
                                   'chosen_inline_result': on_chosen_inline_result
                                   }))
print('Listening ...')

loop.run_forever()