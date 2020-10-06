from flask import Flask
app=Flask(__name__)
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import request
class TwitterClient(object):
	''' 
	Generic Twitter Class for sentiment analysis.
	'''
        
	def __init__(self):
		''' 
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key = 'b1j7iT6GBsR3TA57mru9RQDOC'
		consumer_secret = 'IloyDAE9Pi9tUteDwCwXXBhGL0MEjiji7QxRlZx991mpWuXQ8n'
		access_token = '1268141730458505216-f84B621tgaHsJ40KdVIFnzSAVEfigH'
		access_token_secret = 'kX71My5BevDfETRpQP8jXJHnONAHVZNMfw9NzWRkDyWB5'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")
        
	def clean_tweet(self, tweet):
		''' 
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        
	def get_tweet_sentiment(self, tweet):
		''' 
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'
        
	def get_tweets(self, query, count = 10):
		''' 
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q = query, count = count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

def collectinginput():
	celebrityName=request.form.get("bt1")
	return celebrityName 


def main():
	# creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    q=collectinginput()
    tweets = api.get_tweets(query = q , count = 200)
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    pos=100*len(ptweets)/len(tweets)
    neg=100*len(ntweets)/len(tweets)
    neu=100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)
    new_data={'p_name':['POSITIVE','NEUTRAL','NEGATIVE'],'value1':[pos,neu,neg]} 
    df=pd.DataFrame.from_dict(new_data)
    fig=plt.figure(figsize=(7,4))
    ax1=plt.subplot(1,1,1)
    ax1.barh(df.p_name,df.value1)
    for Y,X in enumerate(df.value1):
       ax1.annotate("{:,}".format(X),xy=(X,Y))
    ax1.set_xlim(0,df.value1.max()*1.50)
    plt.title("SENTIMENT ANALYSIS ON "+q) 
    plt.show() 	

if __name__ == "__main__": 
    # calling main function 
    main() 
