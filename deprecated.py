def csv_to_dicts(filename: str) -> list[dict]:
    """
    Load data from csv file in DATA_PATH
    :param filename: name of the csv file
    :return: list of dictionaries
    """
    df = pd.read_csv(os.path.join(data_path, filename))
    return df.to_dict('records')


def csv_to_df(filename):
    """
    Load data from csv file in DATA_PATH
    :param filename: name of the csv file
    :return: pandas DataFrame
    """
    df = pd.read_csv(os.path.join(data_path, filename))
    return df


def write_csv(df, filename):
    """

    :param df:
    :param filename:
    """
    df.to_csv(os.path.join(data_path, filename), index=False)


def paint_bars(series, cluster):
    series[:25].plot.bar()
    # plt.bar(series[:30])
    plt.title(f'Histogram Cluster {cluster}')
    plt.show(block=True)


def paint_word_cloud(df, cluster):
    """

    :param df:
    :param cluster:
    :return:
    """
    txt = " ".join(text for text in df[df.sentiment == cluster].text)

    # Create and generate a word cloud image:
    wordcloud = WordCloud().generate(txt)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'Word cloud Cluster {cluster}')
    plt.axis("off")
    plt.show(block=True)
