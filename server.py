import sys
from io import BytesIO

import requests
from flask import Flask, request, send_file

import telegram
from randy_bot import randyMachine

from random import randint
from randy_bot import *

app = Flask(__name__)

bot_token = "527773154:AAGWCJJmg9s70uZi4GF3V5d0AIcDUt0IzYg"

bot = telegram.Bot(token=bot_token)
machine = randyMachine(
    states=[
		'menu',
		'scheduling_mode',
        'calm',
        'annoyed',
        'angry',
        'rage'
    ],

    transitions=[
		{
			'trigger': 'advance',
			'source': 'menu',
			'dest': 'calm',
			'conditions': 'menu_to_calm'
		},
        {
            'trigger': 'advance',
            'source': 'calm',
            'dest': 'annoyed',
			'conditions': 'calm_to_annoyed'
        },
        {
            'trigger': 'advance',
            'source': 'annoyed',
            'dest': 'angry',
			'conditions': 'annoyed_to_angry'
        },
        {
            'trigger': 'advance',
            'source': 'angry',
            'dest': 'rage',
			'conditions': 'angry_to_rage'
        },
		{
			'trigger': 'advance',
			'source': 'rage',
			'dest': 'rage',
			'conditions': 'rage_to_rage'
		},
		{
			'trigger': 'advance',
			'source': [
				'calm',
				'annoyed',
				'angry',
				'rage'
			],
			'dest': 'calm',
			'conditions': 'back_to_calm'
		},
		{
			'trigger': 'advance',
			'source': [
				'calm',
				'annoyed',
				'angry',
				'rage'
			],
			'dest': 'menu',
			'conditions': 'back_to_menu'
		}
    ],
    initial='menu',
    auto_transitions=False,
    show_conditions=True
)


def get_url(method):
    return "https://api.telegram.org/bot{}/{}".format(bot_token, method)


# def process_message(update):
    # data = {}
    # data["chat_id"] = update["message"]["from"]["id"]
    # data["text"] = "Say something"
    # r = requests.post(get_url("sendMessage"), data=data)


@app.route("/{}".format(bot_token), methods=["POST"])
def process_update():
	if request.method == "POST":
    	# process_message(update)
		update = telegram.Update.de_json(request.get_json(force=True), bot)
		if machine.state == 'menu':
			update.message.reply_text("please select a mode:\n/angry_randy - try to annoy Randy.\n/scheduling - Randy will help you manage your schedule.\n/menu - see what Randy can do.")
			
		else:
			if machine.state == 'calm':
				update.message.reply_text(listCalm[randint(0,2)])
				machine.calmCnt = machine.calmCnt+1
			elif machine.state == 'annoyed':
				update.message.reply_text(listAnnoyed[randint(0,2)])
				machine.annoyCnt = machine.annoyCnt+1

			elif machine.state == 'angry':
				update.message.reply_text(listAngry[randint(0,2)])
				machine.angryCnt = machine.angryCnt+1
		
			elif machine.state == 'rage':
				update.message.reply_photo(listGrandma[randint(0,2)])
		
		print("current state: ", machine.state)
		machine.advance(update)

		return "ok!", 200

@app.route('/show-fsm', methods=['GET'])
def show_fsm():
	byte_io = BytesIO()
	machine.graph.draw(byte_io, prog='dot', format='png')
	byte_io.seek(0)
	return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

