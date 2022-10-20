import tkinter as tk
from tkinter import messagebox
import snscrape.modules.twitter as sntwitter
import pandas as pd
import nltk
import tkcalendar

import TmWin
import SaWin
import cluster_output
import settings

# nltk.download('words')
words = set(nltk.corpus.words.words())


def file_selection():
    search_list = []
    search_input = settings.search_input + '.csv'
    if search_input not in search_list:
        search_list.append(search_input)
        return search_input
    else:
        return 0


class SearchWindow:
    # create a constructor
    def __init__(self):

        self.win = tk.Tk()

        self.frame = None
        self.line = None
        self.start_title = None
        self.search_label = None
        self.access_button = None
        self.sentimentanalysis_button = None
        self.topicmodelling_button = None
        self.start_date = None
        self.end_date = None
        self.search_entry = None

        # reset the window and background color
        self.canvas = tk.Canvas(self.win, width=600, height=400, bg='light blue')
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        hx = int(width / 2 - 600 / 2)
        wy = int(height / 2 - 400 / 2)
        str1 = "600x400+" + str(hx) + "+" + str(wy)
        self.win.geometry(str1)

        # disable resize of the window
        self.win.resizable(width=False, height=False)

        # change the title of the window
        self.win.title("TWEETSCRAPE | SEARCH WINDOW")

    def loginWin(self):
        # create an inner frame
        self.frame = tk.Frame(self.win, width=600, height=300)
        self.frame.place(x=0, y=50)

        self.line = tk.Canvas(self.frame, width=40, height=200)
        # self.line.create_line(23, 0, 23, 200, width=3)
        # self.line.place(x=x + 150, y=y + 10)

        self.start_title = tk.Label(self.frame, text="TWEETSCRAPE")
        self.start_title.config(font=("Calibri", 30, 'bold'))
        self.start_title.place(x=170, y=50)

        self.sentimentanalysis_button = tk.Button(self.frame, text="Sentiment Analysis", font=('Calibri', 15, 'bold'),
                                                  command=self.startSa)
        self.sentimentanalysis_button.place(x=130, y=200)

        self.topicmodelling_button = tk.Button(self.frame, text="Topic Modelling", font=('Calibri', 15, 'bold'),
                                               command=self.startTm)
        self.topicmodelling_button.place(x=305, y=200)

        self.start_date = tkcalendar.DateEntry(self.frame, width=10, font=('Calibri', 10), relief="solid")
        self.start_date.place(x=455, y=140)

        self.end_date = tkcalendar.DateEntry(self.frame, width=10, font=('Calibri', 10), relief="solid")
        self.end_date.place(x=455, y=160)

        self.search_label = tk.Label(self.frame, text="Search Keyword:", font=('Calibri', 20, 'bold'))
        self.search_label.place(x=50, y=140)

        self.search_entry = tk.Entry(self.frame, width=20, font=('Calibri', 15), relief="solid")
        self.search_entry.place(x=250, y=147)

        self.search_entry.bind("<Return>", self.extractTweet)

        self.win.bind('<Escape>', self.endSess)

        # Anything after this is not in window
        self.win.mainloop()

    def endSess(self, event):
        if messagebox.askokcancel('END SESSION', 'Exit Program?'):
            return self.win.quit(), self.win.destroy()
        else:
            return None

    def startTm(self):
        cluster_output.topicModelling()

    def startSa(self):
        self.win.destroy()
        SaWin.SaWindow()
        TmWin.TmWindow()

    def extractTweet(self, event):
        tweets_list2 = []
        settings.search_input = self.search_entry.get()
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        search_lang = 'en'
        search_location = 'Singapore'
        search_proximity = '10km'
        print(start_date)
        print(end_date)

        # Using TwitterSearchScraper to scrape data and append tweets to list
        for i, tweet in enumerate(
                sntwitter.TwitterSearchScraper(f'{settings.search_input} since:{start_date} until:{end_date}, '
                                               f'lang:{search_lang} near:{search_location} within:{search_proximity}').get_items()):
            if i > 100:
                break
            tweets_list2.append([tweet.date, tweet.id, tweet.user.username, tweet.content])

        # Creating a dataframe from the tweets list above
        tweets_df2 = pd.DataFrame(tweets_list2, columns=['Date', 'Tweet Id', 'Username', 'Tweet'])

        # Create .csv file
        tweets_df2.to_csv(self.search_entry.get() + '.csv', index=False)
        messagebox.showinfo(title="Tweetscrape", message="Scrapping Complete", )

        self.callEntry()

    def callEntry(self):
        search_input = self.search_entry.get()
        df = pd.read_csv(search_input + '.csv', names=['Tweet'])
        for row in df["Tweet"].items():
            print(row)  # Print .csv rows
        print(len(df))
        return df


if __name__ == '__main__':
    exeL = SearchWindow()
    exeL.loginWin()
    exeL.callEntry()
