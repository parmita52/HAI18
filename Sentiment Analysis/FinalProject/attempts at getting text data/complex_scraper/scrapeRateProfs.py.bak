"""Python Module for scraping reviews from RateMyProfessor.

This module scrapes reviews about professors from a certain university from ratemyprofessor.com.

Does this in the following steps:
Step 1: Get the list of professors starting with each letter
Step 2: Get the list of all reviews for that professor.
Step 3: Get each review from that list.

It also has the ability to be interrupted and (effectively) resume from where it stopped without having to redownload all the previous files. It does this by performs optimizations such as storing the webpages it has downloaded and compacting the downloaded pages into a format that is easy to process.

Usage:
  scrapeRateProfs.py [-h] -sid SchoolID [-delay DELAY] -o OUTPUT -path PATH

Inputs:
  -h, --help      show this help message and exit
  -sid SchoolID   ID of the school on RateMyProf
  -delay DELAY    Amount of time to pause after downloading a website
  -o OUTPUT       Path to output file for reviews
  -path PATH      Directory where the webpages should be downloaded

Key Outputs:
  - TSV File containing the review information.
  - TSV File containing the aggregate information for a professor.
  - Condensed set of information downloaded
  
Formats are provided in the accompanying README  
"""

import argparse
import urllib2
import sys
import time
import os
import bisect

#Set the global variables
path = '/home/karthik/Desktop/Scraping/Hotels/WebPages'
delayTime = 1
baseUrl = "http://www.ratemyprofessors.com/"
outAggFile = None
outRevFile = None
totReviews = 0
totReviews2 = 0	#Using the NumReviews field
totProfs = 0
totProfsEmpty = 0
outAggFile = None
outRevFile = None

def getFileContentFromWeb(url):
	"""Downloads data from a website
	
	Inputs:
	- url : Url to be downloaded
	
	Returns:
	- Content of url
	
	"""
	time.sleep(delayTime)
	response = urllib2.urlopen(url)	
	return response.read()

def downloadToFile(url, fileName, force = False):  
	"""Downloads url to file
	
	Inputs:
	- url : Url to be downloaded
	- fileName : Name of the file to write to
	- force : Optional boolean argument which if true will overwrite the file even it it exists
	
	Returns:
	- Pair indicating if the file was downloaded and a list of the contents of the file split up line-by-line
	
	"""  
	
	fullFileName = path+'/'+ fileName.replace("/","\\/")
	downloaded = False
	if not force and os.path.exists(fullFileName):
		print "Reading file: ", fileName
		thisFile = open(fullFileName)
		fileContents = thisFile.read()
		thisFile.close()
	else:
		print "Downloading URL : ", url, " to file: ", fullFileName
		fileContents = getFileContentFromWeb(url)
		output = open(fullFileName, 'w')
		output.write(fileContents)
		output.close()
		downloaded = True
	return (fileContents.split("\n"), downloaded)

def pruneProfListFile(plContents, fileName):
	"""Prunes the professor list file contents from the entire website to only what is required
	
		
	Inputs:
	- plContents : Contents of the Professor List webpage
	- filename   : Name of the file to write the output to
	
	Returns:
	- Pruned content from the list page containing only information about the links to each individual professor's review page"""  
	
	print "Pruning professor list page"
	startS = "<div class=\"profName\">"
	pruneContent = []
	i = 0
	while i < len(plContents):
		line = plContents[i]
		i+=1
		foundV = line.find(startS)
		if foundV != -1:	#Add the line containing the number
			lineContent = line[foundV + len(startS):]
			pruneContent.append( lineContent )
			
	with open(path+'/'+ fileName.replace("/","\\/"),'w') as outF:
		for line in pruneContent:
			outF.write(line+'\n')
			
	print "Professor list pruned to ", len(pruneContent)," lines from ", len(plContents)," lines"
	return pruneContent
	
