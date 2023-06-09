import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# VARIABLES

PLOT_COLORS = ['red', 'green']

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
             'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
             'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these',
             'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
             'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
             'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
             'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
             'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
             'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
             'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']


# FUNCTIONS


def preprocess_text(txt: str) -> str:
    """
    Clean text removing urls and non ASCII characters, and lowercase it.
    :param txt: text to be clean
    :return: cleaned text
    """

    # remove urls
    cleaned_text = re.sub(r'\bhttps?:[\-\w~./]*\b', '', txt)

    # replace "'" for " "
    cleaned_text = cleaned_text.replace("'", " ")

    # remove no ASCII chars
    # cleaned_text = re.sub(r"[^\x00-\x7F]+", "", cleaned_text)
    # valid_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
    valid_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ[\\] s\t\n\r\x0b\x0c'
    cleaned_text = re.sub(f"[^{valid_chars}]+", "", cleaned_text)

    # remove more than one space
    cleaned_text = re.sub(r"[\n\r\t\s]+", " ", cleaned_text)

    return cleaned_text.lower()


def remove_stopwords(txt: str, stopwords: list[str] = STOPWORDS) -> str:
    """
    Remove words in stopword list from text
    :param txt: the text to be cleaned
    :param stopwords: list of words to eliminate from txt
    :return: text without stopwords
    """
    return ' '.join([word for word in txt.split(' ') if word not in stopwords])


def preprocess_data(data):
    """
    Clean and remove stopwords from texts in key 'text' in a list of dicts
    :param data:
    :return:
    """

    for d in data:
        cleaned_text = remove_stopwords(preprocess_text(d['text'])).strip()
        d['text'] = cleaned_text

    return data


def create_bows_vocab(data):
    """

    :param data:
    :return:
    """
    bows = []
    vocab = set()

    counter = 0
    for d in data:
        words = d['text'].split(' ')
        bows.append(dict(Counter(words)))
        vocab = vocab.union(set(words))
        # print(counter, words)
        counter += 1
    return bows, sorted(list(vocab))


def join_dicts_bows(dicts, bows):
    """

    :param dicts:
    :param bows:
    :return:
    """
    df = pd.DataFrame.from_dict(dicts)
    df['bow'] = bows
    return df


def create_cluster_bow(df, cluster):
    """

    :param df: dataframe with text and sentiment columns
    :param cluster: category for sentiment column
    :return: pandas series with a Bag of Words from all texts in df's text column
    """

    union_text = [" ".join(txt for txt in df[df.sentiment == cluster].text)][0]
    words = union_text.split(" ")
    bow = pd.Series(Counter(words)).sort_values(ascending=False)
    return bow


def paint_2word_clouds(df):
    clusters = df.sentiment.unique()
    wordclouds = []
    for cluster in clusters:
        txt = " ".join(text for text in df[df.sentiment == cluster].text)
        wordclouds.append(WordCloud().generate(txt))

    fig, axes = plt.subplots(nrows=2, ncols=1)

    for i in range(len(clusters)):
        axes[i].imshow(wordclouds[i], interpolation='bilinear')
        axes[i].set_title(f'WordCloud Cluster {clusters[i]}')
        axes[i].axis("off")

    fig.tight_layout(pad=2)
    plt.show()


def paint_2bars(df: pd.DataFrame, max_tokens: int = 25, colors: list = PLOT_COLORS) -> None:
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
