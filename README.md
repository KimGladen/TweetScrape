# Tweetscrape v1.0, maintained as of 21/10/2022.
Abstract: We are a five member year one university students from Computer Engineering doing a team assignment based on Python Programming.
As our last lesson before embarking to other programming languages, we have been assigned a project to utilise our capabilities.


# The objective of this project was to develop a program that was capable of:
1. Crawling data online
2. Cleaning and preprocessing data
3. Process data into Sentiment Analysis and Topic Modelling
4. Display result via Graphical User Interface


# The topic for this project: Public responses towards healthcare workers during COVID19 pandemic.
keyowrds: covid19, healthcare workers, public response

# User guide when setting up the pogram for the first time.
The Integrated Development Environment used is PyCharm 2022 Community Version.

There are 6 main files for this program. In sequence are:
1. SearchWin.py
2. settings.py
3. SaWin.py
4. TmWin.py
5. cluster_backend.py
6. cluster_output.py

# There are 15 libraries used to support this program. In sequence and grouping are:
- Crawiling of online data
1. Snscrape

- Graphical User Interface
2. Tkinter 
3. tkcalender

- Handling of data
4. Pandas
5. Numpy

- Cleaning, preprocessing and processing of data
6. Re
7. Nltk
8. Gensim
9. Gsdmm
10. Pickle
11. Tqdm
12. Textblob

- Displaying of results
13. Matplotlib
14. Plotly 
15. Wordcloud

Ensure all files and libraries are properly installed and imported, else it will not function properly.
Two ways of installing libraries manually.
1. pip command on terminal: pip install +git(link)
2. Pycharm IDE > File > Settings > Project(Your project name) > Python Intepreter > + sign > search for library required

NOTE: For gsdmm library, you will need to include the file into your project otherwise the gsdmm library will not function. 
Common recurring errors faced: Directory/Pathway can't be found/accessed, Library/Module doesn't exist.


# User guide when running the program for the first time.
Once all files and libraries are properly setup, run the SearchWin.py first.
Key in your choice of keyword and press Enter key.
Once a message box appears, click Ok.
Click the Sentiment Analysis Button and view results, press esc key or click x to leave the windows.
Once returned to main window, click Topic Modelling and view results.


# The source code of this program was referenced from open source material online.
References link and materials used:

https://betterprogramming.pub/how-to-scrape-tweets-with-snscrape-90124ed006af

https://pub.towardsai.net/tweet-topic-modeling-part-2-cleaning-and-preprocessing-tweets-e3a08a8b1770

https://github.com/bicachu/short-text-topic-modeling-tutorial

https://github.com/rwalk/gsdmm/blob/master/README.md

https://docs.python.org/3/library/tk.html

https://matplotlib.org/stable/index.html

https://datatofish.com/matplotlib-charts-tkinter-gui/

https://radimrehurek.com/gensim/auto_examples/index.html

https://buildmedia.readthedocs.org/media/pdf/nltk/latest/nltk.pdf



  

