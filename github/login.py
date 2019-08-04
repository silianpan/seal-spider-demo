import requests
from lxml import etree


class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/login',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Host': 'github.com',
            'Origin': 'https://github.com',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.dashbord_url = 'https://github.com/dashboard-feed'
        self.session = requests.Session()
    
    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        # print(etree.tostring(selector))
        token = selector.xpath('//input[@name="authenticity_token"]/@value')
        # print(token)
        return token
    
    def login(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token()[0],
            'login': email,
            'password': password,
            'webauthn-support': 'supported'
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            self.dynamics(response.text)
        
        response = self.session.get(self.logined_url, headers=self.headers)
        if response.status_code == 200:
            self.profile(response.text)
    
    def dynamics(self, html):
        response = self.session.get(self.dashbord_url, headers=self.headers)
        selector = etree.HTML(response.text)
        dynamics = selector.xpath('//div[contains(@class, "flex-items-baseline")]')
        print(dynamics)
        for item in dynamics:
            username = ' '.join(item.xpath('./div/a[1]/text()')).strip().replace('\n', '')
            projectname = ' '.join(item.xpath('./div/a[2]/text()')).strip().replace('\n', '')
            dynamic = ' '.join(item.xpath('./div/text()')).strip().replace('\n', '')
            if username:
                print(username, projectname, dynamic)
    
    def profile(self, html):
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print(name, email)


if __name__ == "__main__":
    login = Login()
    login.login(email='user', password='password')
