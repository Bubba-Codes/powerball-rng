#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import random
import time

# Define powerball input class for entering custom input
class PowerballInput:
    def __init__(self, initial_inputs=[]):
        self.initial_inputs = initial_inputs
        self.additional_inputs = [time.time(), self.scrape_powerball_jackpot(), self.scrape_last_powerball()]

    # Add additional inputs
    def add_inputs(self):
        done = False
        while not done:
            user_response = input("Please enter additional inputs. Enter \"done\" when finished: ")
            if user_response.lower() == "done":
               print("Inputs received.", end="\n\n")
               done = True
            else:
                self.additional_inputs.append(user_response)

    # Return powerball page as BeautifulSoup
    def powerball_site_scrape(self, tag, cls):
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

        el = soup.find(tag, class_=cls)
        while not el:
            time.sleep(2)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            el = soup.find(tag, class_=cls)
        return el.text.strip()

    # Get powerball jackpot value
    def scrape_powerball_jackpot(self): 
        jackpot_text = self.powerball_site_scrape("span", "game-jackpot-number text-xxxl lh-1 text-center")
        jackpot_text = jackpot_text.replace("$","")
        val, unit = jackpot_text.split(" ")

        if unit.lower() == "million":
            jackpot_value = float(val) * 1000000.00
        if unit.lower() == "billion":
            jackpot_value = float(val) * 1000000000.00
        return int(jackpot_value)

    # Get last powerball drawn
    def scrape_last_powerball(self):
        powerball_text = self.powerball_site_scrape("div", "form-control col powerball item-powerball")
        return int(powerball_text)
    
    # Show list of inputs
    def show_inputs_hash(self):
        inputs = tuple(self.initial_inputs + self.additional_inputs)
        print("The following inputs will be hashed into an integer seed.")
        print(f"Inputs: {inputs}")
        print(f"Hash: {hash(inputs)}")
        

test = PowerballInput()

print(test.scrape_powerball_jackpot())
print(test.scrape_last_powerball())
test.add_inputs()
test.show_inputs_hash()


 