def getLinksFromList(plContents):
	"""Extracts the links for the individual review pages of each professor
	
	Inputs:
	- plContents : Pruned contents of the professor list file.
	
	Returns:
	- Triplet containing 3 arrays, one for the professor names, the link to their review page and a boolean flag indicating if they have any reviews"""  
	
	print "Extracting individual professor's review pages"
	startS1 = "<a href=\""
	endS1 = "\">"
	endS2 = "</a>"
	profUrl = []
	profName = []
	profEmpty = []
	
	for line in plContents:
		line = line.strip()
		if len(line) < 2:
			continue
	  
		ind1 = line.find(startS1)
		line = line[ind1 + len(startS1):]
		
		ind2 = line.find(endS1)
		url = line[:ind2]
		
		line = line[ind2+len(endS1):]
		name = line[:line.find(endS2)]
		
		empty = False
		if url.find("AddRating") != -1:
			empty = True
		
		profUrl.append(url)
		profName.append(name)
		profEmpty.append(empty)
		
	print "Found ", len(profName)," professors"
	return (profUrl, profName, profEmpty)

def pruneProfReviewFile(prContents, fileName):
	"""Prunes the review page for a particular professor to only what is required namely the stats and the reviews
	
	Inputs:
	- prContents : Contents of the review webpage for a particular professor
	- filename   : Name of the file to write the output to
	
	Returns:
	- Pruned contents of the review page, which includes aggregate details of all reviews, as well as all individual reviews."""  

	print "Pruning review  page"
	nameStartS = "<h2 id=\"profName\""	#e.g. <h2 id="profName" style="color:black;">Salam&nbsp;Abdus</h2>
	deptStartS = "<li>Department: <strong>"
	qualityStartS = "title=\"Overall Quality is determined by the average rating of the Helpfulness and Clarity given by all users.\""	
	helpfulStartS = "title=\"Is this professor approachable, nice and easy to communicate with? How accessible is the professor and is he/she available during office hours or after class for additional help?\""
	clarityStartS = "title=\"How well does the professor teach the course material? Were you able to understand the class topics based on the professor's teaching methods and style?\""	
	easyStartS = "title=\"Is this class an easy A? How much work do you need to do in order to get a good grade?  Please note this category is NOT included in the"
	numRatStartS = "<p><span id=\"rateNumber\">Number of ratings <strong>"
	dateStartS = "<div class=\"date\">"
	clasStartS = "<div class=\"class\">"
	ratingStartS = "<div class=\"rating\">"
	commentStartS = "<p class=\"commentText\">"
	revqS = "Quality</p>"
	reveStartS = "<p class=\"rEasy status"
	revhStartS = "<p class=\"rHelpful status"
	revcStartS = "<p class=\"rClarity status"
	reviStartS = "<p class=\"rInterest status"
	
	
	pruneContent = []
	numReviewsSoFar = -1
	insideReview = False
	insideRating = False
	
	#Global properties
	name = ""
	dept = ""
	quality = ""
	helpful = ""
	clarity = ""
	easy = ""
	nr = ""
	
	#Properties of each review
	date = ""
	clas = ""
	comment = ""
	revQ = ""
	revH = ""
	revC = ""
	revE = ""
	revI = ""
	
	for line in prContents:
		if numReviewsSoFar == -1:	#Look for aggregate statistics only when reviews have not started
			nameInd = line.find(nameStartS)
			if nameInd != -1:	#Add the line containing the name
				lineContent = line[ line.find(">", nameInd + len(nameStartS)) + len(">"):]
				name = lineContent[:lineContent.find("</h2>")].replace("&nbsp;", " ")
				continue

			deptInd = line.find(deptStartS)
			if deptInd != -1:	#Add the line containing the name
				lineContent = line[ deptInd + len(deptStartS):]
				dept = lineContent[:lineContent.find("</strong>")].replace("&nbsp;", " ")
				continue				
				
			qualityInd = line.find(qualityStartS)
			if qualityInd != -1:	#Add the line containing the quality
				lineContent = line[ line.find("><strong>", qualityInd + len(qualityStartS)) + len("><strong>"):]
				quality =  lineContent[:lineContent.find("</strong>")]
				continue
				
			helpfulInd = line.find(helpfulStartS)
			if helpfulInd != -1:	#Add the line containing the helpful
				lineContent = line[ line.find("><strong>", helpfulInd + len(helpfulStartS)) + len("><strong>"):]
				helpful =  lineContent[:lineContent.find("</strong>")]
				continue
	
			clarityInd = line.find(clarityStartS)
			if clarityInd != -1:	#Add the line containing the clarity
				lineContent = line[ line.find("><strong>", clarityInd + len(clarityStartS)) + len("><strong>"):]
				clarity =  lineContent[:lineContent.find("</strong>")]
				continue
				
			easyInd = line.find(easyStartS)
			if easyInd != -1:	#Add the line containing the easiness
				lineContent = line[ line.find("><strong>", easyInd + len(easyStartS)) + len("><strong>"):]
				easy =  lineContent[:lineContent.find("</strong>")]
				continue
			      
			nrInd = line.find(numRatStartS)
			if nrInd != -1:	#Add the line containing the number of ratings
				lineContent = line[ nrInd + len(numRatStartS):]
				nr =  lineContent[:lineContent.find("</strong>")]
				continue   
			      
			dateInd = line.find(dateStartS)
			if dateInd != -1:	#Indicate that the reviews are starting
				numReviewsSoFar += 1
				pruneContent.append( "Name:"+name )
				pruneContent.append( "Dept:"+dept )
				pruneContent.append( "Quality:"+quality )
				pruneContent.append( "Helpful:"+helpful )
				pruneContent.append( "Clarity:"+clarity )
				pruneContent.append( "Easy:"+easy )
				pruneContent.append( "NR:"+nr )
				continue
		elif not insideReview:
			dateInd = line.find(dateStartS)
			if dateInd != -1:	#Add the line containing the date
				lineContent = line[ dateInd + len(dateStartS) : ]
				date =  lineContent[:lineContent.find("</div>")]
				
				numReviewsSoFar += 1
				insideReview = True
				
				clas = ""
				comment = ""
				revQ = ""
				revH = ""
				revC = ""
				revE = ""
				revI = ""
				
				continue
		elif not insideRating:
			clasInd = line.find(clasStartS)
			if clasInd != -1:	#Add the line containing the class
				lineContent = line[ clasInd + len(clasStartS) : ]
				clas =  lineContent[:lineContent.find("</div>")]
				continue
			      
			if line.find(ratingStartS)!= -1:	#Signal that you are entering a rating
				insideRating = True
				
			commentInd = line.find(commentStartS)
			if commentInd != -1:	#Add the line containing the comment
				lineContent = line[ commentInd + len(commentStartS) : ]
				comment =  lineContent[:lineContent.find("</p")]
				pruneContent.append( "Date:"+date )
				pruneContent.append( "Class:"+clas )
				pruneContent.append( "RevQ:"+revQ )
				pruneContent.append( "RevH:"+revH )
				pruneContent.append( "RevC:"+revC )
				pruneContent.append( "RevE:"+revE )
				pruneContent.append( "RevI:"+revI )
				pruneContent.append( "Comment:"+comment )
				insideReview = False	#Signal that this is the end of the review
				continue      
		else:	#Get the rating scores for the review
			if line.find(revqS)!= -1:	#Add the quality
				if line.find("Poor")!= -1:
					revQ = "Poor"
				elif line.find("Good")!= -1:
					revQ = "Good"
				else:
					revQ = "Average"
				continue
			
			reveInd = line.find(reveStartS)
			if reveInd != -1:	#Add the line containing the easiness rating of this review
				lineContent = line[ reveInd + len(reveStartS) : ]
				revE =  lineContent[:lineContent.find("\">")].replace("&nbsp;","")
				continue

			revhInd = line.find(revhStartS)
			if revhInd != -1:	#Add the line containing the helpfullness rating of this review
				lineContent = line[ revhInd + len(revhStartS) : ]
				revH =  lineContent[:lineContent.find("\">")].replace("&nbsp;","")
				continue
			      
			revcInd = line.find(revcStartS)
			if revcInd != -1:	#Add the line containing the clarity rating of this review
				lineContent = line[ revcInd + len(revcStartS) : ]
				revC =  lineContent[:lineContent.find("\">")].replace("&nbsp;","")
				continue
			      
			reviInd = line.find(reviStartS)
			if reviInd != -1:	#Add the line containing the interest rating of this review
				lineContent = line[ reviInd + len(reviStartS) : ]
				revI =  lineContent[:lineContent.find("\">")].replace("&nbsp;","")
				insideRating = False
				continue
			      
	with open(path+'/'+ fileName.replace("/","\\/"),'w') as outF:
		for line in pruneContent:
			outF.write(line+'\n')
			
	print "Professor list pruned to ", len(pruneContent)," lines from ", len(prContents)," lines"
	return pruneContent

