import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from nltk.tokenize import TweetTokenizer
from wordcloud import STOPWORDS


def print_wordcloud(data):
    plt.style.use('seaborn-darkgrid')
    wc = WordCloud(background_color='black', height=1500,
                   width=4000).generate(data)

    plt.figure(figsize=(10, 20))
    plt.imshow(wc, interpolation="hamming")

    plt.axis('off')
    plt.show()


def cleanup_tweet(text):
    text = str(text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www.\S+', '', text)
    text = text.replace('RT ', ' ')
    text = text.replace('&amp;', 'and')
    text = text.replace(r'[^A-Za-z0-9]+', ' ')
    text = text.lower()

    return text


def better_wordcloud(df, feature, stopword_set):
    rows = [" ".join(el) if isinstance(el, list) else str(el) for el in df[feature]]
    data = " ".join(rows)

    wordcloud = WordCloud(width=1000,
                          height=800,
                          stopwords=stopword_set,
                          collocations=False,
                          colormap='Set3',
                          margin=0,
                          max_words=200,
                          min_word_length=4,
                          max_font_size=130, min_font_size=15,
                          background_color='gray').generate(data)
    plt.figure(figsize=(20, 15))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    tweets = pd.read_csv("covid19_tweets.tsv")
    tweets.columns = tweets.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("(", "").str.replace(")", "")

    print(tweets.columns)
    print(len(tweets) - len(tweets["text"].unique()))
    tweets = tweets.dropna(subset=["text"])
    print(tweets["text"].head())

    all = " ".join(text for text in tweets["text"])
    tweets['text'] = tweets['text'].apply(cleanup_tweet)
    tt = TweetTokenizer()
    tweets['tokenized'] = tweets['text'].apply(tt.tokenize)
    stopwoorden = STOPWORDS
    print_wordcloud(all)
    better_wordcloud(tweets, 'tokenized', stopwoorden)
