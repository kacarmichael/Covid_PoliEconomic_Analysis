import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math

from afinn import Afinn
from nrclex import NRCLex
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

from sklearn import preprocessing

#Import separate csv files and compile into one
os.chdir(r"C:\Users\Aaron\Google Drive\School Stuff\Summer 2020\Project\tweets")

file_list = os.listdir()

tweets = pd.read_csv(file_list[0])

for i in range(1, len(file_list)):
    tweets = pd.concat([tweets, pd.read_csv(file_list[i])], axis=0, ignore_index=True)

#The script pulled tweets based on time, which included duplicate tweets, this drops them based on id
tweets = tweets.drop_duplicates(subset=['status_id'])

#The Twitter API returns 90 columns, most of which are irrelevant to this project
tweet_df = tweets[['created_at', 'screen_name', 'text', 'favorite_count', 'retweet_count', 'quote_count', 'reply_count', 'hashtags', 'quoted_text', 'retweet_text']]

#Resets the index after dropping duplicates
tweet_df.index = range(0, len(tweet_df))

#Assign Rep/Dem label
r = ['GOPLeader', 'senatemajldr', 'realDonaldTrump']
d = ['AOC', 'AyannaPressley', 'BernieSanders', 'JoeBiden', 'Ilhan', 'SpeakerPelosi', 'RashidaTlaib', 'SenSchumer']
tweet_df['party'] = ''

for i in range(0, len(tweet_df)):
    if(tweet_df.screen_name[i] in r):
        tweet_df.party[i] = "Republican"
    else:
        tweet_df.party[i] = "Democrat"

#Analysis w/Afinn lexicon
af = Afinn()

af_scores_source = [af.score(tweet) for tweet in tweet_df.text]
af_category_source = ['positive' if score > 0
               else 'negative' if score < 0
               else 'neutral'
               for score in af_scores_source]

#Run analysis on quoted tweets and retweets
tweet_df.quoted_text = tweet_df.quoted_text.fillna('')

af_scores_quote = [af.score(tweet) for tweet in tweet_df.quoted_text]
af_category_quote = ['positive' if score > 0
               else 'negative' if score < 0
               else 'neutral'
               for score in af_scores_quote]

tweet_df.retweet_text = tweet_df.retweet_text.fillna('')

af_scores_retweet = [af.score(tweet) for tweet in tweet_df.retweet_text]
af_category_retweet = ['positive' if score > 0
               else 'negative' if score < 0
               else 'neutral'
               for score in af_scores_retweet]

tweet_df['afinn_source'] = af_scores_source
tweet_df['afinn_source_category'] = af_category_source
tweet_df['afinn_quote'] = af_scores_quote
tweet_df['afinn_quote_category'] = af_category_quote
tweet_df['afinn_retweet'] = af_scores_retweet
tweet_df['afinn_retweet_category'] = af_category_retweet

#Analysis w/NRC Lexicon
tweet_df['fear_score'] = np.nan
tweet_df['fear_freq'] = np.nan
tweet_df['anger_score'] = np.nan
tweet_df['anger_freq'] = np.nan
tweet_df['anticip_score'] = np.nan
tweet_df['anticip_freq'] = np.nan
tweet_df['trust_score'] = np.nan
tweet_df['trust_freq'] = np.nan
tweet_df['surprise_score'] = np.nan
tweet_df['surprise_freq'] = np.nan
tweet_df['pos_score'] = np.nan
tweet_df['pos_freq'] = np.nan
tweet_df['neg_score'] = np.nan
tweet_df['neg_freq'] = np.nan
tweet_df['sad_score'] = np.nan
tweet_df['sad_freq'] = np.nan
tweet_df['disgust_score'] = np.nan
tweet_df['disgust_freq'] = np.nan
tweet_df['joy_score'] = np.nan
tweet_df['joy_freq'] = np.nan

for i in range(0, len(tweet_df.text)):
    tweet_nrc = NRCLex(tweet_df.text[i].lower())
    scores = tweet_nrc.raw_emotion_scores
    freq = tweet_nrc.affect_frequencies
    try:
        tweet_df.fear_score[i] = scores['fear']
        tweet_df.fear_freq[i] = freq['fear']
        tweet_df.anger_score[i] = scores['anger']
        tweet_df.anger_freq[i] = freq['anger']
        tweet_df.anticip_score[i] = scores['anticip']
        tweet_df.anticip_freq[i] = freq['anticip']
        tweet_df.trust_score[i] = scores['trust']
        tweet_df.trust_freq[i] = freq['trust']
        tweet_df.surprise_score[i] = scores['surprise']
        tweet_df.surprise_freq[i] = freq['surprise']
        tweet_df.pos_score[i] = scores['positive']
        tweet_df.pos_freq[i] = freq['positive']
        tweet_df.neg_score[i] = scores['negative']
        tweet_df.neg_freq[i] = freq['negative']
        tweet_df.sad_score[i] = scores['sadness']
        tweet_df.sad_freq[i] = freq['sadness']
        tweet_df.disgust_score[i] = scores['disgust']
        tweet_df.disgust_freq[i] = freq['disgust']
        tweet_df.joy_score[i] = scores['joy']
        tweet_df.joy_freq[i] = freq['joy']
    except: 
        #Checks for exception if there is no score
        print("An exception occurred")

