from Classes import ImageCrawler
import re

def transformer(bs_obj):
  sources = map(lambda x: x.attrs.get('src', '') if x.attrs else '', bs_obj.find_all('img'))
  sourcesRefined = set(filter(lambda x: re.search("https", x) != None, sources))
  print(f'Images found: {sourcesRefined}')
  return sourcesRefined

def main():
  ic = ImageCrawler("https://www.google.com/search?q=moldy+buds&oq=moldy+buds&aqs=chrome.0.69i59l2j0l5j69i60.7018j1j7&sourceid=chrome&ie=UTF-8", transformer, 20, 20)
  ic.start()
  print(ic.data)

if __name__ == "__main__":
  main()