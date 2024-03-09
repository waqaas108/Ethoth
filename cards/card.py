# defining a card, and just making space for all the different attributes a card can have
# not all attributes are used for every card, so I wanted to have setters for all of them, although they were not used
# not bothering with checks since this function is entirely made for the deck to work with

class Card:
    def __init__(self, name, image_filename, title, planet_orb, planet_house, sign_1, sign_2, sign_3, suit_1, suit_2, path, sephira, element_1, element_2):
        self.name = name
        self.image_filename = image_filename
        self.title = title
        self.planet_orb = planet_orb
        self.planet_house = planet_house
        self.sign_1 = sign_1
        self.sign_2 = sign_2
        self.sign_3 = sign_3
        self.suit_1 = suit_1
        self.suit_2 = suit_2
        self.path = path
        self.sephira = sephira
        self.element_1 = element_1
        self.element_2 = element_2

    def set_title(self, title):
        self.title = title

    def set_planet_orb(self, planet_orb):
        self.planet_orb = planet_orb

    def set_planet_house(self, planet_house):
        self.planet_house = planet_house

    def set_sign_1(self, sign_1):
        self.sign_1 = sign_1

    def set_sign_2(self, sign_2):
        self.sign_2 = sign_2

    def set_sign_3(self, sign_3):
        self.sign_3 = sign_3

    def set_suit_1(self, suit_1):
        self.suit_1 = suit_1

    def set_suit_2(self, suit_2):
        self.suit_2 = suit_2

    def set_path(self, path):
        self.path = path

    def set_sephira(self, sephira):
        self.sephira = sephira

    def set_element_1(self, element_1):
        self.element_1 = element_1

    def set_element_2(self, element_2):
        self.element_2 = element_2