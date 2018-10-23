i. What was the most difficult part of this assignment?


Figuring our the regular expression to extract the ending URLS from the text obtained took most of my time.
The following website was useful in getting started with Regex:
https://regex101.com

ii. Optional: Any additional information you may wish to provide about running the script RunCrawler.

	Python3 must be installed and the following libraries are used:
	import urllib.request
	import re
	from collections import deque
	from sys import getsizeof
	import time
	from urllib.request import Request, urlopen
	from urllib.error import HTTPError, URLError
	
	To run the script and generate the output, go to the directory where RunCrawler.py is stored 
	and execute by calling "python RunCrawler.py" or run directly from your favorite IDE like Pycharm.
	It takes the seed_url and number of pages to be crawled as input during runtime.