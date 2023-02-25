import requests
import lxml
import smtplib
import os
from twilio.rest import Client
from notification_manager import NotificationManager
# --------------------------------------------------------- webscraping --------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup


class Tracker:

    def __init__(self, product_name, product_url, expected_price, phone_number):
        self.product_url = product_url
        self.expected_price = expected_price
        self.product_name = product_name
        self.phone_number = phone_number
        # self.Update()

    def Update(self):
        print("tracking....")
        response = requests.get(self.product_url, headers={"Accept-Language": "en-US,en;q=0.9",
                                                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                         "Chrome/106.0.0.0 Safari/537.36 "
                                                                         "Edg/106.0.1370.52 "
                                                           }
                                )

        soup = BeautifulSoup(response.content, "lxml")
        # print(soup.prettify())
        price_html = soup.find("span", class_="a-offscreen")
        # returns inner text.getText()
        price = price_html.getText()
        # print(price)
        price_without_currency = price.split('₹')[1]
        price_without_comma = price_without_currency.replace(",", "")
        price_float = float(price_without_comma)
        print(price_float)
        price = price_float
        print("Printing Price to check")
        print(self.expected_price)
        price_limit = float(self.expected_price)
        product_title = self.product_name

        notification_manager = NotificationManager(self.phone_number)
        if price <= price_limit:
            print("sending")
            notification_manager.send_sms(
                message=f"Subject: Low Price Alert -- ₹ {price} for {product_title} has dropped to ₹ {price}"
            )

        return price
