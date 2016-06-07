import urllib
from bs4 import BeautifulSoup
from urllib import urlopen

class HtmlToTextConverter:
	def transform_html_into_text(self, url):
	    html = urllib.urlopen(url).read()
	    soup = BeautifulSoup(html)
	    for script in soup(["script", "style"]):
	        script.extract()
	    text = soup.get_text()
	    lines = (line.strip() for line in text.splitlines())
	    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	    return '\n'.join(chunk for chunk in chunks if chunk)