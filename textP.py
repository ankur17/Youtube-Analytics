from __future__ import division
from pprint import pprint
from bs4 import BeautifulSoup
import urllib2
import requests
import pandas as pd
import numpy as np
import re
import os
url = "" #Enter the link of the channel here
sc = requests.get(url)

soup = BeautifulSoup(sc.text,'html.parser')
# anime = soup.select('li a')
print "======Following is the description====="

video_Alllists = soup.find_all("div", class_="yt-lockup-content")
name = list()
duration = list()
Uploaded = list()
for line in video_Alllists[:2]:
	# print line.a.get('title')
	print re.findall('\d.*seconds',line.span.text)[0]