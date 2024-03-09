# this file will compile all the readings and interpret the attributes of the cards
# a date range will be used to filter the readings
# card attributes will be turned into a dataframe and then analyzed

import os
import re
import numpy as np
import pandas as pd
from datetime import datetime
from .deck import Deck
from .reading import Reading

class ReadingInterpreter:
    def __init__(self, deck_location, reading_location):
        self.deck = Deck(deck_location)
        self.reading_location = reading_location
        self.readings = []
        self.reading_files = os.listdir(reading_location)
        self.reading_files.sort()
        self.reading_files = [file for file in self.reading_files if file.endswith(".txt")]
        self.reading_files = [os.path.join(reading_location, file) for file in self.reading_files]
        self.reading_files = self.reading_files[::-1]

    # compile the readings from the files
    def compile_readings(self):
        for file in self.reading_files:
            with open(file, "r") as file:
                cards = []
                for line in file:
                    if line.startswith("DATETIME"):
                        date = re.search(r'DATETIME: (.*)', line).group(1)
                        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')
                    else:
                        card = self.deck.get_card_by_name(line.strip())
                        cards.append(card)
                self.readings.append((cards, date))

    # filter the readings by date
    def filter_readings(self, start_date, end_date):
        self.readings = [reading for reading in self.readings if start_date <= reading[1] <= end_date]

    # interpret the readings and turn them into a dataframe
    def interpret_readings(self):
        card_data = {'Planet': {'Luna': 0, 'Earth': 0, 'Mars': 0, 'Mercury': 0, 'Saturn': 0, 'Sol': 0, 'Venus': 0, 'Jupiter': 0, 'Uranus': 0, 'Neptune': 0, 'Pluto': 0, "Dragon's Head": 0, "Dragon's Tail": 0},
                     'Sign': {'Aries': 0, 'Taurus': 0, 'Gemini': 0, 'Cancer': 0, 'Leo': 0, 'Virgo': 0, 'Libra': 0, 'Scorpio': 0, 'Sagittarius': 0, 'Capricorn': 0, 'Aquarius': 0, 'Pisces': 0},
                     'Suit': {'Cups': 0, 'Disks': 0, 'Swords': 0, 'Wands': 0},
                     'Sephira': {'Chokmah': 0, 'Binah': 0, 'Chesed': 0, 'Geburah': 0, 'Tiphareth': 0, 'Netzach': 0, 'Hod': 0, 'Yesod': 0, 'Malkuth': 0},
                     'Element': {'Fire': 0, 'Water': 0, 'Air': 0, 'Earth': 0}}
        for reading in self.readings:
            for card in reading[0]:
                # planet_count, sign_count, suit_count, sephira_count, element_count are determined by the number of not null attributes
                planet_count = sum([1 for planet in [card.planet_orb, card.planet_house] if planet])
                sign_count = sum([1 for sign in [card.sign_1, card.sign_2, card.sign_3] if sign])
                suit_count = sum([1 for suit in [card.suit_1, card.suit_2] if suit])
                element_count = sum([1 for element in [card.element_1, card.element_2] if element])
                # if the attribute is not null, we increment the count
                if card.planet_orb and card.planet_orb is not np.nan:
                    card_data['Planet'][card.planet_orb] += 1/planet_count
                if card.planet_house and card.planet_house is not np.nan:
                    card_data['Planet'][card.planet_house] += 1/planet_count
                if card.sign_1 and card.sign_1 is not np.nan:
                    card_data['Sign'][card.sign_1] += 1/sign_count
                if card.sign_2 and card.sign_2 is not np.nan:
                    card_data['Sign'][card.sign_2] += 1/sign_count
                if card.sign_3 and card.sign_3 is not np.nan:
                    card_data['Sign'][card.sign_3] += 1/sign_count
                if card.suit_1 and card.suit_1 is not np.nan:
                    card_data['Suit'][card.suit_1] += 1/suit_count
                if card.suit_2 and card.suit_2 is not np.nan:
                    card_data['Suit'][card.suit_2] += 1/suit_count
                if card.sephira and card.sephira is not np.nan:
                    card_data['Sephira'][card.sephira] += 1
                if card.element_1 and card.element_1 is not np.nan:
                    card_data['Element'][card.element_1] += 1/element_count
                if card.element_2 and card.element_2 is not np.nan:
                    card_data['Element'][card.element_2] += 1/element_count
        self.card_data = card_data