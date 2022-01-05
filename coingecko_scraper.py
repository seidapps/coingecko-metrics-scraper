import csv
import requests

from dataclasses import asdict
from helpers import CoinMetrics, CoinExchange

class CoinGeckoScraper:

    def parse_coingecko_exchange_metrics(self, result):

        exchange_data_list = [] 

        volume_24h = result['market_data']['total_volume']['usd']

        tickers = result['tickers']
        for ticker in tickers:
            exchange_data = CoinExchange(
                coin_id            = result['id'],
                coin_name          = result['name'],
                symbol             = result['symbol'],
                base               = ticker['base'],
                target             = ticker['target'],
                market_name        = ticker['market']['name'],
                market_identifier  = ticker['market']['identifier'],
                market_has_trading_incentive = ticker['market']['has_trading_incentive'],
                price              = ticker['last'],
                volume             = ticker['converted_volume']['usd'],
                pp_total_volume    = float(ticker['converted_volume']['usd']) / float(volume_24h),
                is_stale           = ticker['is_stale'],
            )
            exchange_data_list.append(exchange_data)

        return (exchange_data_list)        

    def parse_coingecko_metrics(self, result):

        market_data = result['market_data']
        community_data = result['community_data']
        developer_data = result['developer_data']        

        try: fully_diluted_valuation = market_data['fully_diluted_valuation']['usd']
        except: fully_diluted_valuation = 0

        return CoinMetrics(

            # Coin information
            coin_id                    = result['id'],
            coin_name                  = result['name'],
            symbol                     = result['symbol'],

            # Price and volume data
            price                      = market_data['current_price']['usd'],
            volume_24h                 = market_data['total_volume']['usd'],
            market_cap                 = market_data['market_cap']['usd'],
            fully_diluted_valuation    = fully_diluted_valuation,
            circulating_supply         = market_data['circulating_supply'],
            total_supply               = market_data['total_supply'],
            max_supply                 = market_data['max_supply'],

            # Community data
            twitter_followers           = community_data['twitter_followers'],
            facebook_likes              = community_data['facebook_likes'],
            reddit_average_posts_48h    = community_data['reddit_average_posts_48h'],
            reddit_average_comments_48h = community_data['reddit_average_comments_48h'],
            reddit_subscribers          = community_data['reddit_subscribers'],
            reddit_accounts_active_48h  = community_data['reddit_accounts_active_48h'],
            telegram_channel_user_count = community_data['telegram_channel_user_count'],

            # Developer data
            forks                       = developer_data['forks'],
            stars                       = developer_data['stars'],
            subscribers                 = developer_data['subscribers'],
            total_issues                = developer_data['total_issues'],
            closed_issues               = developer_data['closed_issues'],
            pull_requests_merged        = developer_data['pull_requests_merged'],
            pull_request_contributors   = developer_data['pull_request_contributors'],
            code_additions_deletions_4_weeks_additions = developer_data['code_additions_deletions_4_weeks']['additions'],
            code_additions_deletions_4_weeks_deletions = developer_data['code_additions_deletions_4_weeks']['deletions'],
            commit_count_4_weeks        = developer_data['commit_count_4_weeks']
        )


    def fetch_coingecko_data(self, coin_id):

        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        r = requests.get(url)
        return r.json()

    def coingecko_scraper(self):

        coin_metrics_output_filename = 'data/coin_metrics.csv'
        coin_metrics_filenames = list(CoinMetrics.__annotations__.keys())
        coin_metrics_writer = csv.DictWriter(open(coin_metrics_output_filename, 'w'), fieldnames=coin_metrics_filenames)       
        coin_metrics_writer.writeheader()

        exchange_metrics_output_filename = 'data/exchange_metrics.csv'
        exchange_metrics_filenames = list(CoinExchange.__annotations__.keys())
        exchange_metrics_writer = csv.DictWriter(open(exchange_metrics_output_filename, 'w'), fieldnames=exchange_metrics_filenames)
        exchange_metrics_writer.writeheader()

        with open('coin_ids.csv', 'r') as f:

            csvreader = csv.reader(f)
            for row in csvreader:
                
                coin_id = row[0]

                result = self.fetch_coingecko_data(coin_id)

                coin_metrics = self.parse_coingecko_metrics(result)
                coin_metrics_writer.writerow(asdict(coin_metrics))

                exchange_metrics = self.parse_coingecko_exchange_metrics(result)
                for exchange in exchange_metrics:
                    exchange_metrics_writer.writerow(asdict(exchange))

if __name__ == '__main__':

    scraper = CoinGeckoScraper()
    scraper.coingecko_scraper()