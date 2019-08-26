from typing import TextIO

import numpy as np
import pandas as pd
from newsapi import NewsApiClient

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from pyparsing import unicode

import main

import datetime
import requests
import json


class Data(object):
    def __init__(self, stock: str):
        self.stock = stock
        self.price_file_csv = 'temp_datasets/{}_price_datasets.csv'.format(self.stock)
        self.news_file_csv = 'temp_datasets/{}_news_datasets.csv'.format(self.stock)

        self.stock_dictionary = {
            'AAPL': 'Apple',
            'MSFT': 'Microsoft',
            'TSLA': 'Tesla',
            'NFLX': 'Netflix'
        }

        self.newsapi = NewsApiClient(api_key=main.NEWS_API_KEY)

    def get_price_data(self):
        with open(self.price_file_csv, 'w+') as f:
            csv_data = requests.get('https://www.alphavantage.co/query?'
                                    'function=TIME_SERIES_DAILY_ADJUSTED'
                                    '&symbol={}'
                                    '&apikey={}'
                                    '&outputsize=compact'
                                    '&datatype=csv'
                                    .format(self.stock, main.PRICE_API_KEY)).text
            f.write(csv_data)

    def get_news_data(self):
        dict_data = self.newsapi.get_everything(q=self.stock_dictionary[self.stock],
                                                sources='bbc-news,'
                                                        'the-verge,'
                                                        'business insider,'
                                                        'techcruch,'
                                                        'bloomberg,'
                                                        'info money',
                                                from_param='2019-07-25',
                                                to='2019-08-24',
                                                page_size=100,
                                                page=1)

        news = []
        for i in range(len(dict_data['articles'])):
            d = {}
            date = dict_data['articles'][i]['publishedAt']
            title = dict_data['articles'][i]['title']
            description = dict_data['articles'][i]['description']
            text = '{}. {} '.format(title, description)
            d['text'] = text.encode('utf-8', 'ignore')
            d['date'] = date
            news.append(d)

        keys = news[0].keys()
        with open(self.news_file_csv, 'w+') as file:
            writer = csv.DictWriter(file, keys)
            writer.writeheader()
            writer.writerows(news)

    def get_whole_dataset(self):
        # self.get_price_data()
        # self.get_news_data()

        df_prices = pd.read_csv(self.price_file_csv)
        df_prices.rename(columns={'timestamp': 'date'},
                         inplace=True)

        df_articles = pd.read_csv(self.news_file_csv)
        df_articles['date'] = df_articles['date'].apply(lambda x: x[:10])

        return pd.merge(df_prices, df_articles, how='outer')
