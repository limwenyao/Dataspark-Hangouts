import sys
import csv
import tweepy
import matplotlib.pyplot as plt
import os
import json

from collections import Counter
from aylienapiclient import textapi

def getSentiment(subject):

  filepath = os.path.dirname(os.path.realpath(__file__))
  # print filepath
  oldFilename = "eventdata_"+subject+'.json'
  filename = os.path.join(filepath,oldFilename)
  # print filename
  filelist = os.listdir(filepath)
  # print 'oldFilename',oldFilename
  # print 'filelist',filelist
  if oldFilename in filelist:
    print "File exists"
    data = json.load(open(filename))
    # print data
    return data

  # if sys.version_info[0] < 3:
  #    input = raw_input

  ## Twitter credentials
  consumer_key = "qkSwIveFpaFGd2PkJXx8q45II"
  consumer_secret = "AKZY0u4faQYituN9rqsp5T4dVOegRuRgn3ZKtKrey77zDBIvO4"
  access_token = "1925790914-pDKSVrgpQ1XYDdI6sxGQziMmPFdDj9v8Cytxycp"
  access_token_secret = "lPIMEi97wlk7tqd6eFtXb6NVMco6EftJfQd10JOucHM45"

  ## AYLIEN credentials
  application_id = "c25cbda9"
  application_key = "b12b250de88a56695ea787b3bf5b2993"

  ## set up an instance of Tweepy
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)

  ## set up an instance of the AYLIEN Text API
  client = textapi.Client(application_id, application_key)

  ## search Twitter for something that interests you
  # query = input("What subject do you want to analyze for this example? \n")
  # number = input("How many Tweets do you want to analyze? \n")
  query = subject
  number = 5

  results = api.search(
     lang="en",
     q=query + " -rt",
     count=number,
     result_type="recent",
     geocode = "1.352083,103.819836,25km"
  )

  print("--- Gathered Tweets \n")

  ## open a csv file to store the Tweets and their sentiment 
  # file_name = 'Sentiment_Analysis_of_{}_Tweets_About_{}.csv'.format(number, query)

  # with open(file_name, 'w') as csvfile:
  #    csv_writer = csv.DictWriter(
  #        f=csvfile,
  #        fieldnames=["Tweet", "Sentiment"]
  #    )
  #    csv_writer.writeheader()

     # print("--- Opened a CSV file to store the results of your sentiment analysis... \n")

  listOfTweets = []
  ## tidy up the Tweets and send each to the AYLIEN Text API
  for c, result in enumerate(results, start=1):
         tweet = result.text
         tidy_tweet = tweet.strip().encode('ascii', 'ignore')

         if len(tweet) == 0:
             print('Empty Tweet')
             continue

         response = client.Sentiment({'text': tidy_tweet})
         listOfTweets.append((str(response['text']).replace('\n', ' '), str(response['polarity'])))

         print("Analyzed Tweet {}".format(c))
  sum = 0
  for tweet in listOfTweets:
    if tweet[1]=='positive':
      sum+=1
    elif tweet[1]=='neutral':
      sum+=0.5
    else:
      sum+=0
  
  jsondata = {'tweets':listOfTweets, 'overall':sum/float(number)}
  with open(filename, 'w') as f:
    json.dump(jsondata, f)
  # return listOfTweets,sum/float(number)
  return jsondata

if __name__=="__main__":
  print getSentiment('River Hongbao 2018')