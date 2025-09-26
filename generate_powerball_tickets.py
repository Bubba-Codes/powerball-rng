#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import random
import time

# Define powerball input class for entering custom input
class PowerballInput:
    def __init__(self, initial_inputs=[]):
        self.additional_inputs = [time.time()]
        self.inputs = initial_inputs + self.additional_inputs

    def add_inputs(self):
        done = False
        while not done:
            user_response = input("Please enter additional inputs. Enter \"done\" when finished.")
            if user_response.lower() == "done":
               print("Inputs received.", end="\n\n")
               done = True
            else:
                self.additional_inputs.append(user_response)