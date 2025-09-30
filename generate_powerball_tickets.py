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
                print()
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
    def show_inputs(self):
        inputs = tuple(self.initial_inputs + self.additional_inputs)
        print("The following inputs will be hashed into an integer seed.")
        print(f"Inputs: {inputs}")
        print(f"Hash: {hash(inputs)}")
        print()

    # Return a hash of all current inputs
    def get_hash(self):
        inputs = tuple(self.initial_inputs + self.additional_inputs)
        return hash(inputs)
        
# Class for generating powerball tickets
class PowerballTicket:
    # Initialize with lucky hash for 
    def __init__(self, luck_hash):
        self.lucky_hash = luck_hash

    # Set seed for generating samples
    def set_seed(self):
        random.seed(self.lucky_hash)
        print(f"Random seed set with lucky hash: {self.lucky_hash}", end="\n\n")

    def generate_tickets(self, num_tickets=1):
        def red(text):
            return f"\x1b[91m{text}\x1b[0m"
        
        def white(text):
            return f"\x1b[97m{text}\x1b[0m"
        
        if num_tickets < 1:
            print("No tickets generated.")
        else:
            for _ in range(num_tickets):
                white_balls = sorted(random.sample(range(1, 70), 5))
                powerball = random.randint(1, 26)
                print("Powerball ticket generated: ", end=" ")
                for wb in white_balls:
                    print(white(wb), end=" ")
                print(red(powerball), end="\n\n")


lucky_inputs = PowerballInput()

lucky_inputs.add_inputs()

lucky_hash = lucky_inputs.get_hash()

lucky_rng = PowerballTicket(lucky_hash)
lucky_rng.generate_tickets(num_tickets=5)

 