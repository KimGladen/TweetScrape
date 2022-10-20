import tkinter as tk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from textblob import TextBlob
import re
import gensim
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS
from PIL import Image, ImageTk

import SearchWin


class SaWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PROJECT MANAGEMENT | ")
        self.configure(background="white")

        self.attributes('-fullscreen', True)
        self.bind('<Escape>', self.end_session)

        # reference_df = SearchWin.file_selection()
        # tweet_df = pd.read_csv(reference_df)
        tweet_df = pd.read_csv('COVID19.csv')
        tweet_df.dropna(axis='columns', inplace=True)
        tweet_df.drop_duplicates(inplace=True, subset="Tweet")

        punctuation = r'!"%&\’()*+,-./:;<=>?[\\]^_`{|}~•@'

        def remove_links(tweet):
            """Takes a string and removes web links from it"""
            tweet = re.sub(r'http\S+', '', tweet)  # remove http links
            tweet = re.sub(r'bit.ly/\S+', '', tweet)  # remove bitly links
            tweet = tweet.strip('[link]')  # remove [links]
            tweet = re.sub(r'pic.twitter\S+', '', tweet)
            return tweet

        def remove_users(tweet):
            """Takes a string and removes retweet and @user information"""
            tweet = re.sub('(RT\\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet)  # remove re-tweet
            tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet)  # remove tweeted at
            return tweet

        def remove_hashtags(tweet):
            """Takes a string and removes any hashtags"""
            tweet = re.sub('(#[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet)  # remove hashtags
            return tweet

        def remove_av(tweet):
            """Takes a string and removes AUDIO/VIDEO tags or labels"""
            tweet = re.sub('VIDEO:', '', tweet)  # remove 'VIDEO:' from start of tweet
            tweet = re.sub('AUDIO:', '', tweet)  # remove 'AUDIO:' from start of tweet
            return tweet

        def tokenize(tweet):
            """Returns tokenized representation of words in lemma form excluding stopwords"""
            result = []
            for token in gensim.utils.simple_preprocess(tweet):
                if token not in gensim.parsing.preprocessing.STOPWORDS \
                        and len(token) > 2:  # drops words with less than 3 characters
                    result.append(lemmatize(token))
            return result

        def lemmatize(token):
            """Returns lemmatization of a token"""
            return WordNetLemmatizer().lemmatize(token, pos='v')

        def preprocess_tweet(tweet):
            """Main master function to clean tweets, stripping noisy characters, and tokenizing use lemmatization"""
            tweet = remove_users(tweet)
            tweet = remove_links(tweet)
            tweet = remove_hashtags(tweet)
            tweet = remove_av(tweet)
            tweet = tweet.lower()  # lower case
            tweet = re.sub('[' + punctuation + ']+', ' ', tweet)  # strip punctuation
            tweet = re.sub('\\s+', ' ', tweet)  # remove double spacing
            tweet = re.sub('([0-9]+)', '', tweet)  # remove numbers
            tweet = re.sub('📝 …', '', tweet)
            tweet_token_list = tokenize(tweet)  # apply lemmatization and tokenization
            tweet = ' '.join(tweet_token_list)
            return tweet

        def basic_clean(tweet):
            """Main master function to clean tweets only without tokenization or removal of stopwords"""
            tweet = remove_users(tweet)
            tweet = remove_links(tweet)
            tweet = remove_hashtags(tweet)
            tweet = remove_av(tweet)
            tweet = tweet.lower()  # lower case
            tweet = re.sub('[' + punctuation + ']+', ' ', tweet)  # strip punctuation
            tweet = re.sub('\\s+', ' ', tweet)  # remove double spacing
            tweet = re.sub('([0-9]+)', '', tweet)  # remove numbers
            tweet = re.sub('📝 …', '', tweet)
            return tweet

        def tokenize_tweets(df):
            df['tokens'] = df.Tweet.apply(preprocess_tweet)
            num_tweets = len(df)
            print('Complete. Number of Tweets that have been cleaned and tokenized : {}'.format(num_tweets))
            return df

        clean_df = tokenize_tweets(tweet_df)
        clean_df.to_csv(r'cleaned_covid19.csv', index=False, header=True)

        # get sentiment of each tweet
        result = ['Positive', 'Negative', 'Neutral']
        sentiment = [0, 0, 0]
        colors = ["lightgreen", "red", "lightgrey"]
        for i, val in enumerate(clean_df.Tweet):
            if i != 0:
                x = str(val)
                Blob = TextBlob(x)
                if Blob.sentiment.polarity > 0:
                    sentiment[0] += 1
                elif Blob.sentiment.polarity < 0:
                    sentiment[1] += 1
                else:
                    sentiment[2] += 1

        # filter out zero sentiment
        result = [result[i] for i in range(len(sentiment)) if sentiment[i] != 0]
        colors = [colors[i] for i in range(len(sentiment)) if sentiment[i] != 0]
        sentiment = [i for i in sentiment if i != 0]

        # plot sentiment onto pie chart
        figure2 = Figure(figsize=(40, 10))
        ax2 = figure2.add_subplot(111)
        ax2.pie(sentiment, labels=result, colors=colors, autopct='%1.1f%%')
        canvas = FigureCanvasTkAgg(figure2, master=self)
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        # canvas.get_tk_widget().place(x=10, y=10)
        canvas.draw()

        # for the wordcloud
        comment_words = ''
        stopwords = list(STOPWORDS) + ["https"]

        # iterate through the csv file
        for val in clean_df.Tweet:

            # typecaste each val to string
            val = str(val)

            # split the value
            tokens = val.split()

            # Converts each token into lowercase
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()

            comment_words += " ".join(tokens) + " "

        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              min_word_length=3,
                              min_font_size=10).generate(comment_words)

        # for the wordcloud
        comment_words = ''
        stopwords = list(STOPWORDS) + ["https"]

        # iterate through the csv file
        for val in clean_df.Tweet:

            # typecaste each val to string
            val = str(val)

            # split the value
            tokens = val.split()

            # Converts each token into lowercase
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()

            comment_words += " ".join(tokens) + " "

        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              min_word_length=3,
                              min_font_size=10).generate(comment_words)

        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()
        plt.savefig('sentiment_wordcloud.png')

        image1 = Image.open("sentiment_wordcloud.png")
        test = ImageTk.PhotoImage(image1)
        label1 = tk.Label(image=test)
        label1.image = test

        # Position image
        label1.place(x=50, y=50)

    def end_session(self, *args):
        self.destroy()
        exe = SearchWin.SearchWindow()
        exe.loginWin()
        return 'break'


if __name__ == '__main__':
    exeSa = SaWindow()
    exeSa.mainloop()
