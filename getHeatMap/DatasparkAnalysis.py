from datetime import datetime
import json, ast
import requests
import base64

import sys, os, time, math, re
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from IPython.display import display, HTML
from datetime import date, timedelta

def dataAnalysis():

	#Load back all datasets
	#TODO: CHANGE os.getcwd
	allFiles = glob.glob(os.path.dirname(os.path.realpath(__file__)) + "/dataspark_exported*.csv")
	# allFiles = glob.glob(os.getcwd() + "/dataspark_exported*.csv")
	frame = pd.DataFrame()
	list_ = []
	for file_ in allFiles:
	    df = pd.read_csv(file_, header=0)
	    list_.append(df)
	df = pd.concat(list_)
	df['timestamp'] = df['timestamp'].map(lambda x: re.sub('T', ' ', x))
	df['timestamp'] = df['timestamp'].map(lambda x: x.split("+")[0])

	#Do some useful data manipulation
	df['average_stay_duration'] = df['total_stay_duration']/df['total_stay']
	df['timestamp'] = df['timestamp'].astype('datetime64[ns]')
	df.insert(1,'time',df['timestamp'].dt.time.astype(str))
	df.insert(2,'day',df['timestamp'].dt.dayofweek.astype(str))

	#Aggregate 10 week data into 1 week, using median.
	week_hour_agg = df.groupby(['staypoint_subzone','time','day']).median().reset_index().sort_values(['day','time'])

	#Median Subtraction
	df_medianreduce = df.merge(week_hour_agg,'left',['staypoint_subzone','time','day'])
	df_medianreduce['total_stay_diff'] = df_medianreduce['total_stay_x'] - df_medianreduce['total_stay_y']

	#Median Log Division
	df_medianreduce['total_stay_log_divison'] = np.log(df_medianreduce['total_stay_y'] / df_medianreduce['total_stay_x'])

	#TODO: A GET REQUEST FOR USER TO SPECIFY DATE/TIME
	USR_DT = '2018-02-17 13:00:00'
	compare_df = df.loc[df['timestamp'] == USR_DT]
	compare_df = compare_df.merge(week_hour_agg,'left',['staypoint_subzone','time','day'])
	compare_df['total_stay_diff'] = compare_df['total_stay_x'] - compare_df['total_stay_y']
	compare_df['total_stay_log_divison'] = np.log(compare_df['total_stay_y'] / compare_df['total_stay_x'])
	print(compare_df)

	subzone_anomaly = pd.Series(compare_df.total_stay_log_divison.values, index = compare_df.staypoint_subzone).to_dict()
	subzone_anomaly['max'] = np.nanmax(np.array(subzone_anomaly.values()))
	subzone_anomaly['min'] = min(subzone_anomaly.values())

	return subzone_anomaly

if __name__=="__main__":
	print dataAnalysis()
