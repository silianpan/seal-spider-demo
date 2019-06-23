from urllib.parse import urlencode
from urllib.request import urlopen

data = bytes(urlencode({'word': 'hello'}), encoding='utf8')
response = urlopen('http://httpbin.org/post', data=data)
print(response.read())