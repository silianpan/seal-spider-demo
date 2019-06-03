from urllib import request,error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
try:
    response = request.urlopen('http://cuiqingcai.com/index.htm')
except error.HTTPError as e:
    print(e.reason, e.code, e.headers, sep='\n')