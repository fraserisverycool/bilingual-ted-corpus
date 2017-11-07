# This takes the aligned data and makes the corpus out of it

import re
import xlsxwriter

# Initialise a few things
outputname = "tedcorpus"

# Here I am already opening the "main" corpus files which will contain all TED talks. I will add to them as I loop through the talks
# The TMX file (with the first part already):
j = open("outputcorpus/tedcorpus.total.tmx", "w")
j.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<tmx version=\"1.4\">\n\t<header segtype=\"sentence\" adminlang=\"de\" srclang=\"de\" datatype=\"xml\" creationdate=\"20170408T073750Z\">\n\t</header>\n\t<body>\n")

# The list of aligned german sentences
k = open("outputcorpus/tedcorpus.total.de", "w")

# The list of aligned korean sentences
l = open("outputcorpus/tedcorpus.total.ko", "w")

# The information file
m = open("outputcorpus/info.txt", "w")

# The excel spreadsheet
totalexceldata = [["ID","German","Korean"]]

count = 0

# Here we loop through all the TED talks again...

for y in range(2047):

	# Read the alignment file
	with open("outputcorpus/" + str(y) + "/tedcorpus." + str(y) + ".align") as f:
		data = [x.strip().split("\t") for x in f.readlines()]

	de_sens, ko_sens = [],[]

	# Looking at each line in the alignment file
	for item in data:

		# If the sentence passes these tests: longer than one character, contains a letter in it, then we continue, else it's ignored
		if len(item) > 1 and re.search("[a-zA-Z]",item[0]) and item[1] != "0.3" and item[1] != "-0.3":

			# Extract the sentences in both languages
			de_sen = item[0]
			ko_sen = item[1]

			# Remove these tildes used for 2:1 alignments
			if "~~~" in de_sen:
				de_sen = de_sen.replace("~~~ ", "")
			if "~~~" in ko_sen:
	                        ko_sen = ko_sen.replace("~~~ ", "")
			de_sens.append(de_sen)
			ko_sens.append(ko_sen)

	# PRINTING! This writes to several different files all at once to save time when looping through the TED talks
	# TMX format (includes the first part of the TMX):
	f = open("outputcorpus/" + str(y) + "/" + outputname + "." + str(y) + ".tmx", "w")
	f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<tmx version=\"1.4\">\n\t<header segtype=\"sentence\" adminlang=\"de\" srclang=\"de\" datatype=\"xml\" creationdate=\"20170408T073750Z\">\n\t</header>\n\t<body>\n")
	
	# Just the german sentences
	g = open("outputcorpus/" + str(y) + "/" + outputname + "." + str(y) + ".de", "w")

	# Just the korean sentences
	h = open("outputcorpus/" + str(y) + "/" + outputname + "." + str(y) + ".ko", "w")

	# Let's add a few things to the info file
	i = open("outputcorpus/" + str(y) + "/info.txt","a")

	# Preparing an excel spreadsheet
	# The way we write Excel worksheets appends information and doesn't rewrite it when you run this script a second time. So we delete the previous result
	if not os.path.exists("outputcorpus/" + str(y) + "/tedcorpus." + str(y) + "xlsx"):
    	os.remove("outputcorpus/" + str(y) + "/tedcorpus." + str(y) + "xlsx")
	exceldata = [['ID', 'German', 'Korean']]

	# Looping through each sentence in the TED talk
	for x in range(len(de_sens)):

		# Printing to each individual ted talk
		f.write("\t\t<tu tuid=\"" + str(x+1) + "\">\n\t\t\t<tuv xml:lang=\"de\">\n\t\t\t\t<seg>" + de_sens[x] + "</seg>\n\t\t\t</tuv>\n\t\t\t<tuv xml:lang=\"ko\">\n\t\t\t\t<seg>" + ko_sens[x] + "</seg>\n\t\t\t</tuv>\n\t\t</tu>\n")
		g.write(de_sens[x] + "\n")
		h.write(ko_sens[x] + "\n")
		exceldata.append([str(x+1),de_sens[x],ko_sens[x]])

		# Printing to the whole corpus
		k.write(de_sens[x] + "\n")
		l.write(ko_sens[x] + "\n")
		j.write("\t\t<tu tuid=\"" + str(x+1) + "\">\n\t\t\t<tuv xml:lang=\"de\">\n\t\t\t\t<seg>" + de_sens[x] + "</seg>\n\t\t\t</tuv>\n\t\t\t<tuv xml:lang=\"ko\">\n\t\t\t\t<seg>" + ko_sens[x] + "</seg>\n\t\t\t</tuv>\n\t\t</tu>\n")
		totalexceldata.append([str(x+1),de_sens[x],ko_sens[x]])

		count += 1

	f.write("\t</body>\n</tmx>")
	i.write("\nNumber of aligned sentences: " + str(len(de_sens)))

	f.close(), g.close(), h.close(), i.close()

	# This prints the corpus to the excel spreadsheet
	row, col = 0, 0
	workbook = xlsxwriter.Workbook("outputcorpus/" + str(y) + "/" + outputname + "." + str(y) + ".xlsx")
	worksheet = workbook.add_worksheet()
	for tuid, de, ko in exceldata:
		worksheet.write(row, col, tuid)
		worksheet.write(row, col + 1, de)
		worksheet.write(row, col + 2, ko)
		row += 1
	workbook.close()

	# Keeps track of how long it takes
	if y%100==0:
		print(str(y) + " ted talks already done")

j.write("\t</body>\n</tmx>")
m.write("Total combined TED talk corpus\nNumber of sentences: " + str(count))

row, col = 0, 0
workbook = xlsxwriter.Workbook("outputcorpus/tedcorpus.total.xlsx")
worksheet = workbook.add_worksheet()
for tuid, de, ko in exceldata:
	worksheet.write(row, col, tuid)
	worksheet.write(row, col + 1, de)
	worksheet.write(row, col + 2, ko)
row += 1
workbook.close()

j.close(), k.close(), l.close(), m.close()
