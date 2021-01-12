import os
import time
import sys

try:
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
    from pathlib import Path
    import requests
    import yagmail
    import logging
except ModuleNotFoundError:
    sys.exit("Required modules were not found.")

# Setup logging
logging.basicConfig(filename='zodiac.log', level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")

if os.path.exists('config'):
    env_path = Path('./config/')/'.env'
    load_dotenv(dotenv_path=env_path)
elif os.path.exists('config2'):
    env_path = Path('./config2/')/'.env'
    load_dotenv(dotenv_path=env_path)

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


class Zodiac:
    BASE_URL = "https://www.astrology.com/horoscope/daily/"
    TITLE = None
    CONTENT = None

    def __init__(self, zodiac_sign):
        self.zodiac_sign = zodiac_sign
        self.url = self.BASE_URL + self.zodiac_sign + '.html'
        self.scrape()

    def scrape(self):
        while True:
            try:
                r = requests.get(self.url)
                soup = BeautifulSoup(r.content, 'html.parser')
                content = soup.find('p').text
                self.TITLE = soup.title.string
                self.CONTENT = content
            except requests.exceptions.HTTPError as err:
                print("HTTP error:", err)
                time.sleep(2)
                continue
            except requests.exceptions.ConnectionError as err:
                print("Connection error:", err)
                time.sleep(2)
                continue
            except requests.exceptions.Timeout as err:
                print("Timeout Error:", err)
                time.sleep(2)
                continue
            except requests.exceptions.RequestException as err:
                print("Oops: Something Else", err)
                time.sleep(2)
                continue
            break


class SendMail(Zodiac):
    def __init__(self, zodiac_sign, email):
        self.email = email
        super().__init__(zodiac_sign)
        self.send_email()

    def send_email(self):
        subject = self.TITLE
        contents = self.CONTENT
        try:
            yag = yagmail.SMTP(email, password)
            yag.send(self.email, subject=subject, contents=contents)
            logging.info(f"Email successfully sent.")
        except yagmail.error.YagInvalidEmailAddress as err:
            logging.error("Invalid Email Address:", err)
