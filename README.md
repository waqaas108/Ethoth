# Ethoth: Digital Tarot a la Crowley

1. Describe the project. Don’t worry if you end up changing your idea, that’s fine as long as you
tell me. (4 points)

The project has stayed true to the proposal, and it's a digital Tarot deck that keeps track of the order of cards, and saves readings that it can then compile and graph up acoording to the elements in the cards that were drawn. The main requirements for the app were to have a deck object that simulates a real-life deck; the deck object should be able to be drawn from and shuffled, and the deck should be saved in its exact configuration when the app is closed. There should be a way to choose the exact spot from which the deck is shuffled, and the cards should be drawn off from the top of the deck. The readings made should be saved, and then the app should be able to compile and graph the readings to show the frequency of certain elements latent in the cards, such as planets, elements, etc.

2. Explain in a few sentences why you selected this project, and if you learned what you had
hoped to learn by doing this project (from your proposal). (4 points)

I selected this project because Tarot is a deeply personal discipline for me, and I've wondered about looking at readings across time for a few years now. The concepts I needed to know to make something like this were included in our course material, and I took the opportunity to make this. I also hope to market an app like this, because I know that if I was disappointed at the state of randomly generated internet Tarot decks, other people would be too. Over the course of the project I learned that making interlocking functions in the way that I did is not a straightforward task. I had to jump back and forth between the different script pages endless times to figure out what wasn't working. I've gained a new appreciation for the work that goes into making very basic applications. I also learned that it's not as hard as I thought either, since I was able to come pretty far and I've accomplished most of what I set out to do in the proposal. I might be able to make a marketable app out of this yet.

3. Describe the two major class themes selected, why you selected them, and how they are
applied in the project. (5 points)

The two themes for this project are GUI programming and Object Oriented Programming. I selected them because they work well together, and for any application that wants to see mass use, it has to move away from a terminal or a notebook. I also chose these because there is a lot more utility in these concepts (for me) than the other themes, especially since I want to make more projects with GUIs, and OOP was a glaring weakspot in my programming skills previously.

The GUI programming is applied in the project using Kivy, a framework for making apps that work on most operating systems, including iOS and Android. The app has a few tabs for the different functionalities, and the main tab has a deck object that can be shuffled and drawn from. I also managed to incorporate in some fun additions, such as playing sounds when certain actions take place.

The Object Oriented Programming is applied in the project by making a deck object that itself is made of card objects, which work together to populate reading objects. Most of the manipulations of cards are functions of the deck class, and the reading saving mechanism is a function of the reading class. Interestingly enough, I managed to make the analyses out of objects too. It helps that GUI programming translates well to OOP, and I was able to make a lot of the GUI elements into objects that I could manipulate together with the card and deck objects.

4. What you would do differently if you were to have an opportunity to redo this project and why.
(4 points)

I might have taken a stab at OpenGL for the deck object, and I might have used plotly, or some other hand-made solution, to visualize the readings as a heatmap on the tree of life. It's a lot more complicated than it sounds however, and I'm happy with settling for bar graphs for now. I would also include more complex interactions, such as the co-occurence of planets that are hostile to each other, or other things like that. As it is, I'm saving all the cards together (in a given timeframe of readings), and I'm not taking each reading into account as a unique occurence. I would have to rethink the way I'm approaching the analysers of this project to make that work.

5. How to run your project. (4 points)

Most libraries used are stock anaconda packages, except kivy itself. Kivy also has a specialized version of matplotlib which needs to be installed. The two commands I had to run are:
pip install kivy-garden
garden install matplotlib
Once the dependencies are installed, the project can be run by navigating a terminal into the main project folder and running:
python window.py

6. Was the project challenging in the way you expected? What did you overcome? (4 points)

