import sys
import os
import pandas as pd
import json
from utils import DATA_PATH, INPUT_FILE, PROCESSED_FILE, MENU, \
                  stop_between_steps, preprocess_data, create_bows_vocab, join_dicts_bows, paint_2word_clouds, \
                  paint_2bars, create_cluster_bow


if __name__ == '__main__':

    print(MENU)
    option = int(input('Select 0, 1, 2, 3 ó 4: '))
    # option = 3
    while option not in range(5):
        option = int(input(f'{option} is not a valid option. Please, select 0-4: '))

    if option == 0:
        sys.exit("Abort PEC's execution.")

    if option in [1, 2]:

        # EXERCISE 1
        exercise = 1
        print('INFO EX 1: Start reading data')
        dicts_tweets = pd.read_csv(os.path.join(DATA_PATH, INPUT_FILE)).to_dict('records')
        print(f'First 5 dicts (of {len(dicts_tweets)} total dicts): {json.dumps(dicts_tweets[:5], indent=2)}\n')

        exercise = stop_between_steps(option, exercise)

        # EXERCISE 2
        print('INFO EX 2: Start cleaning data')
        clean_dicts_tweets = preprocess_data(dicts_tweets[:100] + dicts_tweets[-100:])
        print(f"Last 5 dicts (of {len(clean_dicts_tweets)}): {json.dumps(clean_dicts_tweets[-5:], indent=2)}\n")

        exercise = stop_between_steps(option, exercise)

        # EXERCISE 3
        print('INFO EX 3: Start BoWs')
        list_bows, vocabulary = create_bows_vocab(clean_dicts_tweets)
        print(f'First 5 bows (of {len(list_bows)} total bows): {json.dumps(list_bows[:5], indent=2)}')
        print(f'First 10 words of vocabulary (of {len(vocabulary)} total unique words): {vocabulary[:10]}\n')

        exercise = stop_between_steps(option, exercise)

        # EXERCISE 4
        print('INFO EX 4: Start joining and writing BoWs')
        df_tweets = join_dicts_bows(clean_dicts_tweets, list_bows)
        print(f"Record 20 (index 19): {df_tweets.to_dict('records')[19]}")
        df_tweets.to_csv(os.path.join(DATA_PATH, PROCESSED_FILE), index=False)
        print(PROCESSED_FILE, ' file wrote.\n')

        # clean memory
        del dicts_tweets, clean_dicts_tweets, list_bows, vocabulary, df_tweets

        exercise = stop_between_steps(option, exercise)

    if option in range(1, 5):

        # EXERCISE 5
        exercise = 5
        print('INFO EX 5: Data Analysis - Word clouds')
        df_processed = pd.read_csv(os.path.join(DATA_PATH, PROCESSED_FILE))
        print(f'Answer EX 5.1: The processed dataset has {df_processed.sentiment.nunique()} clusters')
        n_nulls = df_processed[df_processed.text == ''].shape[0]
        print(f'Answer EX 5.2: There are {n_nulls}, {n_nulls / df_processed.shape[0]:.2%} tweets without text variable')
        print('Answer EX 5.3: Printing word clouds in pop-up\n')
        paint_2word_clouds(df_processed)

        exercise = stop_between_steps(option, exercise)

        # EXERCISE 6
        print('INFO EX 6: Data Analysis - Bows Bars')
        paint_2bars(df_processed, max_tokens=25)

        exercise = stop_between_steps(option, exercise)

        # EXERCISE 7
        print('INFO EX 7: Data Analysis - Conclusions')
        postive_bow = create_cluster_bow(df_processed, 4)
        negative_bow = create_cluster_bow(df_processed, 0)
        intersection_words = set(postive_bow.index).intersection(set(negative_bow.index))
        print(f'\ta. The most frequent positive words are: {list(postive_bow.index)[:10]}')
        print(f'\tb. The most frequent negative words are: {list(negative_bow.index)[:10]}')
        print(f"""\tc. There are {len(intersection_words)} words in both positive and negative tweets.
        For example: {list(intersection_words)[:10]}""")
        print(f"""\td. We can see very positive words in the WordCloud por cluster 4, like: good, fun, nice.
        And we can also see negative words for for cluster 0, like: sad, hate, sorry, need.
        I think tokens need more preprocess but we can see the positive-negative tendency of the clusters.\n""")


print('End execution PEC 4 - Ana Blanco - Twitter NLP')
