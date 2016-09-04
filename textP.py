from __future__ import division
from pprint import pprint
from bs4 import BeautifulSoup
import urllib2
import requests
import pandas as pd
import numpy as np
import re
import os

longWork = False

def getUpload(href):
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


url = "https://www.youtube.com/channel/UCUSkquV90DhVgCk49XXqbBw/videos" #Enter the link of the channel here
url = "https://www.youtube.com/channel/UCUSkquV90DhVgCk49XXqbBw/videos?view=0&shelf_id=0&sort=dd" #Enter the link of the channel here
sc = requests.get(url)

soup = BeautifulSoup(sc.text,'html.parser')
# anime = soup.select('li a')
print "======Following is the Analysis ANkurji====="

video_Alllists = soup.find_all("div", class_="yt-lockup-content")
title = list()
duration = list()
uploadLag = list()
date = list()
view = list()

for line in video_Alllists:
	if longWork:
		date.append(getUpload(line.a.get('href')))
	uploadLag.append(line.find_all('li')[1].text)
	view.append(line.li.text)
	title.append(line.a.get('title'))
	duration.append(re.findall('\d.*',line.span.text)[0][:-1])

titlePd = pd.Series(title)
durPd = pd.Series(duration)
viewPd = pd.Series(view)
uploadLagPd = pd.Series(uploadLag)

d = dict()
attributes = [('Title',titlePd),('Duration',durPd),('Views',viewPd),('Upladed Ago',uploadLagPd)]

if longWork:
	d['Date'] = pd.Series(date)
d = buildDict(attributes)
df = pd.DataFrame(d)
pprint(df.head(40))




#############################################################################################
