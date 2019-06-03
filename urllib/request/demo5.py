import urllib.request

response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)
print(response.read())