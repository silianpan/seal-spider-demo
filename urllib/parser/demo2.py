from urllib.robotparser import RobotFileParser
from urllib.request import urlopen, Request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

rp = RobotFileParser()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:67.0) Gecko/20100101 Firefox/67.0'}
req = Request(url='https://www.jianshu.com/robots.txt', headers=headers)
rp.parse(urlopen(req).read().decode('utf-8').split('\n'))
print(rp.can_fetch('*', 'https://www.jianshu.com/p/b67554025d7d'))
print(rp.can_fetch('*', "https://www.jianshu.com/search?q=python&page=1&type=collections"))