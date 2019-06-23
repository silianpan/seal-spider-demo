import requests

r = requests.get("https://tse3-mm.cn.bing.net/th?id=OIP.nHHTYpPJ7Kb_6kHaUBZZOwHaEK&w=272&h=160&c=7&o=5&pid=1.7")
with open('favicon.jpg', 'wb') as f:
    f.write(r.content)