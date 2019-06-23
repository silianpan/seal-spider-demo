from urllib.request import urlopen
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

response = urlopen('https://www.python.org')
print(response.read().decode('utf-8'))