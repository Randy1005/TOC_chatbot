from transitions.extensions import GraphMachine
from random import randint

listCalm = ["May I help you??", "Umm....Yes??", "???"]
listAnnoyed = ["You're being annoying right now...", "I'm almost out of patience", "Just what do you want from me??"]
listAngry = ["Fxck off right now and I'll pretend nothing happened", "SHUT UP!!", "STOP IT!!"]
listGrandma = ["https://i.imgur.com/m3J0acg.jpg", "https://i.imgur.com/KJ7iU9I.jpg", "https://i.imgur.com/Mb5YaGB.jpg"]

class randyMachine(GraphMachine):
	calmCnt = 0
	annoyCnt = 0
	angryCnt = 0
	from_menu = 0

	def __init__(self, **machine_configs):
		self.machine = GraphMachine(
			model=self,
			**machine_configs
		)
	def menu_to_calm(self, update):
		text = update.message.text
		if text == '/angry_randy':
			self.from_menu = 1
			return 1
		else:
			return 0

	def on_enter_menu(self, update):
		update.message.reply_text("please select a mode:\n/angry_randy - try to annoy Randy.\n/scheduling - Randy will help you manage your schedule.\n/menu - see what Randy can do.")

	def on_enter_calm(self, update):
		if self.from_menu == 1:
			self.calmCnt = 0
			self.annoyCnt = 0
			self.angryCnt = 0
			update.message.reply_text("(sigh)....Alright then....")
			self.from_menu = 0
		else:
			self.calmCnt = 0
			self.annoyCnt = 0
			self.angryCnt = 0
			update.message.reply_text("Please...Don't do this again.")


	def calm_to_annoyed(self, update):
		if self.calmCnt > 3:
			return 1
		else:
			return 0
			
		
	def on_enter_annoyed(self, update):
		print("now annoyed.")


	def annoyed_to_angry(self, update):
		if self.annoyCnt > 3:
			return 1
		else:
			return 0
	
	def on_enter_angry(self, update):
		print("now angry.")

	def angry_to_rage(self, update):
		if self.angryCnt > 3:
			return 1
		else:
			return 0
	
	def on_enter_rage(self, update):
		update.message.reply_text("YOU ASKED FOR THIS.")

	def rage_to_rage(self, update):
		text = update.message.text
		if text == 'sorry':
			return 0
		elif text == '/menu':
			return 0
		else:
			return 1


	def back_to_calm(self, update):
		text = update.message.text
		return text.lower() == 'sorry'
	
	def back_to_menu(self, update):
		text = update.message.text
		return text.lower() == '/menu'

