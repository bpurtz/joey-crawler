import requests    
import re    
from urllib.parse import urlparse    
import os
import html

class ImageCrawler:
    def __init__(self, starting_url, transformer, dataLimitCount, recursionLimit):
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
        
    def start(self, badVisited = 0, url=''):
      print(f'Starting at: {url}')
      if (not (self.recursionCount > self.recursionLimit | len(self.data) > self.dataLimitCount | url in self.visited)):
        raw = requests.get(self.starting_url if len(url) == 0 else url)
        raw = raw.text
        htmlString = html.unescape(raw)
        transformed = self.transformer(htmlString)
        if (len(transformed) == 0 & badVisited > 10):
          return

        self.data = self.data.union(transformed)
        links = self.getLinks(htmlString)
        for x in links:
          self.start(0 if len(transformed) > 0 else badVisited+1, x)

    def getLinks(self, text):
      text = html.unescape(text)
      aTags = re.findall('<a[^<]*</a>', text)
      print(f'TAGS: {len(set(aTags))}')
      sourcesRaw = map(lambda x: re.search('href="[^"]*"', x), aTags)
      print(sourcesRaw)
      sourcesMid = set()
      sourcesRefined = set()
      print(sourcesRaw)
      for x in sourcesRaw:
          a = x.group()
          sourcesMid.add(a)
      print(sourcesMid)
      for x in sourcesMid:
          a = x[6:-1]
          sourcesRefined.add(a)
      print(f'Links found: {sourcesRefined}')
      return sourcesRefined