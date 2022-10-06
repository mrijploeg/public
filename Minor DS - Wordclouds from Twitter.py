import pandas as pd
from nltk import ngrams
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from nltk.tokenize import TweetTokenizer
from wordcloud import STOPWORDS
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import seaborn as sns


def bar_text_freq(df, feature, n):
    # " ".join(r1).split(" ")).items()
    rows = [" ".join(el) if isinstance(el, list) else str(el) for el in df[feature]]
    data = " ".join(rows).split(" ")
    tweet_count = Counter(data)
    top_words = pd.DataFrame(tweet_count.most_common(n), columns=['word', 'count'])
    fig, ax = plt.subplots(figsize=(16, 6))
    sns.barplot(x='word', y='count',
                data=top_words, ax=ax)
    plt.title("Top {} Prevalent Words".format(n))
    plt.xticks(rotation='vertical')


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


def get_ngrams(text, num):
    tokens = tt.tokenize(text)
    ngs = ngrams(tokens, num)
    return list(ngs)


def get_sentiment(row):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(row)
    return sentiment_score['compound']


if __name__ == '__main__':
    nltk.download('vader_lexicon')
    tweets = pd.read_csv("covid19_tweets.tsv")
    tweets.columns = tweets.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("(", "").str.replace(")", "")

    # Answers to the questions.
    print(tweets.columns)
    print(len(tweets) - len(tweets["text"].unique()))
    tweets = tweets.dropna(subset=["text"])
    print(tweets["text"].head())

    # Unprocessed wordcloud.
    all = " ".join(text for text in tweets["text"])
    print_wordcloud(all)

    # Clean tweets.
    tweets['text'] = tweets['text'].apply(cleanup_tweet)

    # Tokenize tweets.
    tt = TweetTokenizer()
    tweets['tokenized'] = tweets['text'].apply(tt.tokenize)

    # Create bigrams.
    tweets['bigrams'] = tweets['text'].apply(lambda x: get_ngrams(x, 2))

    # Get sentiment analysis from the tweets.
    tweets['sentiment_scores'] = tweets['text'].apply(get_sentiment)
    tweets['sentiment_label'] = tweets['sentiment_scores'].apply(
        lambda x: 'neutral' if x == 0 else (
            'positive' if x > 0 else 'negative'))

    # Leave stopwords in the tweets.
    bar_text_freq(tweets, 'tokenized', 20)
    stop = STOPWORDS
    tweets['tweet_without_stopwords'] = tweets['text'].apply(
        lambda x: ' '.join(
            [word for word in x.split() if word not in (stop)]))
    
    # ...
    bar_text_freq(tweets, 'tweet_without_stopwords', 20)
    stopwoorden = STOPWORDS
    tokenized_all = ' '.join(
        ' '.join(tt) for tt in tweets['tokenized_text'])

    # Get tweets by country.
    india = ' '.join(text for text in
                     tweets['text'][tweets['user_location'] == 'India'])
    china = ' '.join(text for text in
                     tweets['text'][tweets['user_location'] == 'China'])
    usa = ' '.join(text for text in tweets['text'][
        tweets['user_location'] == 'United States'])
    sa = ' '.join(text for text in tweets['text'][
        tweets['user_location'] == 'South Africa'])

    # Print the processed wordcloud.
    better_wordcloud(tweets, 'tokenized', stopwoorden)
