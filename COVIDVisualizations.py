import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

import seaborn as sns



from datetime import datetime as dt

os.chdir(r"****")

tweets = pd.read_csv("tweets_final.csv")
tweets = tweets.drop(columns=['Unnamed: 0'])
tweets.created_at = pd.to_datetime(tweets.created_at)

stocks = pd.read_csv("yahoo_fin_full.csv")
stocks.rename(columns={'Symbol':'symbol'}, inplace=True)
stocks = stocks.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])

symbols = pd.read_csv("stocksymbols_full.csv")


stock_data = stocks.merge(symbols)
stock_data.to_csv("fin_full.csv")



#Set data types of columns
stock_data.rename(columns={'Date':'date', 'Open':'open', 'High':'high',
                           'Low':'low', 'Close*':'close', 'Adj Close**': 'adj_close',
                           'Volume':'volume'}, inplace=True)

#Companies that have stock splits are causing huge drops in price that are not reflective of market conditions
stock_splits = stock_data[stock_data['open'].astype(str).str.contains('Split')].company_name.unique()

stock_data = stock_data[~stock_data['company_name'].isin(stock_splits)]

stock_data['date'] = pd.to_datetime(stock_data['date'])
stock_data['open'] = pd.to_numeric(stock_data['open'], errors='coerce')
stock_data['high'] = pd.to_numeric(stock_data['high'], errors='coerce')
stock_data['low'] = pd.to_numeric(stock_data['low'], errors='coerce')
stock_data['close'] = pd.to_numeric(stock_data['close'], errors='coerce')
stock_data['adj_close'] = pd.to_numeric(stock_data['adj_close'], errors='coerce')
stock_data['volume'] = pd.to_numeric(stock_data['volume'], errors='coerce')

tweets['created_at'] = pd.to_datetime(tweets['created_at'].dt.strftime('%Y-%m-%d'))
os.chdir(r".\Visualizations")

sns.set_palette("Accent")
#Overall sentiment over time
avg_sent = tweets[['created_at', 'sentiment_compound']].groupby(['created_at']).mean()
plot = sns.lineplot(data=avg_sent)
plot.set(xlabel='Date', ylabel='Average Sentiment', title='Average Political Sentiment')
#plt.show()
fig = plot.get_figure()
fig.set_size_inches(12, 8)
fig.savefig('overall_sentiment.png', dpi=300)
plt.clf()

#Dot Plot w/trendline
trend_sent = avg_sent
trend_sent = trend_sent.reset_index()

plot = sns.regplot(data=trend_sent, x=test.index, y='sentiment_compound')
plot.set(title='Trend of Average Political Sentiment')
fig = plot.get_figure()
fig.savefig('overall_sentiment_trend.png', dpi=300)
plt.clf()

#By Party
sent = tweets[['created_at', 'sentiment_compound', 'party']]
combo_sent = pd.melt(sent, id_vars=['created_at', 'party'], value_vars=['sentiment_compound']).groupby(['created_at', 'party']).mean().reset_index()
party_plot = sns.lineplot(x='created_at', y='value', data=combo_sent, palette=sns.color_palette("RdBu_r", 2), hue='party')
party_plot.set(xlabel='Date', ylabel='Average Sentiment', title='Average Political Sentiment By Political Party')
party_plot.set_xticklabels(party_plot.get_xticklabels(), rotation=45)
plt.show()
fig = party_plot.get_figure()
fig.set_size_inches(12, 8)
fig.savefig('overall_sentiment_party.png', dpi=300)
plt.clf()

#Party trends
party_trend = combo_sent
party_trend['index1'] = party_trend.index
party_trend.columns = ['created_at', 'party', 'average_sentiment', 'index', 'index1']
plot = sns.lmplot(data=party_trend, x='index1', y='average_sentiment', hue='party', col='party')
plot.set(xlabel='')
plt.show()
f.savefig("party_trend.png", dpi=300)
plt.clf()

#Individuals
authors = tweets[['created_at', 'screen_name', 'sentiment_compound', 'party']]
for author in authors.screen_name.unique():
    data = authors[authors.screen_name == author]
    if (data.party == 'Republican').sum() > 0:
        sns.set_palette("Reds")
    else:
        sns.set_palette("Blues")  
    plot = sns.lineplot(x='created_at', y='sentiment_compound', data=data, ci=None)
    plot.set(xlabel='Date', ylabel='Average Sentiment', title = 'Average Political Sentiment By Author: '+author)
    fig = plot.get_figure()
    fig.set_size_inches(12, 8)
    fig.savefig('overall_sentiment_'+author+'.png', dpi=300)
    plt.clf()

sns.set_palette("Greens_d")

#Plotting financial data
#Average closing price
stock_copy = stock_data[['date', 'adj_close', 'symbol', 'company_name', 'sector', 'industry']]
avg_close = stock_copy.groupby(['date']).mean()
ax = sns.lineplot(data=avg_close)
ax.set(xlabel='Date', ylabel='Average Adj. Close Price ($)', title='Average Adj. Closing Price Across All Four Sectors')
fig = ax.get_figure()
fig.set_size_inches(12, 8)
fig.savefig('average_stockclose.png', dpi=300)
plt.clf()