def getReviewsForProf(rurl, rname):
	"""Gets the reviews and aggregate statistics for a specific professor.
		
	Inputs:
	- rurl : Link to the review page for a professor
	- rname: Name of the professor (this will be unique)"""
	
	global totProfs, totProfsEmpty, totReviews, totReviews2
	print "2) Getting the reviews for professor ", rname

	profUrl = baseUrl+rurl+"&all=true"
	prFileName = "profReview_name-"+rname+".html"
	(prContents, dwnld) = downloadToFile(profUrl,prFileName)

	if dwnld:	#If downloaded then prune the page	
		prContents = pruneProfReviewFile(prContents, prFileName)

	if len(prContents) < 2:
		outAggFile.write(str(totProfs) + '\t' + rname + '\t0\n')
		outAggFile.flush()
		return
	
	i = 0
	
	#First get the aggregate properties
	nameInd = prContents[i].find("Name:") + len("Name:")
	name = prContents[i][nameInd:].strip()
	i += 1

	deptInd = prContents[i].find("Dept:") + len("Dept:")
	dept = prContents[i][deptInd:].strip()
	i += 1
	
	qualityInd = prContents[i].find("Quality:") + len("Quality:")
	quality = prContents[i][qualityInd:].strip()
	i += 1

	helpfulInd = prContents[i].find("Helpful:") + len("Helpful:")
	helpful = prContents[i][helpfulInd:].strip()
	i += 1
	
	clarityInd = prContents[i].find("Clarity:") + len("Clarity:")
	clarity = prContents[i][clarityInd:].strip()
	i += 1
	
	easyInd = prContents[i].find("Easy:") + len("Easy:")
	easy = prContents[i][easyInd:].strip()
	i += 1

	nrInd = prContents[i].find("NR:") + len("NR:")
	nr = prContents[i][nrInd:].strip()
	if len(nr) > 0: totReviews2 += int(nr)
	i += 1
	
	outAggFile.write(str(totProfs) + '\t' + name + '\t' + nr + '\t' + dept + '\t' + quality + '\t' + helpful + '\t' + clarity +'\t' + easy + '\n')
	outAggFile.flush()
	
	thisRev = 0
	while i < len(prContents):	#Read the individual reviews
		prContents[i] = prContents[i].strip()
		if len(prContents[i]) < 2:
			break
		
		dateInd = prContents[i].find("Date:") + len("Date:")
		date = prContents[i][dateInd:].strip()
		i += 1

		clasInd = prContents[i].find("Class:") + len("Class:")
		clas = prContents[i][clasInd:].strip()
		i += 1
		
		revQInd = prContents[i].find("RevQ:") + len("RevQ:")
		revQ = prContents[i][revQInd:].strip()
		i += 1		
		
		revHInd = prContents[i].find("RevH:") + len("RevH:")
		revH = prContents[i][revHInd:].strip()
		i += 1	
				
		revCInd = prContents[i].find("RevC:") + len("RevC:")
		revC = prContents[i][revCInd:].strip()
		i += 1	
			
		revEInd = prContents[i].find("RevE:") + len("RevE:")
		revE = prContents[i][revEInd:].strip()
		i += 1	
			
		revIInd = prContents[i].find("RevI:") + len("RevI:")
		revI = prContents[i][revIInd:].strip()
		i += 1	
			
		commentInd = prContents[i].find("Comment:") + len("Comment:")
		comment = prContents[i][commentInd:].strip()
		i += 1	
		
		totReviews += 1
		thisRev += 1
		outRevFile.write(str(totReviews) + '\t' + name + '\t' + dept + '\t' + str(thisRev) + '\t' + date + '\t' + clas + '\t' + revQ + '\t' + revH + '\t' + revC + '\t' + revE +'\t' + revI + '\t' + comment + '\n')
		outRevFile.flush()
		
	print "***Total number of profs so far: ", totProfs," having ", totReviews, "|", totReviews2, "reviews (with ", totProfsEmpty," having no reviews)"
		
