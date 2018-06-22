# these should be the only imports you need

import requests
from bs4 import BeautifulSoup

# write your code here
# usage should be python3 part3.py

base_url = "https://www.michigandaily.com/"
r = requests.get(base_url)
data = r.text
soup = BeautifulSoup(data, 'html.parser')

# print(soup.prettify())

mostread = soup.find('div', {'class': 'pane-mostread'})
# print(mostread)

headlines_soup = mostread.find_all('a')
headlines = []
authors = []

for article in headlines_soup:
	headlines.append(article.get_text())

for article in headlines_soup:
	r = requests.get(base_url + article['href'])
	data = r.text
	soup = BeautifulSoup(data, 'html.parser')

	author_soup = soup.find('div', {'class': 'byline'})

	if (author_soup):
		author = author_soup.find('a').get_text()
		authors.append(author)

		# print("author: " + author)
	else:
		authors.append('Unspecified')
		# print("author: " + author)


print('Michigan Daily -- MOST READ')

for i in range(len(headlines)):
	print(headlines[i])
	print("  by " + authors[i])