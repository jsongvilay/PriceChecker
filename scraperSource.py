# Jason Songvilay
# PriceChecker Source Code
# Check item price on website once per day and notify user by email when desired item drops below set price

import requests
from bs4 import BeautifulSoup
import smtplib
import time

# URL of item
URL = 'https://www.tillys.com/product/honda-hole-shot-white-mens-t-shirt/354616150.html?dwvar_354616150_color=150&cgid=sale-mens-clothing-t-shirts'

# path of user's computer found using google
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/### Safari/###'}

# scrape the title and current price of item

# returns data from website


def check_price():
    page = requests.get(URL, headers=headers)  # return URL headers

    # parse html of page using BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')

    # scrape name of item
    title = soup.find(class_="product-name hidden-sm-down").get_text()
    price = soup.find(class_='price-bold').get_text()  # scrape price of item
    # convert price string of item to a float for comparison
    converted_price = float(price[1:5])

    print(converted_price)
    print(title.strip())  # print name and price of item in terminal

    if(converted_price < 10):
        send_mail()  # if the price of desired item falls below certain price point, notify user by email

# notify user via email when price falls below desired amount


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)  # set up email notifications
    server.ehlo()
    server.starttls()
    server.ehlo()

    # provide sender email login information
    server.login('user@email.com', 'password')
    # provide item name and price for dynamic info in email
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(class_="product-name hidden-sm-down").get_text()
    price = soup.find(class_='price-bold').get_text()

    # Dynamic subject line and body of email with link to
    subject = 'Price of ' + title + ' dropped!'
    body = 'It is now ' + price + '! Check the link below!\n\nhttps://www.tillys.com/product/honda-hole-shot-white-mens-t-shirt/354616150.html?dwvar_354616150_color=150&cgid=sale-mens-clothing-t-shirts'
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('sender email', 'receiving email', msg)  # send mail
    print('Email sent!')  # confirm email is sent
    server.quit()  # close server


check_price()  # check if price is below desired threshold

# automatically check the price once per day
# while(True):
# check_price()
# time.sleep(86400)
