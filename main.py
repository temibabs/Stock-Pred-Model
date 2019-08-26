import argparse

# import keras
# from models import LSTM, SVM, LR
from data import *
import os

PRICE_API_KEY = '07AS57PI8CJAK06A'
NEWS_API_KEY = 'e9f86dd606b74d04a79a3fedda2bee3e'
def parse_args() -> argparse.Namespace:
    desc = 'Stock Prediction models implementations'
    parser = argparse.ArgumentParser(desc)
    parser.add_argument('--stock', type=str, default='AAPL', help='The stock to train/test for')
    parser.add_argument('--mode', type=str, default='train', help='Whether to train or test')
    parser.add_argument('--proxy', type=str, default='http://trendgate.interswitchng.com:8080',
                        help='Proxy Setting (for connection to the dataset)')

    arguments = parser.parse_args()
    return arguments


def main():
    pd.set_option('display.max_columns', 500)
    arguments = parse_args()
    # lstm_model = LSTM()
    # svm_model = SVM()
    # lr_model = LR()
    os.environ['HTTP_PROXY'] = arguments.proxy
    os.environ['HTTPS_PROXY'] = arguments.proxy
    data = Data(arguments.stock)
    dataset = data.get_whole_dataset()
    print(dataset.head())


if __name__ == '__main__':
    main()
