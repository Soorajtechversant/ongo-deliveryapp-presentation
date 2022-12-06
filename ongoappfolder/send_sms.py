import os
from requests import request
from twilio.rest import Client
from .forms import *


def sendsms(phn_number):
            # form = CustomSignupForm
            phone = phn_number    
            account_sid = 'AC66bd82bd2be639ec3171a35ba5ba0440'
            auth_token = '09f0e0d27ce597c8a7ce3b58ac172676'
            client = Client(account_sid, auth_token)
            message = client.messages \
                                    .create(
                                        body="Welcome TO Ongo Delivery System",
                                        from_='+17088477034',
                                        to= phone
                                    )

            print("Registered successfully")
