
# coding: utf-8

# In[1]:

from __future__ import division
from IPython.core.display import display, HTML
from pprint import pprint
from bs4 import BeautifulSoup
import urllib2
import requests
import pandas as pd
import numpy as np
import re
import os
import time
# from tqdm import tqdm
import thread as th
import sys

# In[9]:

########  USER INPUTS  ###################
longWork = True
beautify = False
#Enter the link of the channel here
urlList = list()
handle = open('./ChannelList.txt','r')
for a in handle:
    ss = re.findall('https://www.youtube.com/.*videos',a)
    if len(ss):
        urlList.append(ss[0])
handle.close()

#############################################

def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val > 10 else 'black'
    return 'color: %s' % color


def getUpload(href):
    #This is the Date of uplad of the video
	url="https://www.youtube.com"+href
	sc = requests.get(url)
	oo = str()
	soup = BeautifulSoup(sc.text,'html.parser')
	oo = soup.find_all("strong", class_="watch-time-text")[0].text[13:]
	return oo
	# return date

def buildDict(listValuePair):
	di = dict()
	for col,row in attributes:
		di[col] = row 
	return di

def channelTotal(url):
    global TotalViews,TotalSubscriber,ChannelName
    urlAbout = url.replace('videos','about')
    sc = requests.get(urlAbout)
    soup = BeautifulSoup(sc.text,'html.parser')
    about_list = soup.find_all("span",class_="about-stat")
    # subdcribers = about_list[0].span.text
    TotalViews = about_list[1].text[2:]
    TotalSubscriber = about_list[0].text
    ChannelName=soup.title.text.replace('YouTube','').replace('-','').replace('\n','')
    print "----------", ChannelName.upper() ,"----------"
    print "Total Views: ", TotalViews
    print "Total Subscribers: ", TotalSubscriber
    print about_list[2].text
    

for url in urlList:
	channelTotal(url)
# 	th.start_new_thread( channelTotal, (url,) )
    
	sc = requests.get(url)

	soup = BeautifulSoup(sc.text,'html.parser')

	video_Alllists = soup.find_all("div", class_="yt-lockup-content")
	title = list()
	duration = list()
	uploadLag = list()
	date = list()
	view = list()
	viewPercent = list()
	d = dict()

	for line in video_Alllists:
		if longWork:
			date.append(getUpload(line.a.get('href')))
		uploadLag.append(line.find_all('li')[1].text)
		view.append(line.li.text)
		title.append(line.a.get('title'))
		duration.append(re.findall('\d.*',line.span.text)[0][:-1])

	datePD = pd.Series(date)    
	titlePd = pd.Series(title)
	durPd = pd.Series(duration)
	viewPd = pd.Series(view)
	uploadLagPd = pd.Series(uploadLag)
	attributes = [('Title',titlePd),('Duration',durPd),('Views',viewPd),('Upladed Ago',uploadLagPd)]

	d = buildDict(attributes)
	df = pd.DataFrame(d)
    
    
	if longWork:
		df['Date'] = pd.Series(date)
	   
	
	if not os.path.isfile('./DataFrames/'+ChannelName):
		df.to_pickle('DataFrames/'+ ChannelName)
        
	
	df_old = pd.read_pickle('DataFrames/'+ ChannelName)
	df = pd.concat([df,df_old]).drop_duplicates(subset=['Duration','Title']).reset_index(drop=True)
#     ,ignore_index=True
# 	try:
# 		fake = df_old.analyticStartDate
# 	except:
# 		df.analyticStartDate = time.ctime()
# 	print "Analytics Starting time:",df.analyticStartDate
    
# 	#Updating the saves
	df.to_pickle('DataFrames/'+ ChannelName)  ####FOR DEBUGGING#####
    
	#Finding the %age of the views
	view_sum = int(TotalViews.replace('views',' ').replace(',',''))
	for eachView in df['Views']:
	    viewPercent.append(round(int(eachView.replace('views',' ').replace(',',''))/view_sum*100,2))
	viewPercentPd = pd.Series([str(a) +'%' for a in viewPercent])
	df['View Percentage'] = viewPercentPd
	if sys.argv[1]=='terminal':
		pprint(df)
	else:
		if beautify:
			display(HTML(df.to_html()))
		else:
			s = df.style.applymap(color_negative_red)
			df.style.bar(subset=['Views'], color='#d65f5f') ##Fails because its in string

print "======Done====="






