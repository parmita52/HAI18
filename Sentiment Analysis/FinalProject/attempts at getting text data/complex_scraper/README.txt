-------------------------
README File For RateProf-Scrape
-------------------------
Karthik Raman

Version 1.0
31/08/2012

http://www.cs.cornell.edu/~karthik/projects/rateprof-scrape/index.html


-------------------------
INTRODUCTION
-------------------------

RateProf-Scrape is a python class for scraping reviews about professors from a certain university from ratemyprofessors.com. This includes both aggregate information as well as detailed review scores (along the 4 different axis the website provides)

Does this in the following steps:
Step 1: Get the list of professors starting with each letter
Step 2: Get the list of all reviews for that professor.
Step 3: Get each review from that list.

It also has the ability to be interrupted and (effectively) resume from where it stopped without having to redownload all the previous files. It does this by performs optimizations such as storing the webpages it has downloaded and compacting the downloaded pages into a format that is easy to process.

Note that no Personal Information of the reviewers such as their account name or address is scraped..

-------------------------
COMPILING
-------------------------

RateProf-Scrape can works in Windows, Linux and Mac environment.

**NOTE**
RateProf-Scrape does require Python version 2.7 or newer in order to run properly.

You can download the latest version of Python at http://www.python.org/download/

-------------------------
INSTALLATION
-------------------------

If you want to install this module in your directory for third-party Python modules then run

python setup.py install

-------------------------
RUNNING
-------------------------

To run the function 

Usage:
  scrapeRateProfs.py [-h] -sid SchoolID [-delay DELAY] -o OUTPUT -path PATH

Inputs:
  -h, --help      show this help message and exit
  -sid SchoolID   ID of the school on RateMyProf
  -delay DELAY    Amount of time to pause after downloading a website
  -o OUTPUT       Path to output file for reviews
  -path PATH      Directory where the webpages should be downloaded

-------------------------
INPUT DATA FORMAT
-------------------------

The function takes in input via the command line as mentioned above. 
The key input is the school id on ratemyprofessors.com.
For example, reviews for faculty from Cornell University are found at http://www.ratemyprofessors.com/SelectTeacher.jsp?sid=298.
Thus Cornell university has the sid of "298"

Simply provided with this, the code will work for any institution having review information available on the ratemyprofessors.com website.


-------------------------
OUTPUT DATA FORMAT
-------------------------
The code produces 2 key TSV output files.

a) The ".aggreg" file is an aggregate file, containing the aggregate information for each different faculty. The file will be sorted alphabetically as per last name (though some faculty for whom there are no reviews will have their last names presented before their first names)

Format: Index	Name	Total # Of Reviews	Department	Average Quality	Average Helpfullness	Average Clarity	Average Easiness

b) The ".review" file contains all the individual reviews for each different faculty. The file is ordered datewise for each faculty (with the faculty being sorted alphabetically by last name as before). The format it follows is: 

ReviewIndex	Faculty Name	Faculty Dept.	Review ID for this faculty	Review Date	Class for which Review was written	Quality Rating	Helpfullnes Rating	Clarity Rating	Easiness Rating	Reviewer Interest	Review Text 

Note that Review-Text may have the windows newline characters (seen as Ctrl+M in vim). These can easily be replaced within vim/using sed or other similar tools.

-------------------------
CONTENTS
-------------------------

The source distribution includes the following files:

1. README.txt : This readme file.
2. LICENSE.txt : License under which software is released.
3. scrapeRateProfs.py : The python module.
4. setup.py : The setup file
5. DOCUMENTATION.html : The file containing detailed documentation of the code.

There is also a windows binary .exe file available (untested though).

-------------------------
SAMPLE USAGE
-------------------------

To run for Cornell University with delay 2, with output files having prefix CornellU.tsv and with intermediate files written into the WebPages directory:

python scrapeRateProfs.py -sid 298 -path WebPages/ -o CornellU.tsv -delay 2


-------------------------
FURTHER DOCUMENTATION
-------------------------

Please see the html file for Documentation about the different functions.

