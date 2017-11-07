# This is for making a list of URLs of TED talks to download

import glob
import re

files = glob.glob("htmls/*")

h = open("koreanurls.txt", "w")

for filename in files:
	with open(filename) as f:
		data = f.read()
	links = re.findall("href=(.*?)\?language=ko", data)
	count = 0
	for link in links:
		if link != "\"/talks":
			count += 1
			if count%2==0:
				h.write(link[1:] + "\n")