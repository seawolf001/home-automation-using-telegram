#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Home automation using telegram.
    Team :
            Jitendra Kumar 1401CS19
            Anupam Das  1401CS52

'''

import requests
import json
import time
import RPi.GPIO as GPIO

API_TOKEN = '457914531:AAEIRn1KLSaDO52QT0GFDx_4JlaQqzJboWE'
API_URL = 'https://api.telegram.org/bot%s/' % API_TOKEN


def getUpdates(
    offset=None,
    limit=None,
    timeout=1000,
    allowed_updates=None,
    ):

    params = {
        'offset': offset,
        'limit': limit,
        'timeout': timeout,
        'allowed_updates': allowed_updates,
        }
    return json.loads(requests.get(API_URL + 'getUpdates',
                      params=params).content.decode('utf8'))


def sendMessage(
    chat_id,
    text,
    parse_mode=None,
    disable_web_page_preview=None,
    disable_notification=None,
    reply_to_message_id=None,
    reply_markup=None,
    ):

    params = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode,
        'disable_web_page_preview': disable_web_page_preview,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
        }
    return json.loads(requests.get(API_URL + 'sendMessage',
                      params=params).content.decode('utf8'))


def onLight():
    GPIO.output(pin1, True)


def offLight():
    GPIO.output(pin1, False)


def onFan():
    GPIO.output(pin2, True)


def offFan():
    GPIO.output(pin2, False)


def generateReply(text):
    if text is None:
        print 'DEBUG: Enter valid input'
        return 'Enter valid input'
    text = text.strip().lower()
    if '/onlight' in text:
        print 'DEBUG: Successfully turned on light'
        onLight()
        return 'Successfully turned on light'
    if '/offlight' in text:
        offLight()
        print 'DEBUG: Successfully turned off light'
        return 'Successfully turned off light'
    if '/onfan' in text:
        onFan()
        print 'DEBUG: Successfully turned on fan'
        return 'Successfully turned on fan'
    if '/offfan' in text:
        offFan()
        print 'DEBUG: Successfully turned off fan'
        return 'Successfully turned off fan'
    if '/help' in text:
        output = \
            '''*Welcome to OptiHomeAutomation*
By Team - *Anupam, Jitendra*

Commands supported:
1. */onlight* To turn on lights
2. */offlight* To turn off lights
3. */onfan* To turn on fans
4. */offfan* To turn off fans
'''

        print ('DEBUG: ' + output)
        return output
    return 'Enter valid input'


if __name__ == '__main__':
    start_time = time.time()
    print 'Welcome to OptiHomeAutomation'
    print 'By Team - Anupam, Jitendra'
    print '--------------------------'
    print '''

'''

    GPIO.setmode(GPIO.BOARD)

    # representing pins with variable names for easiness

    pin1 = 11
    pin2 = 12

    # setting up the GPIOs
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)

    offLight()
    offFan()

    last_update_id = -1
    try:
        while True:
            updates = getUpdates(last_update_id + 1)
            for update in updates['result']:
                if last_update_id < update['update_id']:
                    last_update_id = update['update_id']
                    if 'message' in update and start_time \
                        <= update['message']['date']:
                        chat_id = update['message']['chat']['id']
                        message_id = update['message']['message_id']
                        text = update['message']['text']
                        reply = generateReply(text)
                        sendMessage(chat_id, reply, parse_mode='Markdown')
    except KeyboardInterrupt:
        GPIO.cleanup()
