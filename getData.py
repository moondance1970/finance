# https://fmpcloud.io/api/v3/income-statement/AAPL?period=quarter&apikey=18bb80696ecc77ff0ebaf2056f075aad
# https://fmpcloud.io/api/v3/historical-price-full/AAPL?serietype=line&apikey=18bb80696ecc77ff0ebaf2056f075aad
import json
import requests
import os
import argparse
from datetime import datetime, date

api_key = "18bb80696ecc77ff0ebaf2056f075aad"
prefix_url = "https://fmpcloud.io/api/v3"

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_urls(symbol):
    income_url = prefix_url + '/income-statement/' + symbol + '?limit=120'
    income_url += '&apikey=' + api_key
    historic_url = prefix_url + '/historical-price-full/' + symbol + '?serietype=line'
    historic_url += '&apikey=' + api_key
    return [income_url, historic_url]


def get_results(symbol, urls):
    get_url_data(symbol, 'income', urls[0])
    get_url_data(symbol, 'historical', urls[1])


def get_url_data(symbol, name, url):
    filename = os.path.join('raw', symbol + '_' + name + '.json')
    print(filename)
    if not os.path.exists('raw'):
        os.makedirs('raw')
    with open(filename, 'w') as file:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('utf-8')
            file.write(data)
        else:
            print("failed to get " + name)


def create_score(symbol):
    try:
        if not os.path.exists('scores'):
            os.makedirs('scores')
        filename = os.path.join('seperated', symbol, 'historical1.json')
        with open(filename) as current:
            filename = os.path.join('seperated', symbol, 'historical30.json')
            with open(filename) as old:
                data_current = json.load(current)
                data_old = json.load(old)
                score = data_current['close'] - data_old['close']
                filename = os.path.join('scores', symbol+'_score.json')
                with open(filename, 'w') as score_file:
                    data = {}
                    data['score'] = score
                    data['old'] = data_old['close']
                    data['current'] = data_current['close']
                    data['percentage'] = (((data_current['close'] - data['old']) /  data_current['close']) * 100)
                    json.dump(data, score_file)
    except:
        pass


def analyze_results(symbol):
    if not os.path.exists('seperated'):
        os.mkdir('seperated')
    symbol_path = os.path.join('seperated', symbol)
    if not os.path.exists(symbol_path):
        os.mkdir(symbol_path)
    create_separated_files(symbol, 'income')
    create_separated_files(symbol, 'historical')
    create_score(symbol)
    # for filesname in os.listdir('raw'):
    #     print(filesname)
    # with open('dict.json', 'w') as w:
    #     with open('testfile.json', 'r') as r:
    #         data_list = json.load(r)
    #         for d in data_list:
    #             w.writelines('\n' + str(d['grossProfit']))


def create_separated_files(symbol, querytype):
    filename = os.path.join('raw', symbol + '_' + querytype + '.json')
    if not os.path.exists(filename):
        return
    with open(filename) as f:
        data_list = json.load(f)
        i = 1
        if querytype in data_list:
            data_list = data_list[querytype]
        for data in data_list:
            days_from_now = datetime.strptime(data['date'], '%Y-%m-%d')
            days_diff = datetime.today() - days_from_now
            data['date'] = days_diff.days
            data.pop('label', None)



            today = date.today()
            filename_to_write = os.path.join('seperated', symbol, querytype + str(i) + '.json')
            with open(filename_to_write, 'w') as file_to_write:
                json.dump(data, file_to_write)
            i += 1


def get_companies(args):
    with open(args.companies_file, 'r') as companies:
        for symbol in companies:
            if len(symbol) > 0:
                symbol = symbol[:-1]
                if args.fetchmode:
                    print(symbol)
                    urls = get_urls(symbol)
                    get_results(symbol, urls)
                else:
                    analyze_results(symbol)


def main():
    args = parse_arguments()
    get_companies(args)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--companies_file', type=str,
                        help="the companies you want to download info for", required=True)
    parser.add_argument("--fetchmode", type=str2bool, nargs='?', const=True, default=False,
                        help="fetch data / analyze data")
    # parser.add_argument("--history_window_for_engine_input",
    #                    type=int,  const=True, default=365,
    #                     help="amount of history in days that the engine gets")
    # parser.add_argument("--history_window_for_engine_testing", type=int, const=True,
    #                     default=90, help="amount of history in days that the engine gets")

    return parser.parse_args()


if __name__ == "__main__":
    main()
