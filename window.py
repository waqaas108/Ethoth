from kivy.config import Config

# Set window size
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from cards.deck import Deck
from cards.reading import Reading
from cards.parser import ReadingInterpreter

import os
import re
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# initialize tabs

class DeckTab(TabbedPanelHeader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Deck"
        self.content = DeckContent()

class AnalyticsTab(TabbedPanelHeader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Analytics"
        self.content = AnalyticsContent()

class AboutTab(TabbedPanelHeader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "About"
        self.content = AboutContent()

# initialize content of the tabs

class DeckContent(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # stackoverflow says the on_touch_down custom binding should happen at the start
        self.bind(on_touch_down=self.on_touch_shuffle)
        self.bind(on_touch_down=self.on_touch_draw)
        # Reading images and creating a deck
        self.card_images = []
        self.deck = Deck('deck_files/order.txt')

        # Add a label for total cards in the deck incase some got deleted
        self.total_cards_label = Label(text=f"Total Cards: {len(self.deck.cards)}", size_hint_y=None, height=20, pos=(10, 30))
        self.add_widget(self.total_cards_label)

        self.reading = Reading(self.deck, 'reading_files')

        # create a button bound to self.reading.save_reading with bound displayers and sound effect
        # also added a screen refresh
        save_reading_button = Button(text="Save Reading", size_hint=(None, None), size=(200, 50), pos=(30, 10))
        save_reading_button.bind(on_press=self.reading.save_reading)
        save_reading_button.bind(on_press=self.deck_displayer)
        save_reading_button.bind(on_press=lambda x: SoundLoader.load('sfx/menu.mp3').play())
        save_reading_button.bind(on_press=self.clear_reading_display)
        self.add_widget(save_reading_button)

        # Add a button to return the cards to the deck, with similar bindings
        return_cards_button = Button(text="Return Cards", size_hint=(None, None), size=(200, 50), pos=(400, 10))
        return_cards_button.bind(on_press=self.reading.return_cards)
        return_cards_button.bind(on_press=self.deck_displayer)
        return_cards_button.bind(on_press=lambda x: SoundLoader.load('sfx/menu.mp3').play())
        return_cards_button.bind(on_press=self.clear_reading_display)
        self.add_widget(return_cards_button)

        # Call the displayers initially
        self.deck_displayer()
        self.reading_displayer()

    def deck_displayer(self, *args):
        for i, card in enumerate(self.deck.cards):
            # randomly select back of cards
            card_image = Image(source=np.random.choice(['deck/back1.png', 'deck/back2.png', 'deck/back3.png']), size=(100, 150))
            # pos 0 is 1000,600
            card_image.pos = (23+i-800, 0+(np.random.randint(-1, 1)))
            self.add_widget(card_image)

    def reading_displayer(self, *args):
        cards_on_board = self.reading.cards
        for card in cards_on_board:
            card_image = Image(source=card.image_filename, size=(100, 150))

            # Set the position of the card image based on the number of cards drawn
            if len(cards_on_board) == 1:
                card_image.pos = (-200, 0)
            elif len(cards_on_board) == 2:
                card_image.pos = (200, 0)
            elif len(cards_on_board) == 3:
                card_image.pos = (600, 0)
            # Add the card image to the list and layout
            self.card_images.append(card_image)
            self.add_widget(card_image)


    # method to remove the card images from the layout, had to make this separately
    # should have done so for the deck display as well, but it's not as immediately problematic
    def clear_reading_display(self, *args):
        for card_image in self.card_images:
            self.remove_widget(card_image)
        self.card_images = []

    # set x=44 to x=122 and y=282 to y=816 as a region on screen to click to shuffle deck
    def on_touch_shuffle(self, _, touch):
        if touch.x > 44 and touch.x < 122 and touch.y > 282 and touch.y < 816:
            pixel_card_equivalents = int(touch.x - 44)
            self.deck.cut(pixel_card_equivalents)
            # sfx!
            shuffle_sfx = SoundLoader.load('sfx/card_shuffle.mp3')
            shuffle_sfx.play()
            self.deck_displayer()

    def on_touch_draw(self, _, touch):
        if touch.x > 122 and touch.x < 484 and touch.y > 282 and touch.y < 816:
            self.reading.deal_card()
            # sfx!!1
            draw_sfx = SoundLoader.load('sfx/card_deal.mp3')
            draw_sfx.play()
            self.reading_displayer()

class AnalyticsContent(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # add a drop down menu for the user to select an analysis type out of planets, elements, sephiroth, and suits
        # super repetitive code, used ChatGPT
        self.dropdown = DropDown()
        self.planets = Button(text='Planet', size_hint_y=None, height=44)
        self.planets.bind(on_release=lambda btn: self.dropdown.select(btn.text))
        self.dropdown.add_widget(self.planets)
        self.elements = Button(text='Element', size_hint_y=None, height=44)
        self.elements.bind(on_release=lambda btn: self.dropdown.select(btn.text))
        self.dropdown.add_widget(self.elements)
        self.sephiroth = Button(text='Sephira', size_hint_y=None, height=44)
        self.sephiroth.bind(on_release=lambda btn: self.dropdown.select(btn.text))
        self.dropdown.add_widget(self.sephiroth)
        self.suits = Button(text='Suit', size_hint_y=None, height=44)
        self.suits.bind(on_release=lambda btn: self.dropdown.select(btn.text))
        self.dropdown.add_widget(self.suits)
        self.mainbutton = Button(text='Select Analysis', size_hint=(None, None), size=(200, 50), pos=(10, 1040))
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.add_widget(self.mainbutton)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        # use the reading interpreter to get the data
        self.reading_interpreter = ReadingInterpreter(deck_location='deck/order.txt', reading_location='reading_files')
        self.planets.bind(on_release=self.display_analytics)
        self.elements.bind(on_release=self.display_analytics)
        self.sephiroth.bind(on_release=self.display_analytics)
        self.suits.bind(on_release=self.display_analytics)
        # should add a calendar widget for this, or add text labels for the start and end dates
        # I like this code, this preloads the start and end dates by
        # basically searching for min and max dates in the reading files
        start_date, end_date = self.get_dates_from_files('reading_files')
        self.start_date_input = TextInput(text=start_date, multiline=False, size_hint=(None, None), size=(200, 50), pos=(300, 1040))
        self.add_widget(self.start_date_input)
        self.end_date_input = TextInput(text=end_date, multiline=False, size_hint=(None, None), size=(200, 50), pos=(650, 1040))
        self.add_widget(self.end_date_input)

    def get_dates_from_files(self, reading_location): # regex and datetime is ChatGPT too
        # Get the list of files in the reading location
        files = os.listdir(reading_location)
        # Sort the files
        files.sort(key=lambda x: int(x.split('.')[0]))
        # Get the date from the first file
        with open(os.path.join(reading_location, files[0]), 'r') as f:
            content = f.read()
            start_date = re.search(r'DATETIME: (.*)', content).group(1)
        # Get the date from the last file
        with open(os.path.join(reading_location, files[-1]), 'r') as f:
            content = f.read()
            end_date = re.search(r'DATETIME: (.*)', content).group(1)
        # Convert the dates to the format 'YYYY-MM-DD'
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')
        return start_date, end_date

    def display_analytics(self, btn):
        self.reading_interpreter.compile_readings()
        # Filter the readings by getting the start_date and end_date from the text inputs
        start_date = self.start_date_input.text
        end_date = self.end_date_input.text
        self.reading_interpreter.filter_readings(start_date=start_date, end_date=end_date)
        # Interpret the readings
        self.reading_interpreter.interpret_readings()
        card_data = self.reading_interpreter.card_data
        # Display the card data based on the button text
        if btn.text in ['Planet', 'Element', 'Sephira', 'Suit']:
            data = card_data[btn.text]
            print(data) # debug purposes
            fig, ax = plt.subplots()
            ax.bar(data.keys(), data.values())
            ax.set_title(btn.text)
            # 20 degree rotation of x-axis labels is the best compromise for Dragon's Head and Dragon's Tail
            plt.xticks(rotation=20)
            # Create the plot widget
            plot_widget = FigureCanvasKivyAgg(plt.gcf())
            # essentially anchoring the plot to the bottom of the screen
            plot_widget.size_hint = (1, 0.9)
            plot_widget.pos_hint = {'center_x': 0.5, 'center_y': 0.45}
            self.add_widget(plot_widget)

class AboutContent(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        about_text = """
Deck:
This is a tarot card reading app. It allows the user to shuffle a deck of cards
(click on the left side of the deck, on the stacked cards) and draw a reading (click on the top of the deck).
The shuffle function is actually cutting the deck at a random point, but it uses the mouse position to determine the cut.
Once you draw three cards, the reading is complete, and you can press return cards to discard the reading,
or save reading to save the cards and datetime to a file. The app also provides analytics on the readings.

Analytics:
The analytics tab allows the user to select a type of analysis (planet, element, sephira, or suit),
and then it will display a graph of the frequency of each attribute in the readings.
The user can also filter the readings by start and end date, which is what the text inputs are for.
By default, the start and end date are the first and last readings in the reading files.
So far, only dates in the format 'YYYY-MM-DD' are supported.

Issues:
The GUI loads another instance of the entire set of deck widgets every time you shuffle the deck.
If you spam the shuffle, you will soon run out of processing power. Be nice to the app for now and only run it for a few readings.
I think we are good for about 30 shuffles on an M1 mac.
If you draw cards from the deck and then close the app without returning them to the deck, the cards are lost forever.
Or at least, I haven't found them yet.
You have to go and delete deck_files/order.txt for the cards to come back.
You can go to the analysis tab and generate graphs, then go back to the deck and generate readings,
then go back and try to generate more graphs, but the graphs don't seem to change. For now,
I just reset the program, and then the graphs are generated with updated data.
        """
        about_label = Label(text=about_text, size_hint=(None, None), size=(1000, 600), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(about_label)

class CardApp(App):
    def build(self):
        tab_panel = TabbedPanel(do_default_tab=False)
        tab_panel.add_widget(DeckTab())
        tab_panel.add_widget(AnalyticsTab())
        tab_panel.add_widget(AboutTab())
        return tab_panel

if __name__ == "__main__":
    CardApp().run()