import pandas as pd
import time
import sys 
import os
import pymysql
import pyodbc
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))        
import config
from TwitterDatabase import TwitterDatabase
from TwitterXAPI import TwitterXAPI

class TwitterTraffic:
    def __init__(self, bearer_token, data_file):
        #connect to config
        
        #using config direct the database connection
        if config.DB_DRIVER == 'pyodbc':
            db_connection_string = config.DB_CONNECTION_STRING_TWITTERX_MyODBC_ETL
            connection = pyodbc.connect(db_connection_string)

        elif config.DB_DRIVER == 'pymysql':
            db_connection = config.DB_CONNECTION_STRING_TwitterX_MySQL_ETL
            connection = pymysql.connect(
                host=db_connection['host'],
                user=db_connection['user'],
                password=db_connection['password'],
                database=db_connection['database']
        )
        else:
            raise ValueError("Unsupported database driver")
        
        self.api = TwitterXAPI(bearer_token)
        self.db = TwitterDatabase(connection, config.DB_DRIVER)
        self.data_file = data_file  

    def get_city_traffic_issues(self, cities, use_file=False, max_results=10):
        if config.Use_API == False:
            #load save data from file
            print(f"Loading data from file: {self.data_file}")
            df = pd.read_csv(self.data_file)
        else:
            #call twitter api
            all_tweets = []
            #get the last id so we can set it in the call
            last_tweet_id = self.db.get_last_tweet_id()
            tweet_count = 0
            retries = 0
            #chunks of 10
            while tweet_count < max_results:
                #setup keywords for a query into twitter x
                #query = 'kitchener (collision OR "car accident" OR "construction delays" OR "icy road" OR "drive home") lang:en -is:retweet -is:reply'                
                query = ' OR '.join([f'({city} (driver OR collision OR "car accident" OR "construction delays" OR "icy road" OR "drive home"))' for city in cities])
                query += ' lang:en -is:retweet -is:reply'
                #execute the search
                tweets, meta = self.api.search_tweets(query, max_results, last_tweet_id)
                #respond to the reseult count
                if meta and meta.get('result_count', 0) > 0:
                    #add to list
                    all_tweets.extend(tweets)

                    tweet_count += len(tweets)                    
                    
                    print(f"Fetched {tweet_count} tweets...")
                    #save tweets to file, data is retrieved without city of origin                    
                    df = self.db.save_tweets_to_file(all_tweets, self.data_file)                    
                    
                    print(f"Successfully fetched and saved {tweet_count} tweets for {cities} to file.")                    
                    break
                else:
                    print("No tweets found. Retrying...")
                    retries += 1
                    if retries >= 5:
                        print("Max retries reached. Exiting.")
                        break
                    time.sleep(60)

        return df.to_dict('records')

    #store tweets to database
    def store_tweets(self, tweets):        
         self.db.store_tweets(tweets)
           

if __name__ == "__main__":


    
    #settings
    bearer_token = "AAAAAAAAAAAAAAAAAAAAACySxAEAAAAArQpbpzVcN%2B%2F6gGkMPv%2Fpv4b2LM8%3DUYSTvRUShoGtKGdKJBR3VwZAAZc3w0lmbQ0ZfBcrH2jSdCTsV3"
    data_file = r"Data\TwitterXAPI\data\traffic_tweets.csv"
    cities = ["Kitchener", "Waterloo", "Cambrdige", "London"]

    twitter_traffic = TwitterTraffic(bearer_token, data_file)
    
    #call api
    tweets = twitter_traffic.get_city_traffic_issues(cities, use_file=False, max_results=10)
    #save to db
    twitter_traffic.store_tweets(tweets)
    