It was challenging in ways I did not expect. Making different classes that work together is hard. I moved methods around a lot between different classes before things started working. Some methods, such as drawing a card and placing it in a reading, involved methods in both classes that interlocked, and it took a while to figure that out too, with me ending up assigning one class that would call the other class and not the other way around. The method is still a little jank, but it works for the most part now. Kivy does not make intuitive sense to me, and I still don't know why the code is structured the way it is, but I do have a better understanding of how to make a GUI now. Stackoverflow, random programming blogs, and reddit had to do most of the heavy lifting for me. Initially I had no idea how layouts worked, or how to assign positions, and I only made things work by forcibly restricting the window size, disabling user ability to resize the window, and then using a floatlayout to specify object positions. There's apparently a distinction between pos and pos_hint, which was also a novel concept to me. I still don't quite understand how to dynamically keep track of the changing value of a variable and display it in real time, but thankfully I haven't needed to do it more than once. Using dates to filter readings was also challenging, since it involved string formatting using methods local to the datetime library, and I ended up defaulting to chatGPT on that. I also realized that in most cases I had to use the classes I had made for the decks separately from the classes and methods that kivy used to display widgets, which created a lot of spaghetti code. I simply don't know what to do about it right now, but the code is functional so I'm happy with it for now.

7. Cited sources, appropriate acknowledgements. Explain how each source applied to your
project. (5 points)

https://kivymd.readthedocs.io/en/0.104.0/components/tabs/ - I used this to make the tabs in the app.
https://kivy.org/doc/stable/guide/widgets.html#organize-with-layouts - I used this to understand how to use layouts.
https://blog.kivy.org/2014/01/positionsize-of-widgets-in-kivy/ - I used this to understand how to position widgets.
https://stackoverflow.com/questions/37164410/fixed-window-size-for-kivy-programs - Restricting resizing of the window.
https://stackoverflow.com/questions/75263766/i-cant-install-garden-matplotlib-in-my-venv - Installing matplotlib for kivy to generate graphs in the GUI. End of a long chain of google searches.
ChatGPT - I used this to figure out how to format dates for the database, to slightly edit repititive code for the widgets and buttons, and to debug this instance where my pixel_coordinate selector wasn't working, and it turned out I was dividing things in such a way that the result was always 0. I also wrote most of the deck_downloader code using ChatGPT since it's not technically a part of the project.

8. If you attempted the extra credit, explain how you successfully met the criteria.

I might not have a good implementation of a third major theme, but I have many small implementations across most of our themes. I constructed my deck library by using a notebook (included in the project folder), with code that scrapes the source code of a website for links to the card images, downloads them, resizes them, and then saves them in a folder. This could be a weak variant of the API theme we studied in class. I have a lot of list comprehensions, and some code snippets in the GUI section have lambdas in strange places. I am using a lot of file handlers, with constant saving and loading across the application, and I use some regex here and there. I can probably qualify for the interesting variant of a theme where GUIs are concerned by having used kivy instead of tkinter. I have also used matplotlib inside of kivy, which is not as straightforward as it sounds.

9. Things that don't work. (??? points)

The GUI loads another instance of the entire set of deck widgets every time you shuffle the deck. If you spam the shuffle, you will soon run out of processing power. Be nice to the app for now and only run it for a few readings.
I think we are good for about 30 shuffles on an M1 mac.

If you draw cards from the deck and then close the app without returning them to the deck, the cards are lost forever. You have to go and delete deck_files/order.txt for the cards to come back. I tried to implement a fix but it was getting entirely too complicated, and I'm late to submitting this project as it is.

You can go to the analysis tab and generate graphs, then go back to the deck and generate readings, then go back and try to generate more graphs, but the graphs don't seem to change. For now, I just reset the program, and then the graphs are generated with updated data.

I haven't tested all the different combinations of edge-cases, such as saving a reading without drawing all three cards for the reading. I'm sure there are a lot of bugs in the code that I haven't found yet. The date selection system is also not very intuitive, but if you let things stay at default values, it should work fine.