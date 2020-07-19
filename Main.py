from Classes import ImageCrawler
import re

def transformer(htmlText):
  imageTags = re.findall('<img[^>]*>', htmlText)
  sourcesRaw = map(lambda x: re.search('src="[^"]*"', x), imageTags)
  sourcesMid = []
  sourcesRefined = []
  for x in sourcesRaw:
      a = x.group()
      sourcesMid.append(a)
  # print(sourcesMid)
  for x in sourcesMid:
      a = x[5:-1]
      sourcesRefined.append(a)
  sourcesRefined = filter(lambda x: re.search("https", x) != None, sourcesRefined)
  sourcesRefined = set(sourcesRefined)
  # print(f'FOUND {sourcesRefined}')
  return sourcesRefined

def main():
  ic = ImageCrawler("https://www.google.com/search?q=moldy+buds&oq=moldy+buds&aqs=chrome.0.69i59l2j0l5j69i60.3027j1j4&sourceid=chrome&ie=UTF-8", transformer, 20, 20)
  print("hello")
  ic.start()
  print(ic.data)

if __name__ == "__main__":
  main()