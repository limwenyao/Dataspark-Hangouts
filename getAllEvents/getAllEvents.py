#import mechanize
from bs4 import BeautifulSoup
import cookielib
import pandas
import urllib2
cj = cookielib.CookieJar()
import requests
import unidecode
import json
import googlemaps
from datetime import datetime, date
import csv 
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import numpy as np

#url = "https://www.timeout.com/singapore/things-to-do/things-to-do-in-singapore-this-weekend"
#url = "https://thehoneycombers.com/singapore/events-in-singapore/"
#url = "https://thehoneycombers.com/singapore/top-10-things-to-do-this-weekend-in-singapore-24-25-february-2018/"
#url = "https://thehoneycombers.com/singapore/top-10-things-to-do-this-weekend-in-singapore-17-18-february-2018/"

def dateConstructor(startdate, enddate):
	return startdate.strftime('%d').lstrip('0')+"-"+enddate.strftime('%d').lstrip('0')+'-'+startdate.strftime('%B').lower()+'-'+startdate.strftime('%Y')

# returns a list of events found from website
def getAllEvents(startdate, enddate):

	dateString = dateConstructor(startdate, enddate)

	template_url = "https://thehoneycombers.com/singapore/top-10-things-to-do-this-weekend-in-singapore-%s/"%(dateString)
	print template_url
	try: 
		page = urllib2.urlopen(template_url)
	except:
		page = urllib2.urlopen("https://thehoneycombers.com/singapore/whats-on-weekends-events-singapore-honeycombers-%s/"%(dateString))
	soup = BeautifulSoup(page, 'html.parser')

	p = soup.find_all('p')

	listOfEvents = []
	# children = p.findChildren()
	for each in p:	
		# to eliminate p tags with no bold title
		no_b = True
		for child in each.findChildren():
			if child.name == 'b':
				no_b = False
		if no_b:
			continue
		

		newEvent = {}
		newEvent['EventTitle'] = ''
		newEvent['EventDetails'] = ''
		newEvent['EventDescription'] = ''
		for child in each.findChildren():
			stripped = child.text.strip()
			stripped = unidecode.unidecode(stripped)
			if child.name=='b':
				# print 'EVENT TITLE',child.text
				
				if newEvent['EventTitle'] == '':
					newEvent['EventTitle'] = [stripped]
				else:
					newEvent['EventTitle'].append(stripped)

			elif child.name=='span' and "font-weight: 400" in child.get('style'):
				if child.parent.name == 'i':
					# print 'EVENT DETAILS',child.text
					if newEvent['EventDetails'] == '':
						newEvent['EventDetails'] = [stripped]
					else:
						newEvent['EventDetails'].append(stripped)
				else:

					# print 'EVENT DESCRIPTION',child.text
					if newEvent['EventDescription'] == '':
						newEvent['EventDescription'] = [stripped]
					else:
						newEvent['EventDescription'].append(stripped)
			# print newEvent
		try:
			newEvent['EventTitle'] = ' '.join(newEvent['EventTitle'])
			newEvent['EventDetails'] = ''.join(newEvent['EventDetails'])
			# print 'oldevent',newEvent
			newEvent['EventDescription'] = ' '.join(newEvent['EventDescription'])
			# print 'newevent',newEvent
		except:
			pass
		listOfEvents.append(newEvent)

	for event in listOfEvents:
		if event['EventDetails']!='':
			newDetails = {}
			tempList = event['EventDetails'].split(',')
			newDetails['Name'] = tempList[0].strip()
			listofMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
			if all(item not in tempList[1] for item in listofMonths):
				newDetails['Date'] = ''
				newDetails['Address'] = ', '.join([i.strip() for i in tempList[1:]])
			else:
				newDetails['Date'] = tempList[1].strip()
				newDetails['Address'] = ', '.join(i.strip() for i in tempList[2:])
			event['EventDetails'] = newDetails



	# return listOfEvents
	# for each in listOfEvents:
	# 	print each['EventDetails']
	# 	print '\n'
	newlist = []
	for eachEvent in listOfEvents:
		print eachEvent['EventDetails']
		if eachEvent['EventDetails']:
			formattedData = {}
			print eachEvent
			formattedData['eventName'] = eachEvent['EventDetails']['Name']
			formattedData['eventInfo'] = eachEvent['EventDescription']
			formattedData['eventDate'] = eachEvent['EventDetails']['Date']
			formattedData['evetnCoord'] = getSubZone(eachEvent['EventDetails']['Address'])
			newlist.append(formattedData)
	return newlist

# find dimension of a list 
def dim(a):
    if not type(a) == list:
        return []
    return [len(a)] + dim(a[0])

def getSubZone(address):
	
	subzone = None
	from os import listdir
	from os.path import isfile, join
	onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]
	print onlyfiles

	subzoneFile = 'getAllEvents/subzone.json'
	#retrieve the longtitude and latitude
	key = 'AIzaSyC34ueWVc6iIeObP2BedZhfNo5Z1k8cdmo'
	data = json.dumps({'address':address, 'key': key})
	gmaps = googlemaps.Client(key=key)

	geocode_result = gmaps.geocode(address)
	# google map might fail and return an empty list... if so, we ignore...
	if geocode_result==[]:
		return
	latlng = geocode_result[0]['geometry']['location']
	
	print latlng

	data = json.load(open(subzoneFile))
	for each in data['features']:
		mydim = dim(each['geometry']['coordinates'])
		# to account for 4 dimensional multi polygon in the data.... weird
		if len(mydim)==3:
			polygon = Polygon(each['geometry']['coordinates'][0])
		elif len(mydim)==4:
			polygon = Polygon(each['geometry']['coordinates'][0][0])

		point = Point(latlng['lng'],latlng['lat'])
		# print polygon.contains(point)

		if polygon.contains(point):
			subzone = each['properties']['SUBZONE_C']

	if subzone!=None:
		return subzone
	else:
		return False



if __name__=="__main__":
	
	# print [date(1900, i, 1).strftime('%b')for i in range(1,13)]
	#print datetime(2018, 2, 17)
	#print dateConstructor(datetime(2018, 2, 17), datetime(2018, 2, 18))
	# for i in getAllEvents(datetime(2018, 2, 17), datetime(2018, 2, 18)):
	print getAllEvents(datetime(2018, 2, 17), datetime(2018, 2, 18))
	# 	#print i
	# 	# to exclude events which might not have any event details..so dont bother searching for addr
	# 	if i['EventDetails']!='':
	# 		print 'Event Title:', i['EventDetails']['Name']
	# 		print 'Event Description:', i['EventDescription']
	# 		print 'Event Date:',i['EventDetails']['Date']
	# 		print getSubZone(i['EventDetails']['Address'])
	# 	print '\n'

	# print getSubZone('359, Yishun Ring Road')

