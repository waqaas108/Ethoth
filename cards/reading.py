# a reading is basically a board that will accept cards that get dealt from the deck
# when all cards are dealt, the reading is complete and will be saved to a file
# reading location is a directory, and the reading will be saved as files
# date and time will be inside the files and the filename will be a number

import os
from datetime import datetime

class Reading:
    def __init__(self, deck, reading_location):
        self.deck = deck
        self.cards = []
        self.complete = False
        # problematic code, interferes with using readings in the interpreter
        if len(deck.drawn_cards) > 0:
            self.cards = deck.drawn_cards
            if len(self.cards) == 3:
                self.complete = True
        self.reading_location = reading_location

    # having to coordinate deck draws between the reading and the deck was hard
    def deal_card(self):
        if len(self.cards) < 3:
            self.cards.append(self.deck.deal_card())
        if len(self.cards) == 3:
            self.complete = True

    # apparently if a function is being given to a button, it needs to have *args
    def return_cards(self, *args):
        for card in self.cards:
            self.deck.return_card(card)
        self.cards = []
        self.complete = False

    def save_reading(self, *args):
        if self.complete:
            if not os.path.exists(self.reading_location):
                os.makedirs(self.reading_location)
            reading_files = os.listdir(self.reading_location)
            reading_number = len(reading_files) + 1
            reading_file = os.path.join(self.reading_location, f"{reading_number}.txt")
            with open(reading_file, "w") as file:
                for card in self.cards:
                    file.write(f"{card.name}\n")
                file.write(f"DATETIME: {datetime.now()}")
            self.return_cards()
        else:
            pass