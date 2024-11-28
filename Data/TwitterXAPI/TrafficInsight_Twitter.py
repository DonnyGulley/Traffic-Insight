from datetime import datetime
import tweepy
import pandas as pd
import pyodbc
import time
import os

class TwitterTraffic:
    def __init__(self, bearer_token=None, db_connection_string=None, data_file=None):
        if bearer_token is not None and db_connection_string is not None and data_file is not None:
            # Initialize with custom values (i.e., when all arguments are provided)
            self.bearer_token = bearer_token
            self.api = self.authenticate()
            self.db_connection_string = db_connection_string
            self.conn = self.create_connection()
            self.data_file = data_file
        else:
            # Default initialization behavior
            print("Initializing with default values.")
            self.bearer_token = "default_bearer_token"
            self.api = None  # API initialization logic goes here
            self.db_connection_string = "default_connection_string"
            self.conn = None  # Connection initialization logic goes here
            self.data_file = "default_data_file.csv"

    def authenticate(self):
        try:
            client = tweepy.Client(bearer_token=self.bearer_token)
            print("Authentication successful")
            return client
        except Exception as e:
            print(f"Error during authentication: {e}")
            return None

    def create_connection(self):
        try:
            conn = pyodbc.connect(self.db_connection_string)
            print("Connection to SQL Server successful")
            return conn
        except pyodbc.Error as e:
            print(f"Error connecting to SQL Server: {e}")
            return None
   
  

    def clean_tweet_text(self, tweet_text):
        """
        Clean tweet text by removing unwanted characters, links, and mentions.
        """

        # Remove URLs (http://, https://, www links)
        words = tweet_text.split()  # Split tweet into words
        cleaned_words = []
        for word in words:
            if word.startswith("http://") or word.startswith("https://") or word.startswith("www."):
                continue  # Skip this word as it's a URL
            cleaned_words.append(word)

        tweet_text = " ".join(cleaned_words)  # Rebuild tweet text from cleaned words

        # Remove Twitter mentions (@username)
        words = tweet_text.split()
        cleaned_words = []
        for word in words:
            if word.startswith('@'):
                continue  # Skip mentions starting with "@"
            cleaned_words.append(word)

        tweet_text = " ".join(cleaned_words)  # Rebuild tweet text from cleaned words

        # Remove hashtags (#hashtag)
        words = tweet_text.split()
        cleaned_words = []
        for word in words:
            if word.startswith('#'):
                continue  # Skip hashtags starting with "#"
            cleaned_words.append(word)

        tweet_text = " ".join(cleaned_words)  # Rebuild tweet text from cleaned words

        # Remove non-alphanumeric characters except spaces
        cleaned_words = []
        for word in tweet_text.split():
            cleaned_word = ''.join(char for char in word if char.isalnum() or char == ' ')  # Keep alphanumeric and space only
            cleaned_words.append(cleaned_word)

        tweet_text = " ".join(cleaned_words)  # Rebuild tweet text from cleaned words

        # Remove extra spaces (to make sure there's no leading/trailing space)
        tweet_text = ' '.join(tweet_text.split())

        # Convert text to lowercase (optional)
        tweet_text = tweet_text.lower()

        return tweet_text

    def get_last_tweet_id(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT MAX(TweetID) FROM Tweets")
            last_tweet_id = cursor.fetchone()[0]
            cursor.close()
            return last_tweet_id
        except pyodbc.Error as e:
            print(f"Error fetching last tweet ID: {e}")
            return None   
        
    def search_tweets(self, query, max_results=10, last_tweet_id=None):  
        backoff_time = 60  # Initial backoff time in seconds
        max_backoff_time = 3600  # Max backoff time (1 hour) to prevent indefinite sleeping
        retries = 0
        while True:
            try:
                # Call to Twitter API search
                response = self.api.search_recent_tweets(query=query, max_results=max_results, since_id=last_tweet_id, tweet_fields=['created_at', 'text'])

                print("Tweets fetched successfully")
                
                # Retrieve last tweet ID
                last_tweet_id = response.data[-1].id if response.data else None

                return response.data, response.meta  # Return the tweet data and metadata

            except tweepy.errors.TooManyRequests as e:
                print(f"Rate limit exceeded: {e}")
                
                # Get reset time from the exception response
                reset_time = e.response.headers.get('x-rate-limit-reset')
                reset_time = int(reset_time) if reset_time else time.time() + 60  # Default to 60 seconds if no reset time available

                # Setup a timer 
                sleep_time = max(reset_time - time.time(), backoff_time)
                print(f"Sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)

                retries += 1
                if retries >= 5:  # Limit retries to avoid excessive backoff
                    print("Max retries reached. Exiting.")
                    return [], {}  # Exit after 5 retries

                backoff_time = min(backoff_time * 2, max_backoff_time)  # Exponential backoff with a cap

            except tweepy.errors.Forbidden as e:
                print(f"Usage cap exceeded: {e}")
                print("You have reached your monthly usage cap. Please upgrade your subscription or wait until the next billing cycle.")
                return [], {}  # Return empty response to indicate failure

            except Exception as e:
                print(f"Error fetching tweets: {e}")
                return [], {}

    def get_city_traffic_issues(self, city, use_file=False, max_results=10):
        # Use the file switch to load a file or call the API
        if use_file:
            print(f"Loading data from file: {self.data_file}")
            
            # Load data file to data frame
            df = pd.read_csv(self.data_file)           
        else:
            all_tweets = []
            last_tweet_id = self.get_last_tweet_id()
            tweet_count = 0  # Counter for the number of tweets fetched
            retries = 0

            while tweet_count < max_results:
                query = 'kitchener (collision OR accident OR "delays" OR "construction") lang:en -is:retweet -is:reply'

                # Call API to fetch tweets
                tweets, meta = self.search_tweets(query, max_results,last_tweet_id)

                # Check if tweets were fetched successfully
                if meta and meta.get('result_count', 0) > 0:
                    # Add fetched tweets to the list
                    all_tweets.extend(tweets)
                    tweet_count += len(tweets)  # Update the tweet counter
                    print(f"Fetched {tweet_count} tweets...")

                    # Save to file                     
                    df = self.save_tweets_to_file(all_tweets, city)
                    print(f"Successfully fetched and saved {tweet_count} tweets for {city} to file.")
                    break
                else:
                    print("No tweets found. Retrying...")
                    retries += 1
                    if retries >= 5:  # Retry limit
                        print("Max retries reached. Exiting.")
                        break
                    time.sleep(60)  # Wait before retrying

        return df.to_dict('records')

    def save_tweets_to_file(self, tweets, city):
        # Build a data dictionary
        data = {
            "TweetID": [tweet.id for tweet in tweets],
            "TweetText": [tweet.text for tweet in tweets],
            "CreatedAt": [tweet.created_at for tweet in tweets],
            "City": [city] * len(tweets)
        }

        # Load dictionary of tweet information to DataFrame
        df = pd.DataFrame(data)

        # Save DataFrame to file
        df.to_csv(self.data_file, index=False)
        print(f"Data saved to file: {self.data_file}")

        return df

    def store_tweets(self, tweets, city):
        """
        Store tweets in the database after cleaning and checking for duplicates.
        """
        cursor = None
        try:
            # Prepare data for DataFrame
            data = {
                "TweetID": [tweet['TweetID'] for tweet in tweets],
                "TweetText": [tweet['TweetText'] for tweet in tweets],
                "CreatedAt": [tweet['CreatedAt'] for tweet in tweets],
                "City": [city] * len(tweets)
            }
            df = pd.DataFrame(data)

            # Clean TweetText column using the clean_tweet_text function
            for idx, row in df.iterrows():
                tweet_text = row['TweetText']
                #clean 
                cleaned_text = self.clean_tweet_text(tweet_text)
                df.at[idx, 'TweetText'] = cleaned_text

            # Convert CreatedAt column to datetime format
            df['CreatedAt'] = pd.to_datetime(df['CreatedAt'], errors='coerce')

            # Connect to the database
            cursor = self.conn.cursor()

            # Insert tweets into the database
            for _, row in df.iterrows():
                cursor.execute("SELECT COUNT(*) FROM Tweets WHERE TweetID = ?", row.TweetID)
                if cursor.fetchone()[0] == 0:  # No record found
                    cursor.execute("""
                        INSERT INTO Tweets (TweetID, TweetText, CreatedAt, City)
                        VALUES (?, ?, ?, ?)
                    """, row.TweetID, row.TweetText, row.CreatedAt, row.City)
                    print(f"New tweet inserted: {row.TweetID}")
                else:
                    print(f"Duplicate tweet found, skipping: {row.TweetID}")

            self.conn.commit()

        except pyodbc.Error as e:
            print(f"Error storing tweets: {e}")
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()

# Usage
if __name__ == "__main__":
    bearer_token = "AAAAAAAAAAAAAAAAAAAAACySxAEAAAAArQpbpzVcN%2B%2F6gGkMPv%2Fpv4b2LM8%3DUYSTvRUShoGtKGdKJBR3VwZAAZc3w0lmbQ0ZfBcrH2jSdCTsV3"
    db_connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight_Tweets;Trusted_Connection=yes;'
    
    # Initialize data_file as an empty string initially
    data_file = "traffic_tweets.csv"  # Define the output file path

    # Initialize TwitterTraffic instance
    twitter_traffic = TwitterTraffic(bearer_token, db_connection_string, data_file)

    # Specify the city (can be a list of cities)
    city = "Kitchener"

    # Fetch tweets (either from file or API)
    tweets = twitter_traffic.get_city_traffic_issues(city, use_file=False, max_results=10)

    # Store the fetched tweets in the database
    twitter_traffic.store_tweets(tweets, city)
