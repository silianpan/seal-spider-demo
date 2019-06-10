import requests

response = requests.get('https://www.12306.cn')
# response = requests.get('https://inv-veri.chinatax.gov.cn/')
print(response.status_code)


response = requests.get('https://www.12306.cn', verify=False)
print(response.status_code)
