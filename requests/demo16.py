import requests

cookies = '_zap=2bc4b99c-c31b-4dad-9867-b6d4bfd2a70e; d_c0="AEAkCEvnTw6PTk2WNy3eA6yNHvd4YMW2Tyo=|1538660400"; _xsrf=n3XhVce1AQkLjqExlzvHkEhLUELhaqL8; q_c1=1f329dead96b483b97fc46f243a6f0ee|1560178921000|1547531829000; __utmz=51854390.1560178924.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); tst=r; __utmv=51854390.000--|2=registration_date=20130422=1^3=entry_date=20190115=1; l_n_c=1; l_cap_id="MDdhNmVlMWY3NDY4NGE0NWIwMzEzN2UxMzY3OTAyMmE=|1561252381|3debd6e6290aa2b50e6e16b8c86f397992047c87"; r_cap_id="ZGNhNzA1ZjU1YmEwNDJkMmFhOTVhYjNiYjM2YzU3N2Q=|1561252381|7f3937c21fe73ab1d5ff1ff76df9d3cdc453e4d4"; cap_id="MWNkNjUwODgyMzYyNGVhMDgyYzhjMzYwMWI4NTY1MzQ=|1561252381|c313b6111898c6d965cde98c532558b2dfc12db2"; n_c=1; __utma=51854390.671674692.1560178924.1561189278.1561252384.3; __utmc=51854390; tgw_l7_route=f2979fdd289e2265b2f12e4f4a478330; capsion_ticket="2|1:0|10:1561267929|14:capsion_ticket|44:MTg3ZjQ3ZWI0MzAxNGRjOTk5ZWQ0OWYwOGM0YTFhNDc=|829998652ebf1240ce8f6fb21d0342e0f413b588405d3466404dc36959fad8a6"; z_c0="2|1:0|10:1561267932|4:z_c0|92:Mi4xTTdnS0FBQUFBQUFBUUNRSVMtZFBEaVlBQUFCZ0FsVk4zRno4WFFEd2x5eEJfNmdEaktpbU9yc0dHOUphaWhaSHp3|6a05c2a62c4b5a24ed460c26f2d2979b008dfde1213ada58c2f8606f460acc1b"'
jar = requests.cookies.RequestsCookieJar()
headers = {
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}
for cookie in cookies.split(';'):
    key, value = cookie.split('=', 1)
    jar.set(key, value)
r = requests.get('http://www.zhihu.com', cookies=jar, headers=headers)
print(r.text)