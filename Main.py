from Classes import CrawlerController
import re



def main():
  ic = CrawlerController()
  ic.start()
  print(ic.data)

if __name__ == "__main__":
  main()
