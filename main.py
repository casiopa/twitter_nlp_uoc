"""Main script of the project"""

import sys
import os
import pandas as pd
import sentiment_analyzer as sa


if __name__ == '__main__':

    print(sa.MENU)
    option = int(input('Select 0, 1, 2, 3 or 4: '))

    while option not in range(5):
        option = int(input(f'{option} is not a valid option. Please, select 0-4: '))

    if option == 0:
        sys.exit("Abort PEC's execution.")

    # PART 1: Load Data - Begin execution from INPUT_FILE
    if option in [1, 2]:

        if not sa.file_exists(sa.INPUT_FILE):
            sys.exit(f"""Abort PEC's PART 1 execution because there is not {sa.INPUT_FILE}.
Please copy {sa.INPUT_FILE} inside {sa.DATA_PATH} folder.""")

        # EXERCISE 1
        EXERCISE = 1
        dicts_tweets = pd.read_csv(os.path.join(sa.DATA_PATH, sa.INPUT_FILE)).to_dict('records')
        print(f"""EXERCISE 1: Load data - Reading data file
        First 5 dicts (of {len(dicts_tweets)} total dicts): {dicts_tweets[:5]}\n""")

        # Stop between steps if chosen by user
        EXERCISE = sa.stop_between_steps(option, EXERCISE)

        # EXERCISE 2
        print('EXERCISE 2: Load data - Starting cleaning data')
        clean_dicts_tweets = sa.preprocess_data(dicts_tweets[:1000] + dicts_tweets[-1000:])
        # clean_dicts_tweets = sa.preprocess_data(dicts_tweets)
        print(f"""\tINFO: Data cleaned
        First 5 dicts (of {len(clean_dicts_tweets)}): {clean_dicts_tweets[:5]}
        Last 5 dicts (of {len(clean_dicts_tweets)}): {clean_dicts_tweets[-5:]}\n""")

        # Stop between steps if chosen by user
        EXERCISE = sa.stop_between_steps(option, EXERCISE)

        # EXERCISE 3
        print('EXERCISE 3: Load data - Starting BoWs extraction')
        list_bows, vocabulary = sa.create_bows_vocab(clean_dicts_tweets)
        print(f'\tFirst 5 bows (of {len(list_bows)} total bows): {list_bows[:5]}')
        print(f'\tFirst 10 words of vocabulary (of {len(vocabulary)} total): {vocabulary[:10]}\n')

        # Stop between steps if chosen by user
        EXERCISE = sa.stop_between_steps(option, EXERCISE)

        # EXERCISE 4
        print('EXERCISE 4: Load data - Starting joining and writing BoWs')
        df_tweets = sa.join_dicts_bows(clean_dicts_tweets, list_bows)
        print(f"\tRecord 20 (index 19): {list(df_tweets.to_dict('records'))[19]}")
        df_tweets.to_csv(os.path.join(sa.DATA_PATH, sa.PROCESSED_FILE), index=False)
        print(f'\tINFO: {sa.PROCESSED_FILE} file wrote.\n')

        # clean memory
        del dicts_tweets, clean_dicts_tweets, list_bows, vocabulary, df_tweets

        # Stop between steps if chosen by user
        EXERCISE = sa.stop_between_steps(option, EXERCISE)

    # PART 2: Data Analysis - Begin execution from PROCESSED_FILE
    if option in range(1, 5):

        if not sa.file_exists(sa.PROCESSED_FILE):
            sys.exit(f"""Abort PEC's PART 2 execution because there is not {sa.PROCESSED_FILE}.
Please run PEC's with options 1 or 2 to generate it or download it from repository: 
https://github.com/casiopa/twitter_nlp_uoc/tree/main/data.""")

        # EXERCISE 5
        EXERCISE = 5
        # print('EXERCISE 5: Data Analysis - Word clouds')
        df_processed = pd.read_csv(os.path.join(sa.DATA_PATH, sa.PROCESSED_FILE))
        n_nulls = df_processed[df_processed.text.isna()].shape[0]
        df_processed = df_processed[df_processed.text.notna()]
        print(f"""EXERCISE 5: Data Analysis - Word clouds
        5.1: The processed dataset has {df_processed.sentiment.nunique()} clusters
        5.2: There are {n_nulls}, {n_nulls / df_processed.shape[0]:.2%} tweets without text variable
        5.3: Printing word clouds in pop-up\n""")
        sa.paint_2word_clouds(df_processed)

        # Stop between steps if chosen by user
        EXERCISE = sa.stop_between_steps(option, EXERCISE)

        # EXERCISE 6
        print("""EXERCISE 6: Data Analysis - BoWs Bars
        Printing bar graph in pop-up\n""")
        sa.paint_2bars(df_processed)

        # Stop between steps if chosen by user
        EXERCISE = sa.stop_between_steps(option, EXERCISE)

        # EXERCISE 7
        # print('EXERCISE 7: Data Analysis - Conclusions')
        POSITIVE_BOW = sa.create_cluster_bow(df_processed, 4)
        NEGATIVE_BOW = sa.create_cluster_bow(df_processed, 0)
        n_intersection_words = len(set(POSITIVE_BOW.index).intersection(set(NEGATIVE_BOW.index)))
        intersection_best = set(POSITIVE_BOW.index[:50]).intersection(set(NEGATIVE_BOW.index[:50]))
        print(f"""EXERCISE 7: Data Analysis - Conclusions
        a.  The most frequent positive words are: {list(POSITIVE_BOW.index)[:10]}
        b.  The most frequent negative words are: {list(NEGATIVE_BOW.index)[:10]})
        c.  There are {n_intersection_words} words in both positive and negative tweets.
        \tFor example: {list(intersection_best)[:10]}
        d.  We can see very positive words in the WordCloud por cluster 4, like: good, love, thanks, lol.
        \tAnd we can also see words that can't be condsidered negative for cluster 0 as: work, dont, cant, back.
        \tApparently, tokens need more preprocesing but we can see the positive-negative tendency of the clusters.
        """)


print('End execution PEC 4 - Ana Blanco - Twitter NLP')
