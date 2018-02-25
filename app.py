from flask import Flask, redirect, render_template
from getAllEvents import getAllEvents
from datetime import datetime
from getSentiments import Sentiment
import json

app = Flask(__name__)

@app.route('/')
def show_viz():

	# TODO 1: placeholder for event title, event information, event date and event coordinates
	# hardcoded date for hackathon purposes
	startDate = datetime(2018, 2, 17)
	endDate = datetime(2018, 2, 18)
	# event -> [{eventName:?, eventInfo:?, eventDate:?, eventCoord:?}, ...]
	event = getAllEvents.getAllEvents(startDate, endDate)
	# print event



	# TODO 2: placeholder for aggregated data for heatmap in json format





	# TODO 3: placeholder for sentiment analysis
	# data structure of sentiment -> [([(tweet1,polarity1), (tweet2,polarity2),(tweet3,polarity3)],0.66), ....]
	# can obtain various tweets as well as the average sentiment values
	for eachEvent in event:
		eachEvent['sentiment'] = Sentiment.getSentiment(eachEvent['eventName'])
	print event


	return render_template('index.html', event=event, aggregated=None)