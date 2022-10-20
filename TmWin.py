import tkinter as tk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



class TmWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PROJECT MANAGEMENT | ")
        self.configure(background="white")

        self.attributes('-fullscreen', True)
        self.bind('<Escape>', self.end_session)

        figure2 = Figure(figsize=(40, 10), dpi=100)
        ax2 = figure2.add_subplot(111)
        line = FigureCanvasTkAgg(figure2, master=self)
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        line.draw()

        df2 = pd.read_csv('cleaned_covid19.csv')
        df = pd.DataFrame(df2, columns=['Date', 'Tweet'])
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Year'] = df['Date'].dt.year
        df['Date'] = df['Date'].dt.date
        #df = df[['Date', 'Tweet']].groupby('Date').count()
        #df.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
        df.groupby('Date')['Tweet'].count().plot(kind='line', legend=True, ax=ax2, color='green',
                                                 figsize=(16, 8))
        ax2.set_title('Trend setting')
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Daily Tweets")

    def end_session(self, *args):
        self.destroy()


if __name__ == '__main__':
    exeTm = TmWindow()
    exeTm.mainloop()
