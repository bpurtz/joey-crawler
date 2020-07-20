import requests    
import re    
from urllib.parse import urlparse    
import os
import html
from bs4 import BeautifulSoup
import ImageCrawler

"""
Crawlers don't visit same links as other agents.
Multiple instances of ImageCrawler
change imagecrawler class: passing in a function
new links-> call function. returns unique links
"""

NUM_CRAWLERS = 5

class CrawlerController:
  def __init__(self):
	  self.visited = set()
	  self.staring_url = "https://www.google.com/search?ei=eiYVX9fSFY6-0PEPpbaBmAk&q=modly+buds&oq=modly+buds&gs_lcp=CgZwc3ktYWIQAzIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQR1DdtxpYmcIaYJXDGmgAcAR4AIABAIgBAJIBAJgBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwjX94HTh9vqAhUOHzQIHSVbAJMQ4dUDCAw&uact=5"
	  self.image_crawlers = []
	  
	def verify_links(self, link_list):
		if self.visited.len() == 0:
			self.visited = self.visited.union(link_list)
			return link_list
		else: 
			unique_urls = filter(lambda x: x not in self.visted, link_list)
		  self.visited = self.visited.union(unique_urls)
		  return unique_urls
	
	def get_new_links(self, bs_obj):
		try:
			links = filter(lambda x: re.search("Page \d+", x.attrs.get('aria-label','')), bs_obj.findall('a')
			new_links = map(lambda x: "https://google.com"+x.attrs.get('href', '') if x.attrs else '', links)
		except:
			print('Encountered Error')
		return new_links
		
	def get_last_link(self, bs_tags):
		selected = None
		selected_num = -1
		for tag in bs_tags:
			label = tag.attrs.get('aria-label','')
			num = re.find("\d+", label)
			if num & x = num.group(0) > selected_num:
			 selected = tag.attrs.get('href','')
			 selected_num = x
		return selected	
		
	def transformer(bs_obj):
		sources = map(lambda x: x.attrs.get('src', '') if x.attrs else '', bs_obj.find_all('img'))
		sourcesRefined = set(filter(lambda x: re.search("https", x) != None, sources))
		print(f'Images found: {sourcesRefined}')
		return sourcesRefined
		
	def start(self):
		html = request.get(self.starting_url)
		html = html.text
		raw = BeautifulSoup(html)
		links = get_new_links(raw)
		link_strings = set(self.starting_url, map(lambda x: x.attrs.get('href',''), links))
		last_link = get_last_link(links)

		while len(link_strings) < NUM_CRAWLERS:
			new_html = request.get(last_link).text
			bs_obj = BeautifulSoup(new_html)
			new_links = get_new_links(bs_obj)
			last_link = get_last_link(new_links)
			link_strings = link_strings.union(set(map(lambda x: x.attrs.get('href',''), links)))
			links = links + new_links
		counter = 0
		for x in link_strings:
			if counter > NUM_CRAWLERS:
				break
			counter++
			#(self, starting_url, transformer, dataLimitCount, recursionLimit, verify_links):
			self.image_crawlers.append(ImageCrawler(x, self.transformer, 20, 20, self.verify_links)
		return 1
			 
			
			
			
			
			
		

	


	 

  
