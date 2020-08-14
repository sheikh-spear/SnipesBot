
import re
from urllib.parse import quote
from requet import Requet
from random import randint
from time import sleep
from sys import argv as av


class SnipesBot:
    cookies = {}
    requestAPI = Requet(False, "www.snipes.fr", timeout=30)

    def makeRegistrationForm(self, name, surname, csrf_token):
        email = name + "." + surname + "@gmail.com"
        return "dwfrm_profile_register_title=Herr"\
            + "&dwfrm_profile_register_firstName=" + name\
            + "&dwfrm_profile_register_lastName=" + surname\
            + "&dwfrm_profile_register_email=" + quote(email)\
            + "&dwfrm_profile_register_emailConfirm=" + quote(email)\
            + "&dwfrm_profile_register_password=" + quote(email)\
            + "&dwfrm_profile_register_passwordConfirm=" + quote(email) \
            + "&dwfrm_profile_register_phone=&dwfrm_profile_register_birthday=&dwfrm_profile_register_acceptPolicy=true"\
            + "&csrf_token=" + csrf_token

    def makeLoginForm(self, email, csrf_token):
        return "dwfrm_profile_customer_email=" + email \
            + "&dwfrm_profile_login_password=" + email\
            + "&csrf_token=" + csrf_token

    def createAccount(self, name, surname):
        result, cookies = self.requestAPI.requet("/registration?rurl=1", headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'raw',
            'DNT': '1',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1'
        })
        csrf_token = re.findall(
            "name=\"csrf_token\" value=\"(.*)\"", result)[0]
        sleep(randint(10, 20))
        print(csrf_token)
        payload = self.makeRegistrationForm(name, surname, csrf_token)
        self.requestAPI.requet(
            url="/on/demandware.store/Sites-snse-FR-Site/fr_FR/Account-SubmitRegistration?rurl=1&format=ajax",
            method="POST",
            cookies=cookies,
            body=payload,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Length': str(len(payload)),
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'raw',
                'Referer': 'https://www.snipes.fr/registration?rurl=1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'DNT': '1',
                'Connection': 'close',
                'Upgrade-Insecure-Requests': '1'
            }
        )

    def login(self, email):
        result, self.cookies = self.requestAPI.requet("/login", headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'raw',
            'DNT': '1',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1'
        })
        csrf_token = re.findall(
            "name=\"csrf_token\" value=\"(.*)\"", result)[0]
        payload = self.makeLoginForm(email, csrf_token)
        result, newCookies = self.requestAPI.requet(
            url="/authentication?rurl=1&format=ajax",
            method="POST",
            cookies=self.cookies,
            body=payload,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Length': str(len(payload)),
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'raw',
                'Referer': 'https://www.snipes.fr/registration?rurl=1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'DNT': '1',
                'Connection': 'close',
                'Upgrade-Insecure-Requests': '1'
            }
        )
        self.cookies.update(newCookies)
        self.cookies

    def addShoeToBasket(self):
        payload = "pid=0001380189422100000008&options=%5B%7B%22optionId%22%3A%22212%22%2C%22selectedValueId%22%3A%2240%22%7D%5D&quantity=1"
        self.requestAPI.requet(
            url='/p/adidas-zx_2k_boost_w-solar_yellow%2Fcloud_white%2Fred-00013801894221.html', cookies=self.cookies)
        sleep(randint(10, 20))
        self.requestAPI.requet(
            url="/on/demandware.store/Sites-snse-FR-Site/fr_FR/Cart-AddProduct?format=ajax", method="POST",
            cookies=self.cookies, headers={
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Length': str(len(payload)),
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'raw',
                'Referer': 'https://www.snipes.fr/p/adidas-zx_2k_boost_w-solar_yellow%2Fcloud_white%2Fred-00013801894221.html',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'DNT': '1',
                'Upgrade-Insecure-Requests': '1',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'close'

            }, body=payload)

    def run(self, name: str, surname: str, create: bool):
        try:
            if create:
                self.createAccount(name=name, surname=surname)
            self.login(name + "." + surname + "@gmail.com")
            self.addShoeToBasket()
        except:
            print("Something went wrong")


s = SnipesBot()
if len(av) <= 2:
    print("usage: python3 SoleBoxBot.py name surname [-c]")
    exit(1)

if "-c" in av:
    s.run(av[1], av[2], True)
else:
    s.run(av[1], av[2], False)
