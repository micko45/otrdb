from bs4 import BeautifulSoup as bs
import requests

url = "https://en.wikipedia.org/wiki/List_of_old-time_radio_programs"
req = requests.get(url)
soup = bs(req.content, 'html.parser')
data = []

def strapOnWiki(inputs):
   return  "https://en.wikipedia.org" + inputs

def create_dict(showurl, show):
  return { 'title'   : show,
           'showurl' : showurl }

for i in soup.find_all('ul')[3:-19]:
  for l in i.find_all('li'):
    for t in l:
      try:
        showText = t.text
      except:
        showText = ""
    for a in l.find_all('a'):
      showWikiUrl = strapOnWiki(a.get('href'))
    data.append(create_dict(showWikiUrl, showText))

print(data)