print("Missing values for fear: {x}".format(x = sum(1 for x in tweet_df['fear_score'] if math.isnan(x))))
print("Missing values for anger: {x}".format(x = sum(1 for x in tweet_df['anger_score'] if math.isnan(x))))
print("Missing values for anticipation: {x}".format(x = sum(1 for x in tweet_df['anticip_score'] if math.isnan(x))))
print("Missing values for trust: {x}".format(x = sum(1 for x in tweet_df['trust_score'] if math.isnan(x))))
print("Missing values for surprise: {x}".format(x = sum(1 for x in tweet_df['surprise_score'] if math.isnan(x))))
print("Missing values for positive: {x}".format(x = sum(1 for x in tweet_df['pos_score'] if math.isnan(x))))
print("Missing values for negative: {x}".format(x = sum(1 for x in tweet_df['neg_score'] if math.isnan(x))))
print("Missing values for sadness: {x}".format(x = sum(1 for x in tweet_df['sad_score'] if math.isnan(x))))
print("Missing values for disgust: {x}".format(x = sum(1 for x in tweet_df['disgust_score'] if math.isnan(x))))
print("Missing values for joy: {x}".format(x = sum(1 for x in tweet_df['joy_score'] if math.isnan(x))))

#Analysis w/VADER lexicon
tweet_df['vader_positive'] = np.nan
tweet_df['vader_neutral'] = np.nan
tweet_df['vader_negative'] = np.nan
tweet_df['vader_compound'] = np.nan

vader_analyzer = SentimentIntensityAnalyzer()
for i in range(0, len(tweet_df.text)):
    scores = vader_analyzer.polarity_scores(tweet_df.text[i])
    tweet_df.vader_positive[i] = scores['pos']
    tweet_df.vader_neutral[i] = scores['neu']
    tweet_df.vader_negative[i] = scores['neg']
    tweet_df.vader_compound[i] = scores['compound']

#Analysis w/Textblob lexicon
tweet_df['textblob_polarity'] = np.nan
for i in range(0, len(tweet_df.text)):
    blob = TextBlob(tweet_df.text[i])
    tweet_df.textblob_polarity[i] = blob.sentiment.polarity

#Measure virality by the number of interactions
tweet_df['virality'] = tweet_df['favorite_count'].fillna(0) + tweet_df['retweet_count'].fillna(0) + tweet_df['quote_count'].fillna(0) + tweet_df['reply_count'].fillna(0)



os.chdir(r"..\\")
tweet_df.to_csv("tweets_sentiment_scores.csv")


tweet_df['index_col'] = tweet_df.index

afinn_scores = tweet_df[['index_col', 'created_at', 'screen_name', 'text', 'favorite_count', 'retweet_count', 'quote_count', 'reply_count', 'hashtags', 'quoted_text', 'retweet_text', 'afinn_source', 'afinn_source_category', 'afinn_quote', 'afinn_quote_category', 'afinn_retweet', 'afinn_retweet_category']]
afinn_scores.to_csv("tweets_AFINN.csv")

nrc_scores = tweet_df[['index_col', 'created_at', 'screen_name', 'text', 'favorite_count', 'retweet_count', 'quote_count', 'reply_count', 'hashtags', 'quoted_text', 'retweet_text','fear_score', 'fear_freq', 'anger_score', 'anger_freq', 'anticip_score',
       'anticip_freq', 'trust_score', 'trust_freq', 'surprise_score',
       'surprise_freq', 'pos_score', 'pos_freq', 'neg_score', 'neg_freq',
       'sad_score', 'sad_freq', 'disgust_score', 'disgust_freq', 'joy_score',
       'joy_freq']]
nrc_scores.to_csv("tweets_NRC.csv")

vader_scores = tweet_df[['index_col', 'created_at', 'screen_name', 'text', 'favorite_count', 'retweet_count', 'quote_count', 'reply_count', 'hashtags', 'quoted_text', 'retweet_text', 'vader_positive', 'vader_neutral', 'vader_negative', 'vader_compound']]
vader_scores.to_csv("tweets_VADER.csv")

textblob_scores = tweet_df[['index_col', 'created_at', 'screen_name', 'text', 'favorite_count', 'retweet_count', 'quote_count', 'reply_count', 'hashtags', 'quoted_text', 'retweet_text', 'textblob_polarity']]
textblob_scores.to_csv("tweets_TEXTBLOB.csv")

#Notes on missing values:
#Delete all tweets that do not have a score on any lexicon

