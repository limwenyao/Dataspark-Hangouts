from flask import Flask, redirect, render_template
from getAllEvents import getAllEvents
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def show_viz():

	# placeholder for event title, event information, event date and event coordinates

	# hardcoded date for hackathon purposes
	startDate = datetime(2018, 2, 17)
	endDate = datetime(2018, 2, 18)
	event = getAllEvents.getAllEvents(startDate, endDate)
	print event

	# placeholder for aggregated data for heatmap in json format

	# placeholder for sentiment analysis

	return render_template('index.html', event=None, aggregated=None, sentiment=None)