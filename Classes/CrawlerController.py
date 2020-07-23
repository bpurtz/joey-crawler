import requests    
import re    
from urllib.parse import urlparse    
import os
import html
from bs4 import BeautifulSoup
from . import ImageCrawler
import sys

"""
Crawlers don't visit same links as other agents.
Multiple instances of ImageCrawler
change imagecrawler class: passing in a function
new links-> call function. returns unique links
"""

NUM_CRAWLERS = 10

firstRegexes = [
  "bud",
  "cannabis",
  "marijuana",
  "mj",
  "ganja",
  "hemp",
  "flower",
  "bud rot",
  "crop",
  "weed"
]

secondRegexes = [
  "rot",
  "mold",
  "moldy",
  "bud",
  "mould"
]

# Function to filter out images not associated with mold
def filterMoldImages(bs_image_tag):
  attrs = bs_image_tag.attrs
  accepted = False
  for key, value in attrs.items():
    if (key == 'href'):
      continue
    if (isinstance(value, str)):
      for y in firstRegexes:
        firstPass = re.search(y, value, re.IGNORECASE)
        if (firstPass != None):
          for z in secondRegexes:
            secondPass = re.search(z, value, re.IGNORECASE)
            if (secondPass != None):
              accepted = True
    return accepted

class CrawlerController:
  def __init__(self):
    self.visited = set()
    self.starting_url = "https://www.google.com/search?ei=eiYVX9fSFY6-0PEPpbaBmAk&q=modly+buds&oq=modly+buds&gs_lcp=CgZwc3ktYWIQAzIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQR1DdtxpYmcIaYJXDGmgAcAR4AIABAIgBAJIBAJgBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwjX94HTh9vqAhUOHzQIHSVbAJMQ4dUDCAw&uact=5"
    self.image_crawlers = []
    self.data = set()
	  
  def add_visited_link(self, link):
    print(f'Adding link: {link}')
    self.visited.add(link)

  def verify_links(self, link_list):
    unique_urls = filter(lambda x: x not in self.visited, link_list)
    return list(unique_urls)
    
  def get_next_link(self, bs_obj):
    link = ''
    try:
      links = filter(lambda x: re.search("Next page", x.attrs.get('aria-label','')), bs_obj.find_all('a'))
      new_links = map(lambda x: "https://google.com"+x.attrs.get('href', '') if x.attrs else '', links)
      for x in new_links:
        link = x
        break
    except:
      print('Encountered Error')
    return link
    
  def transformer(self, bs_obj):
    sources = bs_obj.find_all('img')
    filteredSources = list(filter(filterMoldImages, sources))
    sourceStrings = map(lambda x: x.attrs.get('src', '') if x.attrs else '', filteredSources)
    sourcesRefined = set(filter(lambda x: re.search("https", x) != None, sourceStrings))
    print(f'Images found: {sourcesRefined}')
    return sourcesRefined

  def agentComplete(self, data):
    self.data = self.data.union(data)

  def printData(self):
    print(f'Length of data: {len(list(self.data))}')
    print(f'Data: {self.data}')
    
  def start(self):
    html = requests.get(self.starting_url)
    html = html.text
    raw = BeautifulSoup(html)
    next_link = self.get_next_link(raw)
    links = set([self.starting_url])
    while(len(links) < NUM_CRAWLERS):
      # Get next page
      newHtml = requests.get(next_link)
      newRaw = BeautifulSoup(newHtml.text)
      # Get next link
      next_link = self.get_next_link(newRaw)
      # Add link to links
      links.add(next_link)
    for x in links:
      c = ImageCrawler(x, self.transformer, 80, 1000, self.verify_links, self.agentComplete, self.add_visited_link)
      c.start()
      self.image_crawlers.append(c)
    