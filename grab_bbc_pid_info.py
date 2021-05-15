from bs4 import BeautifulSoup as bs
import requests

class BbcPid:

  def __init__(self, _dict ):
   # title, url = get_titleUrl(soup)
    self.title = _dict['title']
    self.url = _dict['url']
    self.parent = _dict['parent_show']
    self.episode =_dict['episode']
    self.series = _dict['series']
    self.short_synop =_dict['synopShort'][0]
    self.long_synop = _dict['synopLong']

  def print(self):
    print(self.title, "\n" + 
          self.url, "\n"+
          self.parent, "\n"+
          self.episode, "\n"+
          self.series, "\n"+
          self.short_synop, "\n")
    for i in self.long_synop:
      print(i)

def get_soup(url):
  """
  Create beautiful soup object from url
  :params url: url
  :returns: Beautiful Soup
  """
  req = requests.get(url)
  soup = bs(req.content, 'html.parser')
  return soup

def extract_tag_from_soup(extractFrom, toExtract):
  """
  Take a html tag and yeet it from the soup
  :params extractFrom: soup obj to remove tag from
  :params toExtract: tag to yeet
  """
  for s in extractFrom.select(toExtract):
    s.extract()
  return

def get_titleUrl(soup):
  """
  Get title of show
  :params soup: soup obj
  :returns: title
  """
  data = soup.find('div', class_="br-masthead__title")
  link = data.find('a')
  text = link.text
  url = "https://www.bbc.co.uk" + link.get('href')
  return text, url
  
def get_episode(soup):
  data = soup.find('div', class_="gamma")
  try:
    data = data.find('span')
  except:
    data = "NULL"
  try:
    data = data.text.strip()
  except:
    data = "NULL"
  return data

def get_series(soup):
  data = soup.find('div', class_="gamma")
  try:
    data = data.find('div', class_="offset")
  except:
    date = "NA"
  try:
    data = data.find_all('a', class_="context__item")
    if len(data) == 2:
      return data[1].text
  except:
      return "NULL"

def get_parent_series(soup):
  data = soup.find('div', class_="gamma")
  try:
    data = data.find('div', class_="offset")
  except:
    date = "NA"
  try:
    data = data.find_all('a', class_="context__item")
    return data[0].find('a').find('href')
  except:
    return "NULL"

def get_short_synop(data):
  aboutShowShort = []
  short_synop = data.find('div', class_="synopsis-toggle__short" )
  for p in short_synop.find_all('p'):
    extract_tag_from_soup(p, "br")
    for pp in p:
      aboutShowShort.append(pp)
  return aboutShowShort

def get_long_synop(data):
  aboutShowLong = []
  long_synop = data.find('div', class_="synopsis-toggle__long" )
  for p in long_synop.find_all('p'):
    extract_tag_from_soup(p, "br")
    for pp in p:
      aboutShowLong.append(pp)
  return aboutShowLong

def make_dict(url_in="https://www.bbc.co.uk/programmes/b0076jd8"):
  soup = get_soup(url_in)
  data = soup.find('div', class_="island")
  title, url = get_titleUrl(soup)
  _dict = { 'title'      : title,
            'url'        : url,
            'parent_show': get_parent_series(soup), 
            'episode'    : get_episode(soup),
            'series'     : get_series(soup),
            'synopShort' : get_short_synop(data),
            'synopLong'  : get_long_synop(data)
          }
  return _dict

def main():
  shows =  []
  for url in example_url[0:1]:
    shows.append(BbcPid(make_dict(url)))
    shows[-1].print()

#Example urls
example_url = ["https://www.bbc.co.uk/programmes/b00j1z95",
               "https://www.bbc.co.uk/programmes/b017prn7",
               "https://www.bbc.co.uk/programmes/b0076jd8",
               "https://www.bbc.co.uk/programmes/b007jq5n",
               "https://www.bbc.co.uk/programmes/m000vjq5",
               "https://www.bbc.co.uk/programmes/b007jzhc",
               "https://www.bbc.co.uk/programmes/b00tvmjw", 
               "https://www.bbc.co.uk/programmes/m0003jms", 
               "https://www.bbc.co.uk/programmes/m000v29y", 
               "https://www.bbc.co.uk/programmes/b04yf68n", 
               "https://www.bbc.co.uk/programmes/b05vjjwn", 
               "https://www.bbc.co.uk/programmes/b00zf648", 
               "https://www.bbc.co.uk/programmes/b03yn6xr" 
	      ]

if __name__ == '__main__':
  main()
