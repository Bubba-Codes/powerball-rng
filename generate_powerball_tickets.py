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

    # Add additional inputs
    def add_inputs(self):
        done = False
        while not done:
            user_response = input("Please enter additional inputs. Enter \"done\" when finished.")
            if user_response.lower() == "done":
               print("Inputs received.", end="\n\n")
               done = True
            else:
                self.additional_inputs.append(user_response)

    # Get powerball jackpot value
    def get_powerball_jackpot(self):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        url = "https://www.powerball.com/"

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        jackpot_el = soup.find("span", class_="game-jackpot-number text-xxxl lh-1 text-center")

        print(jackpot_el)

 