#Closing price by sector
for sector in stock_data.sector.unique():
    os.chdir(r".\\"+sector)
    data = stock_data[stock_data.sector==sector][['date', 'adj_close', 'symbol', 'company_name', 'sector', 'industry']]
    sector_data = data.groupby(['date']).mean()
    plot = sns.lineplot(data=sector_data)
    plot.set(xlabel='Date', ylabel='Average Adj. Close Price ($)', title = 'Average Adj. Closing Price By Sector: ' + sector)
    fig = plot.get_figure()
    fig.set_size_inches(12, 8)
    fig.savefig('avg_adjclose_'+sector+'.png', dpi=300)
    plt.clf()
    for industry in data.industry.unique():
        ind_data = data[data.industry==industry].groupby(['date']).mean()
        plot = sns.lineplot(data=ind_data)
        plot.set(xlabel='Date', ylabel='Average Adj. Close Price ($)', title = 'Average Adj. Closing Price: '+sector+', '+industry)
        plt.show()
        fig = plot.get_figure()
        fig.set_size_inches(12, 8)
        fig.savefig('avg_adjclose_'+sector+"_"+industry+'.png', dpi=300)
        plt.clf()
    os.chdir(r"..\\")

sns.set_palette("hls")
#Line plot w/sectors
plot = sns.lineplot(data = stock_data, x='date', y='adj_close', hue='sector', ci=None)
plot.set(xlabel='Date', ylabel='Average Adj. Close Price ($)', title = 'Average Adj. Closing Price By Sector')
plot.legend(loc='upper center')
#plt.show()
fig = plot.get_figure()
fig.set_size_inches(12, 8)
fig.savefig('avg_adjclose_sector.png', dpi = 300)
plt.clf()

pct_changes = pd.DataFrame(columns=['sector', 'industry', 'start', 'end', 'min', 'pct_change', 'recovery'])
for sec in stock_data.sector.unique():
    data = stock_data[stock_data.sector==sec]
    for ind in data.industry.unique():
        ind_data = data[stock_data.industry==ind].groupby(['date']).mean()
        start = ind_data.adj_close[0]
        end = ind_data.adj_close[len(ind_data)-1]
        min_price = ind_data.adj_close.min()
        pct_change = ((end - start)/start)*100
        recovery = ((end-min_price)/(start-min_price))*100
        new_row = pd.DataFrame.from_records([{'sector': sec, 'industry': ind, 'start':start, 'end':end, 'min':min_price, 'pct_change':pct_change, 'recovery':recovery}])
        pct_changes = pct_changes.append(new_row)

os.chdir(r'..\\')
pct_changes.to_csv("ind_pct_changes.csv")

#Most companies in Apparel manufacturing don't have data for the 24th, causing a significant drop

#Plotting histograms of all NRC Emotions


nrc_data = tweets[['fear_std', 'anger_std', 'sad_std', 'disgust_std', 
                   'anticip_std', 'trust_std', 'surprise_std', 'joy_std']]

os.chdir(r".\Visualizations")

f, axes = plt.subplots(4, 2, figsize=(7, 7), sharex=True, sharey=True)
f.suptitle('NRC Emotion Distribution')

sns.distplot(nrc_data.fear_std, ax=axes[0,0], kde=False)
sns.distplot(nrc_data.anger_std, ax=axes[0,1], kde=False)
sns.distplot(nrc_data.sad_std, ax=axes[1,0], kde=False)
sns.distplot(nrc_data.disgust_std, ax=axes[1,1], kde=False)
sns.distplot(nrc_data.anticip_std, ax=axes[2,0], kde=False)
sns.distplot(nrc_data.trust_std, ax=axes[2,1], kde=False)
sns.distplot(nrc_data.surprise_std, ax=axes[3,0], kde=False)
sns.distplot(nrc_data.joy_std, ax=axes[3,1], kde=False)

f.savefig('NRC_Emotions.png', dpi=300)
plt.clf()

#Distribution of Sentiment Analysis Compound Scores
#Afinn_std, nrc_sentiment, vader_compound, textblob_polarity, sentiment_compound
f, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True, sharey=True)
f.suptitle('Distribution of Standardized Sentiment Analysis Scores by Lexicon')

sns.distplot(tweets.afinn_std, ax=axes[0,0], kde=False)
sns.distplot(tweets.nrc_sentiment, ax=axes[0,1], kde=False)
sns.distplot(tweets.vader_compound_std, ax=axes[1,0], kde=False)
sns.distplot(tweets.textblob_polarity_std, ax=axes[1,1], kde=False)
#plt.show()
f.savefig('Score_Distribution.png', dpi=300)

#Distribution of compound sentiment
plot = sns.distplot(tweets.sentiment_compound, kde=False)
fig = plot.get_figure()
fig.suptitle('Distribution of Compound Sentiment Scores')
#plt.show()
fig.savefig('Compound_Sentiment_Dist.png', dpi=300)
