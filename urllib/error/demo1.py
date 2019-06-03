from urllib import request, error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
try:
    response = request.urlopen('http://cuiqingcai.com/index.htm')
except error.URLError as e:
    print(e.reason)