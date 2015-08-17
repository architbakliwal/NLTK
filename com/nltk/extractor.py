'''
Created on Aug 14, 2015

@author: n553721
'''
import json

with open('positive_tweets.json') as data_file:
    pos_data = json.load(data_file)
# print(data[0]['text'])
tweets = []
pos_tweets = []
for tweet in pos_data:
    tweets.append(((tweet['text'].replace(")", "").replace("(", "")), 'positive'))

with open('negative_tweets.json') as data_file:
    neg_data = json.load(data_file)
# print(data[0]['text'])
neg_tweets = []
for tweet in neg_data:
    tweets.append(((tweet['text'].replace(")", "").replace("(", "")), 'negative'))
#     tweets.append((re.escape(tweet['text'].replace(")", "").replace("(", "")), 'negative'))

try:
    fh = open("ptweets.txt", "w+", encoding='utf-8')
    string_ptweets = str(pos_tweets)
    string_ntweets = str(neg_tweets)
    string_tweets = string_ptweets + string_ntweets
    string_tweets = str(tweets)
    fh.write(string_tweets)
#     print(text)
except Exception as e:
    print(type(e))
    print(e.args)
finally:
    print("Closing the file")
    fh.close()