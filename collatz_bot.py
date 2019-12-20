import sys
import threading
import logging
from time import sleep
from keys2 import keys2
import tweepy


# Class for the Stream
class StreamListener(tweepy.StreamListener):

	def __init__(self, output_file=sys.stdout):
		super(StreamListener, self).__init__()
		self.output_file = output_file

	def on_status(self, status):
		self.seq = []
		print(status.text)
		screen_name = status.user.screen_name
		x = status.text.replace("#CollatzCon",'')
		num = int(x)
		self.collatz(num)
		list = self.seq
		stri = ','.join([str(elem) for elem in list])
		message = "%s" % (stri)
		api.update_status(message, in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)

	def on_error(self, status_code):
		if status_code == 420:
			return False

	seq =[]
	# Function to recursively find the collatz
	def collatz(self, n):
		if n ==1:
			return n
		elif n % 2 == 0 :
			n = int(round(n /2))
			self.seq.append(n)
			self.collatz(n)
		else:
			n = 3*n +1
			self.seq.append(n)
			self.collatz(n)
		return self.seq

# Key Setup
CONSUMER_KEY = keys2['consumer_key']
CONSUMER_SECRET = keys2['consumer_secret']
ACCESS_TOKEN = keys2['access_token']
ACCESS_TOKEN_SECRET = keys2['access_token_secret']

# Auth Config
auth =  tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Fetching tweets, and listening?
def receiver():
	logging.info("The receiver thread has started")
	streamListener = StreamListener()
	stream = tweepy.Stream(auth=api.auth, listener=StreamListener())
	stream.filter(track=['#CollatzCon'], is_async=True)

if __name__ == "__main__":
	try:
		th1 = threading.Thread(target=receiver)
		th1.start()
	except KeyboardInterrupt:
		print("Bye")
		sys.exit()
