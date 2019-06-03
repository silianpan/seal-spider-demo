import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

response = urllib.request.urlopen('https://www.python.org')
print(response.status)
print(response.getheaders())
print(response.getheader('Server'))