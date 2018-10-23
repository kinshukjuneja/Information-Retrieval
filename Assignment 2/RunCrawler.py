import urllib.request
import re
from collections import deque
from sys import getsizeof
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import os

# Initialization of the global members used for computation
BASE_URL = "https://en.wikipedia.org"
# Regex pattern used for searching the pattern in the text obtained
PATTERN = "href=\"(/wiki.*?)\""
# total file size used for defining the size of the files appended later in the program
total_fize_size = []
folder_path = "crawled_files"

if not os.path.isdir(folder_path):
    os.mkdir(folder_path)

# class named as RunCrawler
class RunCrawler:

    # Initialization of the object
    def __init__(self, seed_url, max_num_pages=900, max_depth=5, delay=1, urls_crawled=[]):
        # default seed URL
        self.seed_url = seed_url
        # default number of pages to crawl
        self.max_num_pages = max_num_pages
        # max depth that can be reached
        self.max_depth = max_depth
        # delay to add between each request for politness policy
        self.delay = delay
        # list of urls crawled which will be appended later in the program
        self.urls_crawled = set(urls_crawled)

    def getURLsCrawled(self, file_name):
        """
        Opens a new file and writes the URLS that were crawled by iterating on the self object's
        urls_crawled list
        """
        file = open(file_name, "w")
        for URL in self.urls_crawled:
            file.write(URL + "\n")
        file.close()

    def getFilesCrawled(self):
        """
        Opens a new file and writes the content if that file was crawled successfully
        """
        count = 0
        for url in self.urls_crawled:
            count += 1
            time.sleep(1)
            text = self.permitsCrawl(url)
            if text:
                total_fize_size.append(getsizeof(text))
                file = open(os.path.join(folder_path, str(count)) + '.txt', "w")
                file.write(text)
                file.close()

    def permitsCrawl(self, url):
        """
        Computes if the requested url can be crawled
        and returns the content in the form of text
        otherwise throws an exception
        """
        req = Request(url)
        try:
            response = urlopen(url)
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', req, e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', response, e.reason)
        else:
            with urllib.request.urlopen(url) as url:
                 text = str(url.read())
                 return text

    def BFS(self):
        """
        The standard Bread First Search method that takes in the crawler object and performs
        BFS level by level to compute the desired URL list.
        """
        # frontier deque used for crawling URLS initialized with seed URL at the start of the process and depth 1
        frontier = deque()
        frontier.append([self.seed_url, 1])

        # loop till frontier is not empty and till maximum page count and maximum depth is not reached
        while frontier and len(self.urls_crawled) < self.max_num_pages:
            # pop the current URL with depth
            website, depth = frontier.popleft()
            print(website)
            # add the URL to the object's list to iterate later
            self.urls_crawled.add(website)
            # break if maximum URLS crawled are 900 or maximum depth reached is 5
            if len(self.urls_crawled) >= self.max_num_pages:
                break
            if depth >= self.max_depth:
                continue

            # delay of 1 second added for politness policy
            time.sleep(self.delay)

            # get the text if the website was allowed to be crawled
            text = self.permitsCrawl(website)

            # if text is not empty
            if text:
                # append the text obtained in the global file size to compute stats
                total_fize_size.append(getsizeof(text))
                # Regex used to find the pattern in text and stored in a HashSet to get all unique ending URLS
                end_urls = set([tUrl for tUrl in re.findall(PATTERN, text) if not (tUrl.endswith('Main_Page') or ':' in tUrl)])
                # loop for each ending URL from set
                for end_url in end_urls:
                    # use the BASE_URL to concatenate and form the complete valid URL
                    url_crawled = BASE_URL + end_url
                    # add the URL to the frontier deque for next cycle if not already present
                    # in object's url_crawled set and increment the current depth reached here
                    if url_crawled not in self.urls_crawled:
                        frontier.append([url_crawled, depth + 1])

            # get the statistics and store them in the file "stats.txt"
            self.getStats("stats.txt", depth)


    def getStats(self, file_name, curr_depth):
        """
        Computes the statistics of result obtained from file size
        and writes them into the file name specified as first argument
        The max depth argument is used to compute the maximum depth reached
        """
        file = open(file_name, "w")
        file.write(self.getMaxSize(total_fize_size))
        file.write(self.getMinSize(total_fize_size))
        file.write(self.getAverage(total_fize_size))
        file.write(self.getMaxDepth(curr_depth))
        file.close()



    def getMaxSize(self, total_file_size):
        """
        max(iterable, *[, default=obj, key=func]) -> value
        max(arg1, arg2, *args, *[, key=func]) -> value

        With a single iterable argument, return its biggest item. The
        default keyword-only argument specifies an object to return if
        the provided iterable is empty.
        With two or more arguments, return the largest argument.
        """
        return ("Maximum Size: " + str(max(total_file_size)) + " bytes" + '\n')

    def getMinSize(self, total_file_size):
        """
        min(iterable, *[, default=obj, key=func]) -> value
        min(arg1, arg2, *args, *[, key=func]) -> value

        With a single iterable argument, return its smallest item. The
        default keyword-only argument specifies an object to return if
        the provided iterable is empty.
        With two or more arguments, return the smallest argument.
        """
        return "Minimum Size: " + str(min(total_file_size)) + " bytes" + '\n'

    def getAverage(self, total_fize_size):
        """
        Return the sum of a 'start' value (default: 0) plus an iterable of numbers

        When the iterable is empty, return the start value.
        This function is intended specifically for use with numeric values and may
        reject non-numeric types.
        """
        return "Average size: " + str(sum(total_fize_size) / (len(total_fize_size))) + " bytes" + '\n'

    def getMaxDepth(self, curr_depth):
        """
        Return the maximum depth by looking at the first element of the deque

        When the iterable is empty, return the start value.
        This function is intended specifically for use with numeric values and may
        reject non-numeric types.
        """
        return "Maximum depth reach: " + str(curr_depth)

if __name__ == "__main__":
    seed_url = input("Please enter a single seed URL: ")
    max_num_pages = (int(input("Please enter maximum number of pages to be crawled: ")))

    if not seed_url:
        seed_url = BASE_URL
    if not max_num_pages:
        max_num_pages = 900

    crawler = RunCrawler(seed_url, max_num_pages)

    crawler.BFS()

    crawler.getURLsCrawled("URLsCrawled.txt")

    crawler.getFilesCrawled()