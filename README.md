# TOC FINAL PROJECT: chatbot

### search for 'Randy' in telegram to find it

### usage:
1.	type '/menu' or simply type anything to see the menu of Randy.
2.	there are two modes of this bot. '/angry_randy' or '/scheduling'.
3.	'/angry_randy' is a mode that you can annoy Randy as much as you like, until it reaches the final state. Type in 'sorry' to calm Randy down, he'll be nice again. You can see what he does when he reaches the final state.
4.	'/scheduling' is a mode that you can manage your schedule. Um....Well it's meant to be, but I don't have time to revise Randy into a very convenient schedule manager ;(
5.	You still can enter your schedule in the format <'schedule'-'time'>. 
	for example: buy groceries-9:15
	But Randy only shows you the schedule you entered so far, it won't remind you.
	So it's more like a "to do list bot" :|

### environment setup
*	Well I prefer opening up three three terminals
*	one for ngrok: run `./ngrok http 5000`, modify the token and web URL in server.py and webhook.py
*	one for server.py: run `export FLASK_APP=server.py` and  `flask run`, the server should
*	one for webhook.py: this one's a bit trickier, I had to install "pipenv" for running webhook(or else it just can't work), anyways, run `pipenv shell` to create a virtual shell, then run `python3 webhook.py`

*	there you go!!! you're all set to chat with Randy
