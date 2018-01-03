import sys
from io import BytesIO

import requests
from flask import Flask, request, send_file

import simplejson as json
import urllib

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
		'scheduler',
		'scheduling',
        'calm',
        'annoyed',
        'angry',
        'rage'
    ],

    transitions=[
		# menu to angry_randy
		{
			'trigger': 'advance',
			'source': 'menu',
			'dest': 'calm',
			'conditions': 'menu_to_calm'
		},
		
		# scheduling mode
		{
			'trigger': 'advance',
			'source': 'menu',
			'dest': 'scheduler',
			'conditions': 'menu_to_scheduler'
		},
		{
			'trigger': 'advance',
			'source': 'scheduler',
			'dest': 'menu',
			'conditions': 'scheduler_to_menu'
		},
		{
			'trigger': 'advance',
			'source': 'scheduler',
			'dest': 'scheduling',
			'conditions': 'start_scheduling'
		},
		{
			'trigger': 'advance',
			'source': 'scheduling',
			'dest': 'scheduler',
			'conditions': 'end_scheduling'
		},

		# state transition of angry_randy mode
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

#def build_keyboard(schedules):
#	keyboard = [[schedule] for schedule in schedules]
#	reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
#	return json.dumps(reply_markup)

#def send_message(text, chat_id, reply_markup=None):
#	text = urllib.parse.quote_plus(text)
#	url = "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
#	if reply_markup:
#		url += "&reply_markup={}".format(reply_markup)
#	get_url(url)

# process message for database
def process_message(update):
	text = update["message"]["text"]
	chat_id = update["message"]["chat"]["id"]
	schedules = machine.db.get_sched()
	if text == "/end":
		update.message.reply_text("Your TODO list:\n")
		schedules = machine.db.get_sched()
		message = "\n".join(schedules)
		update.message.reply_text(message)
	else:
		sch, time = text.split("-", 1)
		if sch in schedules:
			machine.db.delete_sched(sch)
			schedules = machine.db.get_sched()
			message = "\n".join(schedules)
			update.message.reply_text(message)			
		else:
			machine.db.add_sched(sch, time)
			schedules = machine.db.get_sched()
			message = "\n".join(schedules)
			update.message.reply_text(message)
			

@app.route("/{}".format(bot_token), methods=["POST"])
def process_update():
	if request.method == "POST":
		update = telegram.Update.de_json(request.get_json(force=True), bot)
		if machine.state == 'menu':
			update.message.reply_text("please select a mode:\n/angry_randy - try to annoy Randy.\n/scheduling - Randy will help you manage your schedule.\n/menu - see what Randy can do.")
		
		elif machine.state == "scheduling":
			process_message(update)

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

