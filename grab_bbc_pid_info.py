from bs4 import BeautifulSoup as bs
import requests

#url = "https://www.bbc.co.uk/programmes/b00j1z95"
url = "https://www.bbc.co.uk/programmes/b017prn7"
url = "https://www.bbc.co.uk/programmes/b0076jd8"
url = "https://www.bbc.co.uk/programmes/b007jq5n"
url = "https://www.bbc.co.uk/programmes/m000vjq5"
url = "https://www.bbc.co.uk/programmes/b007jzhc"

req = requests.get(url)
soup = bs(req.content, 'html.parser')
data = soup.find('div', class_="island")

def extract_tag_from_soup(extractFrom, toExtract):
  for s in extractFrom.select(toExtract):
    s.extract()

def get_title(soup):
  data = soup.find('div', class_="br-masthead__title")
  link = data.find('a')
  text = link.text
  url = "https://www.bbc.o.uk" + link.get('href')
  return text, url


def get_short_synop(data):
  aboutShowShort = []
  short_synop = data.find('div', class_="synopsis-toggle__short" )
  for p in short_synop.find_all('p'):
    extract_tag_from_soup(p, "br")
    for pp in p:
      #print(pp)
      aboutShowShort.append(pp)
  return aboutShowShort

def get_long_synop(data):
  aboutShowLong = []
  long_synop = data.find('div', class_="synopsis-toggle__long" )
  for p in long_synop.find_all('p'):
    extract_tag_from_soup(p, "br")
    for pp in p:
      #print(pp)
      aboutShowLong.append(pp)
  return aboutShowLong

def print_line_by_line(inputs):
  for i in inputs:
    print(i)

def make_dict(data, soup):
  title, url = get_title(soup)
  _dict = { 'title'      : title,
            'url'        : url,
            'episode'    : get_episode(soup),
            'synopLong'  : get_long_synop(data), 
            'synopShort' : get_short_synop(data)
          }
  return _dict

def print_dict(_dict):
  print(_dict['title'])
  print(_dict['url'])
  print(_dict['synopShort'][0])
  print("Series:")
  print(_dict['episode'])
  for i in _dict['synopLong']:
    print(i)
  
def get_episode(soup):
  data = soup.find('div', class_="gamma")
  data = data.find('span')
  return data.text.strip()

#get_title(soup)
#get_episode(soup)
_dict = make_dict(data, soup)
print_dict(_dict)
