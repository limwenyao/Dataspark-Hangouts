from flask import Flask, redirect, render_template
from getAllEvents import getAllEvents
from datetime import datetime
from getSentiments import Sentiment

app = Flask(__name__)

@app.route('/')
def show_viz():

	# placeholder for event title, event information, event date and event coordinates

	# hardcoded date for hackathon purposes
	startDate = datetime(2018, 2, 17)
	endDate = datetime(2018, 2, 18)

	# event -> [{eventName:?, eventInfo:?, eventDate:?, eventCoord:?}, ...]
	event = getAllEvents.getAllEvents(startDate, endDate)
	print event



	# placeholder for aggregated data for heatmap in json format




	# placeholder for sentiment analysis
	# listOfSentiment -> [([(tweet1,polarity1), (tweet2,polarity2),(tweet3,polarity3)],0.66), ....]
	listOfSentiment = []
	for eachEvent in event:
		listOfSentiment.append(Sentiment.getSentiment(eachEvent['eventName']))
	print listOfSentiment



	return render_template('index.html', event=event, aggregated=None, sentiment=None)