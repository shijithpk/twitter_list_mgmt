#!/usr/bin/env python3

#code from https://github.com/ravikiranj/twitter-challenge/blob/master/auth.py 

import tweepy
import configparser

class getAPIHandle:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config_twitter.ini')


        CONSUMER_KEY = config['info']['CONSUMER_KEY']
        CONSUMER_SECRET = config['info']['CONSUMER_SECRET']
        ACCESS_TOKEN = config['info']['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = config['info']['ACCESS_TOKEN_SECRET']

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        
    def getAPI(self):
        return self.api