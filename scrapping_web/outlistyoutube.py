import urllib
import urllib.request
import urllib3
from bs4 import BeautifulSoup
import sys

def text_to_search(textToSearch = 'hello world'):
    query = urllib.request.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    return url

def response(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    return html

def main():
    soup = BeautifulSoup(response(url))
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        print('https://www.youtube.com' + vid['href'])


if __name__=='__main__':
    if len(sys.argv)>1:
        url = sys.argv[1]
        main()
    else:
        url = text_to_search()
        main()


'''
this gives the output:

https://www.youtube.com/watch?v=al2DFQEZl4M
https://www.youtube.com/watch?v=pRKqlw0DaDI
...
https://www.youtube.com/watch?v=9sQEQkMDBjw
'''