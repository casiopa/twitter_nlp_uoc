"""General functions of sentiment_analyzer package"""

import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time


# VARIABLES

PLOT_COLORS = ['red', 'green']

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
             'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
             'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
             'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
             'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
             'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
             'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
             'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
             'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
             'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
             'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
             'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']


# FUNCTIONS

def preprocess_text(txt: str) -> str:
    """
    Clean text removing urls and non-alphanumeric characters, and lowercase it.
    :param txt: text to be clean
    :return: cleaned text
    """
    # remove urls
    cleaned_text = re.sub(r'\bhttps?:[\-\w~./]*\b', '', txt)

    # remove not alphanumeric chars
    cleaned_text = re.sub(r"[^\w \t\r\n]+", "", cleaned_text)

    # remove more than one space
    cleaned_text = re.sub(r"[\n\r\t\s]+", " ", cleaned_text)

    return cleaned_text.lower()


def remove_stopwords(txt: str, stopwords: list[str] = STOPWORDS) -> str:
    """
    Remove words in stopword list from text
    :param txt: the text to be cleaned
    :param stopwords: list of tokens to remove from txt
    :return: text without stopwords
    """
    return ' '.join([word for word in txt.split(' ') if word not in stopwords])


def preprocess_data(data: list[dict]) -> list[dict]:
    """
    Clean and remove stopwords from texts in value of key 'text' in a list of dicts
    :param data: list of dictionaries, keys: words, values: count
    :return: list of dictionaries
    """
    for d in data:
        d['text'] = remove_stopwords(preprocess_text(d['text'])).strip()

    return data


def create_bows_vocab(data: list[dict]) -> (list[dict], list):
    """
    Create 2 elements a BoW for texts in dictionaries and a vocabulary
    Number of total BoWs to process will be printed and
    four intermediate prints will show time of execution elapsed.
    :param data: list of dictionaries with texts under key 'text'
    :return: a list of dictionary with a BagOfWords for each text and a list with vacabulary
    """
    bows = []
    vocab = set()

    print(f"\tINFO: Total bows to process: {len(data)}")
    start_time = time.time()

    for counter, d in enumerate(data, start=1):
        words = d['text'].split(' ')
        bows.append(dict(Counter(words)))
        vocab = vocab.union(set(words))
        if counter % (len(data)/4) == 0:
            t = time.time()-start_time
            print(f"\tINFO: Processing bow {counter:>6} - Time elapsed: {t:.3f} seconds")

    return bows, sorted(list(vocab))


def join_dicts_bows(dicts: list[dict], bows: list[dict]) -> pd.DataFrame:
    """
    Insert a new variable BagOfWords as a column in a dataset
    :param dicts: list of dicts with a text key
    :param bows: list of dicts. Each dictionary is a BoW from the text
    :return: pd.DataFrame with records from list of dicts and new variable bows
    """
    df = pd.DataFrame.from_dict(dicts)
    df['bow'] = bows
    return df


def create_cluster_bow(df: pd.DataFrame, cluster: int) -> pd.Series:
    """
    Create a Series with sorted Bag of Words for all texts df's column text
    :param df: dataframe with text and sentiment columns
    :param cluster: category for sentiment column
    :return: pd.Series with a Bag of Words from all texts in df's text column
    """
    union_text = [" ".join(txt for txt in df[df.sentiment == cluster].text)][0]
    words = union_text.split(" ")
    bow = pd.Series(Counter(words)).sort_values(ascending=False)
    return bow


def paint_2word_clouds(df: pd.DataFrame, stopwords: list[str] = STOPWORDS) -> None:
    """
    Paint one image with a wordcloud per each cluster.
    The function paints one graph in a pop-up and save a png image in images subfolder
    :param df: DataFrame with sentiment (cluster) and text columns
    :param stopwords: list of tokens to remove from wordclud
    :return: None
    """
    clusters = df.sentiment.unique()
    wordclouds = []
    for cluster in clusters:
        txt = " ".join(text for text in df[df.sentiment == cluster].text)
        wordclouds.append(WordCloud(stopwords=set(stopwords)).generate(txt))

    fig, axes = plt.subplots(nrows=2, ncols=1)

    for i in range(len(clusters)):
        axes[i].imshow(wordclouds[i], interpolation='bilinear')
        axes[i].set_title(f'WordCloud Cluster {clusters[i]}')
        axes[i].axis("off")

    fig.tight_layout(pad=2)
    plt.show()


def paint_2bars(df: pd.DataFrame, max_tokens: int = 20, colors: list = PLOT_COLORS) -> None:
    """
    Paint one image with a bar graph of most frequent tokens per each cluster.
    The function paints one graph in a pop-up and save a png image in images subfolder
    :param df: dataframe with sentiment (cluster) and text columns
    :param max_tokens: number of tokens that will be represented in the bar grapha
    :param colors: a list with colors for each cluster
    :return: None
    """
    clusters = df.sentiment.unique()
    bows = []
    for cluster in clusters:
        bows.append(create_cluster_bow(df, cluster))

    fig, axes = plt.subplots(nrows=2, ncols=1, constrained_layout=True)

    for i in range(len(clusters)):
        bows[i][:max_tokens].plot(ax=axes[i], kind='bar', color=colors[i])
        axes[i].set_title(f'{max_tokens} More frequent tokens in cluster {clusters[i]}')
        axes[i].tick_params(axis='x', labelrotation=75)
    plt.show()
