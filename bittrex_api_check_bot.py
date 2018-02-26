#!/usr/bin/python

from twilio.rest import Client
import requests
import json
import threading
from threading import Timer
from time import sleep
import os

def check():
	twilio_key = os.environ.get('TWILIO_KEY')
	twilio_acct = os.environ.get('TWILIO_ACCOUNT')
	client = Client(twilio_acct, twilio_key)
	coin = 'btcp'
	btc_link = "https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-{}".format(coin)
	eth_link = "https://bittrex.com/api/v1.1/public/getmarketsummary?market=eth-{}".format(coin)
	usdt_link = "https://bittrex.com/api/v1.1/public/getmarketsummary?market=usdt-{}".format(coin)

	links = [btc_link, eth_link, usdt_link]
	recipients = [os.environ.get('MY_SPAIN_NUMBER'), os.environ.get('ZHONGHAN_NUMBER')]
	for link in links:
		data = requests.get(link)
		if(data.text != '{"success":false,"message":"INVALID_MARKET","result":null}'):
			print('match')
			for recipient in recipients:
				client.messages.create(
					    to = recipient,
					    from_ = os.environ.get('TWILIO_NUMBER'),
					    body = data.text,
					)
			exit(0)
		else:
			pass
		
class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer     = None
		self.interval   = interval
		self.function   = function
		self.args       = args
		self.kwargs     = kwargs
		self.is_running = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False
	
if __name__ == '__main__':
	rt = RepeatedTimer(1, check)
	try:
		num_days = 2
		sleep(24*60*60*num_days) # your long-running job goes here...
	finally:
		rt.stop() # better in a try/finally block to make sure the program ends!

