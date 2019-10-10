import requests
import oauth2 as oauth
import os
import urllib
import argparse
import json
from twitter import *
from random import randint
from PIL import Image, ImageDraw, ImageFont
import landscape

# Constants
post_tweet_endpoint = 'https://api.twitter.com/1.1/statuses/update.json'
upload_photo_endpoint = 'https://upload.twitter.com/1.1/media/upload.json'

# Fetch environment variables
CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
ACCESS_KEY = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

# Create client
t = Twitter(
    auth=OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

def generateImage():
    return landscape.generate_landscape()

def upload_image(image):
    image.save("/tmp/tat.png")
    with open("/tmp/tat.png", "rb") as imagefile:
        imagedata = imagefile.read()

    # - then upload medias one by one on Twitter's dedicated server
    #   and collect each one's id:
    t_upload = Twitter(domain='upload.twitter.com',
        auth=OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]
    print("uploaded with id_img1: ", id_img1)

    # - finally send your tweet with the list of media ids:
    t.statuses.update(status='soothing', media_ids=",".join([id_img1]))

def lambda_handler(_event_json, _context):
    image = generateImage()
    upload_image(image)
