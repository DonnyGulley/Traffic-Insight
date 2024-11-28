from TwitterDatabase import TwitterDatabase
from TwitterXAPI import TwitterXAPI

import pandas as pd
import time

class TwitterTraffic:
    def __init__(self, bearer_token, db_connection_string, data_file):
        self.api = TwitterXAPI(bearer_token)
        self.db = TwitterDatabase.Database(db_connection_string)
        self.data_file = data_file

    def clean_tweet_text(self, tweet_text):

        pass

    def get_city_traffic_issues(self, city, use_file=False, max_results=10):
        if use_file:
            print(f"Loading data from file: {self.data_file}")
            df = pd.read_csv(self.data_file)
        else:
            all_tweets = []
            last_tweet_id = self.db.get_last_tweet_id()
            tweet_count = 0
            retries = 0

            while tweet_count < max_results:
                query = 'kitchener ("vehicle collision" OR "car accident" OR "construction delays" OR "icy road") lang:en -is:retweet -is:reply'
                tweets, meta = self.api.search_tweets(query, max_results, last_tweet_id)

                if meta and meta.get('result_count', 0) > 0:
                    all_tweets.extend(tweets)
                    tweet_count += len(tweets)
                    print(f"Fetched {tweet_count} tweets...")
                    df = self.db.save_tweets_to_file(all_tweets, city, self.data_file)
                    print(f"Successfully fetched and saved {tweet_count} tweets for {city} to file.")
                    break
                else:
                    print("No tweets found. Retrying...")
                    retries += 1
                    if retries >= 5:
                        print("Max retries reached. Exiting.")
                        break
                    time.sleep(60)

        return df.to_dict('records')

    def store_tweets(self, tweets, city):
        self.db.store_tweets(tweets, city)


if __name__ == "__main__":
    bearer_token = "AAAAAAAAAAAAAAAAAAAAACySxAEAAAAArQpbpzVcN%2B%2F6gGkMPv%2Fpv4b2LM8%3DUYSTvRUShoGtKGdKJBR3VwZAAZc3w0lmbQ0ZfBcrH2jSdCTsV3"
    db_connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight_Tweets;Trusted_Connection=yes;'
    data_file = "\data\\traffic_tweets.csv"

    twitter_traffic = TwitterTraffic(bearer_token, db_connection_string, data_file)
    city = "Kitchener"

    tweets = twitter_traffic.get_city_traffic_issues(city, use_file=False, max_results=10)
    twitter_traffic.store_tweets(tweets, city)
