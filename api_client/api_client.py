

import requests
import pandas as pd
from TwitterAPI import TwitterAPI, TwitterPager

# lauren's keys
access_token_key = "1078387516149981184-EAwOFfwflefT4jwNmEY2cT5GPVjWyv"
access_token_secret = "5aRmDk8oAwEWpRrr09BRKjxMJVkYSl3pjR4AD4MXVHAPy"
consumer_key = "Lx98duo9bsbCj5iL5CkXt5xvz"
consumer_secret = "V0MxMWWsApcI2t4Ul5DxJD0yDZ0EurMyPAcvLZ5zWiVJ7UDWfT"

# build the Twitter api object and pager object
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

# 'wild pigs', 'wild hogs', 'feral swine'
r = TwitterPager(api, 'tweets/search/fullarchive/:pig', {'query': 'wild pigs',
                                                         'maxResults': 500,
                                                         'fromDate': '201910270000',
                                                         'toDate': '201910280000',
                                                         })
# free version here
# r = api.request('search/tweets', {'q': 'trump',
#                                  'tweet_mode': 'extended',
#                                  'max_results': 100})

results = {
    'created_at': [],
    'text': [],
    'user_loc': [],
    'user_desc': [],
    'coords': [],
    'geo': [],
    'place': [],
    'retweet': [],
    'truncated': [],
    'hashtags': [],
    'user_mentions_screen_name': [],
    'user_mentions_name': [],
    'source': [],
    'user_id': [],
    'user_name': [],
    'user_followers_count': [],
    'user_friends_count': [],
    'user_listed_count': [],
    'user_created_at': [],
    'user_favourites_count': [],
    'user_utc_offset': [],
    'user_time_zone': [],
    'user_geo_enabled': [],
    'user_verified': [],
    'user_statuses_count': [],
    'user_lang': [],
    'user_following': [],
    'contributors': [],
    'is_quote_status': [],
    'retweet_count': [],
    'favorite_count': [],
    'favorited': [],
    'retweeted': [],
    'lang': []
}

'''
for item in r.get_iterator():
    result = None
    print('%%%%%%%%%%%%%%%%')
    result = item['text']
    try:
        result = item['extended_tweet']['full_text']
    except: 
        pass
    try:
        result = item['retweeted_status']['extended_tweet']['full_text']
    except:
        pass
    print(result)
    print('$$$$$$$$$$$$')
    print('')
'''

i = 1
for item in r.get_iterator():
    results['created_at'].append(item['created_at'])

    try:
        text = item['text']
    except:
        text = None
    # extended tweet available, use it
    try:
        text = item['extended_tweet']['full_text']
    except:
        pass
    # if retweet full text available use it
    try:
        text = item['retweeted_status']['extended_tweet']['full_text']
    except:
        pass
    results['text'].append(text)
    results['user_loc'].append(item['user']['location'])
    results['user_desc'].append(item['user']['description'])
    results['coords'].append(item['coordinates'])
    results['geo'].append(item['geo'])
    results['place'].append(item['place'])
    results['retweet'].append('retweeted_status' in list(item.keys()))
    if 'retweeted_status' in list(item.keys()):
        try:
            results['full_text'] = item['retweeted_status']['full_text']
        except:
            pass

    results['truncated'].append(item['truncated'])
    results['hashtags'].append(item['entities']['hashtags'])
    if len(item['entities']['user_mentions']) > 0:
        results['user_mentions_screen_name'].append(item['entities']['user_mentions'][0]['screen_name'])
        results['user_mentions_name'].append(item['entities']['user_mentions'][0]['name'])
    else:
        results['user_mentions_screen_name'].append(None)
        results['user_mentions_name'].append(None)
    results['source'].append(item['source'])
    results['user_id'].append(item['user']['id'])
    results['user_name'].append(item['user']['name'])
    results['user_followers_count'].append(item['user']['followers_count'])
    results['user_friends_count'].append(item['user']['friends_count'])
    results['user_listed_count'].append(item['user']['listed_count'])
    results['user_created_at'].append(item['user']['created_at'])
    results['user_favourites_count'].append(item['user']['favourites_count'])
    results['user_utc_offset'].append(item['user']['utc_offset'])
    results['user_time_zone'].append(item['user']['time_zone'])
    results['user_geo_enabled'].append(item['user']['geo_enabled'])
    results['user_verified'].append(item['user']['verified'])
    results['user_statuses_count'].append(item['user']['statuses_count'])
    results['user_lang'].append(item['user']['lang'])
    results['user_following'].append(item['user']['following'])
    results['contributors'].append(item['contributors'])
    results['is_quote_status'].append(item['is_quote_status'])
    results['retweet_count'].append(item['retweet_count'])
    results['favorite_count'].append(item['favorite_count'])
    results['favorited'].append(item['favorited'])
    results['retweeted'].append(item['retweeted'])
    results['lang'].append(item['lang'])


results_df = pd.DataFrame(results)
results_df.to_csv('results.csv', index=False)
