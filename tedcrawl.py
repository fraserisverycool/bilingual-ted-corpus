# This file does the corpus making magic, but leaves the corpus unaligned!

from lxml import etree
from io import StringIO
import nltk
from nltk.tokenize import word_tokenize
import sys
import xlsxwriter
import os

# Initialise the tokeniser and parser

tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')
parser = etree.HTMLParser()

# Couple more initialisations

inputname = "crawlhtmls/transcript?language="
outputname = "tedcorpus"
num_of_files = 2086

# We tried lots of approaches, but this is the best: concatenating all the timestamped paragraphs and splitting them into sentences
# Those sentences are stored here
de_sens_total, ko_sens_total = [],[]

# Loop though all the TED transcript files
# They must end in "de.13" or "ko.152" or something like that - you can change this if you want

for y in range(num_of_files):

	# Read the german transcript
	with open(inputname + "de." + str(y)) as f:
		de_tree = etree.parse(StringIO(f.read()), parser)

	# Read the korean transcript
	with open(inputname + "ko." + str(y)) as f:
		ko_tree = etree.parse(StringIO(f.read()), parser)

	# Get the roots from the etree module
	de_root, ko_root = de_tree.getroot(), ko_tree.getroot()

	# Using the roots, collect all the paragraphs
	de_pars, ko_pars = de_root.findall(".//p"), ko_root.findall(".//p")

	# Initialise some lists which will contain the timestamps
	de_timestamps, ko_timestamps = [], []

	# Collect the title and URL of the TED talk for our info file later
	title = de_root.find(".//title").text
	url = de_root.find(".//link").attrib["href"]

	# Loop through all the german paragraphs, which is a bunch of lines with "\n" in them for each timestamp
	for x in range(len(de_pars)):

		# Extract the text from the etree object
		de_par = de_pars[x].text

		# Don't look at more paragraphs than is in the korean transcript, and ignore timestamps where the text is exactly the same
		if len(ko_pars) > x and de_par == ko_pars[x].text:
			continue

		# "de_timestamps" uses join to put all the single lines together
		de_timestamps.append(" ".join([y.strip() for y in de_par.split("\n")]))

	# Loop through all the korean paragraphs, which is a bunch of lines with "\n" in them for each timestamp
	for x in range(len(ko_pars)):

		# Extract the text from the etree object
		ko_par = ko_pars[x].text

		# Don't look at more paragraphs than is in the german transcript, and ignore timestamps where the text is exactly the same
		if len(de_pars) > x and ko_par == de_pars[x].text:
			continue

		# "ko_timestamps" uses join to put all the single lines together
		ko_timestamps.append(" ".join([y.strip() for y in ko_par.split("\n")]))

	# This is where we join together all the words in the documents and split them into sentences with NLTK
	de_sens, ko_sens = tokenizer.tokenize(" ".join(de_timestamps)), tokenizer.tokenize(" ".join(ko_timestamps))

	# This is for the records later!
	unbalanced_de_length, unbalanced_ko_length = len(de_segs), len(ko_segs)

	# Let's just balance out the lists of sentences by adding empty spaces so that they match
	while len(de_sens) != len(ko_sens):
		if len(de_sens) > len(ko_sens):
			ko_sens.append("")
		elif len(ko_sens) > len(de_sens):
			de_sens.append("")
		else:
			print("Something went wrong with balancing out the lists!")
			sys.exit()

	# Here we add all of this particular documents results into a "final" corpus
	de_sens_total += de_sens
	ko_sens_total += ko_sens

	# We make a directory called outputcorpus and in it are all the various pages from the TED talks, in these specific pages we put the data
	if not os.path.exists("outputcorpus/" + str(y)):
		os.makedirs("outputcorpus/" + str(y))

	# PRINTING! This writes to two different files all at once to save time when looping through the TED talks
	# Just the german sentences:
	g = open("outputcorpus/" + str(y) + "/" + outputname + "." + str(y) + ".de", "w")

	# Just the korean sentences:
	h = open("outputcorpus/" + str(y) + "/" + outputname + "." + str(y) + ".ko", "w")

	# Then go through each of the TED talks and write the appropriate information to each one
	for x in range(len(de_sens)):
		g.write(de_sens[x] + "\n")
		h.write(ko_sens[x] + "\n")

	# Write the information file
	i = open("outputcorpus/" + str(y) + "/info.txt","w")
	i.write(title + "\n" + url + "\nNumber of de sentences (before align):\t" + str(unbalanced_de_length) + "\nNumber of ko sentences (before align):\t" + str(unbalanced_ko_length))

	f.close(), g.close(), h.close(), i.close()

	# Print your progress
	if y%100==0:
		print(str(y) + " ted talks already done")


# Print the final corpus, with everything in it

f = open(outputname + ".bloc.tmx", "w")
f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<tmx version=\"1.4\">\n\t<header segtype=\"sentence\" adminlang=\"de\" srclang=\"de\" datatype=\"xml\" creationdate=\"20170408T073750Z\">\n\t</header>\n\t<body>\n")
g = open(outputname + ".bloc.de", "w")
h = open(outputname + ".bloc.ko", "w")
exceldata = [['ID', 'German', 'Korean']]

for x in range(len(de_sens_total)):
	g.write(de_sens_total[x] + "\n")
	h.write(ko_sens_total[x] + "\n")
	f.write("\t\t<tu tuid=\"" + str(x+1) + "\">\n\t\t\t<tuv xml:lang=\"de\">\n\t\t\t\t<seg>" + de_sens_total[x] + "</seg>\n\t\t\t</tuv>\n\t\t\t<tuv xml:lang=\"ko\">\n\t\t\t\t<seg>" + ko_sens_total[x] + "</seg>\n\t\t\t</tuv>\n\t\t</tu>\n")
	exceldata.append([str(x+1),de_sens_total[x],ko_sens_total[x]])

f.write("\t</body>\n</tmx>")

f.close(), g.close(), h.close()

row, col = 0, 0
workbook = xlsxwriter.Workbook("outputcorpus/" + outputname + ".xlsx")
worksheet = workbook.add_worksheet()
for tuid, de, ko in exceldata:
	worksheet.write(row, col, tuid)
	worksheet.write(row, col + 1, de)
	worksheet.write(row, col + 2, ko)
	row += 1
workbook.close()
