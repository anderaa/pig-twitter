
import pandas as pd
import os


def get_sample(direc='data_raw/', sample_rate=0.2, drop_rt=True, shuffle=True):
    """
    Generates a sample of data that can be labeled.
    :param direc: Directory containing files from which to sample data.
    :param sample_rate: The fraction of tweets to draw from each file.
    :param drop_rt: Should retweets be dropped?
    :return: A combined dataframe of the sample data.
    """

    files = os.listdir(direc)
    files = [f for f in files if '.csv' in f]

    df_sample_list = []

    for file in files:
        df = pd.read_csv(direc + file)

        if drop_rt:
            df = df.loc[df['retweet'] == False, :]

        df = df.sample(frac=sample_rate)

        df['filename'] = file
        df['search_string'] = file.split('_')[1]

        df_sample_list.append(df)

    df_sample_comb = pd.concat(df_sample_list)

    df_sample_comb['created_at'] = pd.to_datetime(df_sample_comb['created_at'])
    df_sample_comb['class'] = np.nan

    df_sample_comb = df_sample_comb.loc[np.logical_and(df_sample_comb['created_at'].dt.year == 2019,
                                                       df_sample_comb['created_at'].dt.month >= 3), :]

    if shuffle:
        df_sample_comb = df_sample_comb.sample(frac=1).reset_index(drop=True)

    return df_sample_comb


# df_sample = get_sample(direc='data_raw/', sample_rate=0.1, drop_rt=True, shuffle=True)
# if 'df_sample_recent.csv' in os.listdir():
#     raise Exception('Will not overwrite existing file of same name. Please change something before writing to disk.')
# else:
#     df_sample.to_csv('df_sample_november.csv', index=False)
