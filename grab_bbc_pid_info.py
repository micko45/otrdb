from bs4 import BeautifulSoup as bs
import requests


class BbcPid:

  def __init__(self, _dict):
    self.title = _dict['title']
    self.url = _dict['url']
    self.parent = _dict['parent_show']
    self.episode =_dict['episode']
    self.series = _dict['series']
    self.short_synop =_dict['synopShort'][0]
    self.long_synop = _dict['synopLong']

  def print(self):
    print(self.title)
    print(self.url)
    print(self.parent)
    print(self.episode)
    print(self.series)
    print(self.short_synop)
    for i in self.long_synop:
      print(i)


def get_soup(url):
  req = requests.get(url)
  soup = bs(req.content, 'html.parser')
  return soup

def extract_tag_from_soup(extractFrom, toExtract):
  for s in extractFrom.select(toExtract):
    s.extract()

def get_titleUrl(soup):
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

def print_line_by_line(inputs):
  for i in inputs:
    print(i)

def make_dict(data, soup):
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

def print_dict(_dict):
  print(_dict['title'])
  print(_dict['url'])
  print(_dict['parent_show'])
  print(_dict['episode'])
  print(_dict['series'])
  print(_dict['synopShort'][0])
  for i in _dict['synopLong']:
    print(i)

def main():
  for l in example_url:
    soup = get_soup(l)
    data = soup.find('div', class_="island")
    _dict = make_dict(data, soup)
    print_dict(_dict)
    print("\n\n\n")

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

#main()

soup = get_soup("https://www.bbc.co.uk/programmes/b0076jd8")
data = soup.find('div', class_="island")
_dict = make_dict(data, soup)
show = BbcPid(_dict)
show.print()