afinn_null = afinn_scores[(afinn_scores.afinn_source == 0) & (afinn_scores.afinn_quote == 0) & (afinn_scores.afinn_retweet == 0)]
nrc_null = nrc_scores[pd.isnull(nrc_scores.fear_score)]
vader_null = vader_scores[(vader_scores.vader_positive == 0) & (vader_scores.vader_negative == 0)]
textblob_null = textblob_scores[(textblob_scores.textblob_polarity == 0)]

nrc_null.index = range(0, len(nrc_null))
#Find indexes of null values
null_idx = []
for i in range(0, len(nrc_null)):
    if(nrc_null.index_col[i] in afinn_null.index):
        if(nrc_null.index_col[i] in vader_null.index):
            if(nrc_null.index_col[i] in textblob_null.index):
                null_idx.append(nrc_null.index_col[i])

tweets_NoNull = tweet_df
for idx in null_idx:
    tweets_NoNull = tweets_NoNull.drop(idx)

tweets_NoNull.index = range(0, len(tweets_NoNull))
tweets_NoNull.to_csv("tweets_NoNull.csv")


#List of NRC Emotions:
#Fear
#Anger
#Sadness
#Disgust
#Anticipation
#Trust
#Surprise
#Joy

#Normalizing scores

#AFINN
afinn_source_std = preprocessing.minmax_scale(tweets_NoNull.afinn_source, feature_range=(-100,100))
#Not enough quote/retweet scores to scale

#NRC
fear_score_std = preprocessing.minmax_scale(tweets_NoNull.fear_score, feature_range=(0,100))
anger_score_std = preprocessing.minmax_scale(tweets_NoNull.anger_score, feature_range=(0,100))
sad_score_std = preprocessing.minmax_scale(tweets_NoNull.sad_score, feature_range=(0,100))
disgust_score_std = preprocessing.minmax_scale(tweets_NoNull.disgust_score, feature_range=(0,100))
anticip_score_std = preprocessing.minmax_scale(tweets_NoNull.anticip_score, feature_range=(0,100))
trust_score_std = preprocessing.minmax_scale(tweets_NoNull.trust_score, feature_range=(0,100))
surprise_score_std = preprocessing.minmax_scale(tweets_NoNull.surprise_score, feature_range=(0,100))
joy_score_std = preprocessing.minmax_scale(tweets_NoNull.joy_score, feature_range=(0,100))
pos_score_std = preprocessing.minmax_scale(tweets_NoNull.pos_score, feature_range=(0, 100))
neg_score_std = preprocessing.minmax_scale(tweets_NoNull.neg_score, feature_range=(0, 100))

nrc_sentiment = pos_score_std - neg_score_std
nrc_PosEmo = anticip_score_std + trust_score_std + surprise_score_std + joy_score_std
nrc_NegEmo = fear_score_std + anger_score_std + sad_score_std + disgust_score_std
nrc_EmoScore = nrc_PosEmo - nrc_NegEmo

#VADER
vader_pos_std = preprocessing.minmax_scale(tweets_NoNull.vader_positive, feature_range=(0, 100))
vader_neg_std = preprocessing.minmax_scale(tweets_NoNull.vader_negative, feature_range=(0, 100))
vader_neutral_std = preprocessing.minmax_scale(tweets_NoNull.vader_neutral, feature_range=(0, 100))
vader_compound_std = preprocessing.minmax_scale(tweets_NoNull.vader_compound, feature_range=(-100, 100))

#Textblob
textblob_polarity_std = preprocessing.minmax_scale(tweets_NoNull.textblob_polarity, feature_range=(-100, 100))

std_df = pd.DataFrame(data = {'afinn_std': afinn_source_std, 'fear_std': fear_score_std, 'anger_std': anger_score_std,
                              'sad_std': sad_score_std, 'disgust_std': disgust_score_std, 'anticip_std': anticip_score_std,
                              'trust_std': trust_score_std, 'surprise_std': surprise_score_std, 'joy_std': joy_score_std,
                              'pos_std': pos_score_std, 'neg_std': neg_score_std, 'nrc_sentiment': nrc_sentiment,
                              'nrc_PosEmo': nrc_PosEmo, 'nrc_NegEmo': nrc_NegEmo, 'nrc_EmoScore': nrc_EmoScore,
                              'vader_pos_std': vader_pos_std, 'vader_neg_std': vader_neg_std, 'vader_neutral_std': vader_neutral_std,
                              'vader_compound_std': vader_compound_std, 'textblob_polarity_std': textblob_polarity_std})

compound_scores = std_df[['afinn_std', 'nrc_sentiment', 'nrc_EmoScore', 'vader_compound_std', 'textblob_polarity_std']].copy()

compound_scores['sentiment_compound'] = compound_scores.mean(axis=1)

final_df = pd.concat([tweets_NoNull, std_df, compound_scores['sentiment_compound']], axis=1)

final_df.to_csv("tweets_final.csv")