def getAllReviews(sid, outF):
	"""The main function to get all the reviews from a school."""
	
	global totProfs, totProfsEmpty, totReviews, outAggFile, outRevFile
	
	outAggFile =  open(outF+'.aggreg','w')
	outRevFile =  open(outF+'.reviews','w')
	for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
		#Step 1: Get all the professors for a particular letter
		print "1) Getting the professors for ", letter
		
		profListUrl = baseUrl+"SelectTeacher.jsp?sid="+sid+"&letter="+letter
		plFileName = "profList_sid-"+sid+"_letter-"+letter+".html"
		(plContents, dwnld) = downloadToFile(profListUrl,plFileName)

		if dwnld:	#If downloaded then prune the page
			plContents = pruneProfListFile(plContents, plFileName)
			if len(plContents) < 2:
				continue
				
		(profUrl, profName, profEmpty) = getLinksFromList(plContents)
		
		prevName = ""
		count = 1
		for ind in range( len( profUrl) ):
			totProfs += 1
			if profEmpty[ind]:
				totProfsEmpty += 1
				outAggFile.write(str(totProfs) + '\t' + profName[ind] + '\t0\n')
				continue
			      
			profName[ind] = profName[ind].replace(',','-').replace(' ','')
			if profName[ind] == prevName:
				profName[ind] += "_"+str(count)
				count += 1
			else:
				prevName = profName[ind]
				count = 1
			getReviewsForProf(profUrl[ind], profName[ind])

		print "----->Total number of profs so far: ", totProfs," having ", totReviews, "|", totReviews2, "reviews (with ", totProfsEmpty," having no reviews)"

	outAggFile.close()
	outRevFile.close()
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This module scrapes reviews about professors from a certain university from ratemyprofessor.com.')
	parser.add_argument('-sid', type=str, metavar = 'SchoolID', default='298', help='ID of the school on RateMyProf.', required=True)
	parser.add_argument('-path',type=str, metavar='PATH', help='Directory where the webpages should be downloaded', required=True)
	parser.add_argument('-o', type=str, metavar='OUTPUT', help='Path to output file for reviews', required=True)
	parser.add_argument('-delay', type=int, default = 1, help='Amount of time to pause after downloading a website')
	
	args = parser.parse_args()	#Parse the command line arguments
	argVars= vars(args)
		
	#Print out the value of all the key variables read	
	schoolID = argVars['sid']
	print 'School ID = ', schoolID
	outF = argVars['o']
	print 'Output file = ', outF
	
	#Read in the other variables
	delayTime = argVars['delay']
	path = argVars['path']
	
	getAllReviews(schoolID, outF)
