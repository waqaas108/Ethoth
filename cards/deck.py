# the deck itself

import os
import random
from .card import Card
import pandas as pd

class Deck:
    # struggled to figure out how to initialize the deck with the cards, ended up saving all the card data in a csv file
    # that I typed manually
    naive_card_list = []
    # open card_table as a df
    card_table = pd.read_csv('cards/cards.csv')
    for index, row in card_table.iterrows():
        card = Card(row["Card"], os.path.join('deck', row["Image"]), row["Title"], row["planet_orb"], row["planet_house"], row["sign_1"], row["sign_2"], row["sign_3"], row["suit_1"], row["suit_2"], row["path"], row["sephira"], row["element_1"], row["element_2"])
        naive_card_list.append(card)

    def __init__(self, deck_location):
        self.cards = []
        self.drawn_cards = []
        self.deck_location = deck_location

        if not os.path.exists(self.deck_location):
            self.cards = self.naive_card_list
            self.save_order()
        else:
            self.cards = self.naive_card_list
            self.load_order()

    def get_card_by_name(self, name):
        for card in self.cards:
            if card.name == name:
                return card
        return None

    def save_order(self):
        with open(self.deck_location, "w") as file:
            for card in self.cards:
                file.write(f"{card.name}\n")
            # this drawn card business is also problematic, but was an attempt to solve the problem of cards going missing
            # if the program is quit without returning the cards first
            for card in self.drawn_cards:
                file.write(f"DRAWN:{card.name}\n")

    def load_order(self):
        # error exception lets us start with a fresh deck if the file is missing or deleted intentionally
        try:
            with open(self.deck_location, "r") as file:
                card_order = [line.strip() for line in file if not line.startswith("DRAWN")]
                drawn_cards = [line.split(":")[1] for line in file if line.startswith("DRAWN")]
                self.drawn_cards = [card for card in self.cards if card.name in drawn_cards]
                self.cards = [card for card in self.cards if card.name in card_order]
                self.cards.sort(key=lambda card: card_order.index(card.name))
        except FileNotFoundError:
            pass

    # unused function
    def shuffle(self):
        random.shuffle(self.cards)
        self.save_order()

    # true shuffle function
    def cut(self, index):
        card_list = self.cards[index:] + self.cards[:index]
        self.cards = card_list
        self.save_order()

    def deal_card(self):
        # pop the last card from the list
        pop = self.cards.pop()
        self.drawn_cards.append(pop)
        self.save_order()
        return pop
    
    def return_card(self, card):
        self.cards.append(card)
        self.drawn_cards.remove(card)
        self.save_order()