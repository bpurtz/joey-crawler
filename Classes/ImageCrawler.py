import requests    
import re    
from urllib.parse import urlparse    
import os
import html
from bs4 import BeautifulSoup

BAD_VISIT_LIMIT = 50

class ImageCrawler:
    def __init__(self, starting_url, transformer, dataLimitCount, recursionLimit, verify_links, onComplete, add_visited_link):
      # function that transforms html and returns a set of desired data
      self.transformer = transformer
      # url to be visited first
      self.starting_url = starting_url
      # The maximum number of data entries
      self.dataLimitCount = dataLimitCount
      # The maximum number of sites visited
      self.recursionLimit = recursionLimit
      # The current number of sites visited
      self.recursionCount = 0
      # set of visited sites
      self.visited = set()
      # set of sites to visit
      self.toBeVisited = set()
      # data returned from transformer
      self.data = set()
      # function returns list of verified links
      self.verify_links = verify_links
      # function is called with final data upon agent completion
      self.onComplete = onComplete
      self.add_visited_link = add_visited_link
        
    def start(self, badVisited = 0, url=''):
      destination = self.starting_url if len(url) == 0 else url
      if ((self.recursionCount < self.recursionLimit) and (len(self.data) < self.dataLimitCount) and (destination not in self.visited)):
        print(f'Going to: {destination}')
        self.visited.add(destination)
        self.add_visited_link(destination)
        raw = None
        try:
          raw = requests.get(destination)
        except:
          print(f'Broken link: {url}')
        if (raw):
          raw = raw.text
          bs_obj = BeautifulSoup(raw)

          transformed = self.transformer(bs_obj)
          if (len(transformed) == 0 and (badVisited > BAD_VISIT_LIMIT)):
            print(f'Stopping Crawler due to bad visits {badVisited}')
            self.onComplete(self.data)
            return

          self.data = self.data.union(transformed)
          links = self.getLinks(bs_obj)
          refined_links = self.verify_links(links)
          if (len(refined_links) == 0):
            print(f'Stopping Crawler due to no unique links')
            self.onComplete(self.data)
          for x in refined_links:
            self.start(0 if len(transformed) > 0 else badVisited+1, x)
      else:
        print(f'Stopping work with COUNT: {self.recursionCount} and DATA: {len(self.data)}')
        self.onComplete(self.data)

    # Working
    def getLinks(self, bs_obj):
      try:
        hrefs = map(lambda x: x.attrs.get('href', '') if x.attrs else '', bs_obj.find_all('a'))
      except:
        print('Encountered Error')
      sourcesRefined = set()
      for x in hrefs:
        b = re.search('http[^"]*', x)
        if (b):
          c = b.group()
          # Remove stupid google thing if exists
          gString = re.search('.*?&sa', c)
          if (gString != None):
            c = gString.group()[:-3]
            sourcesRefined.add(c)
      return sourcesRefined
