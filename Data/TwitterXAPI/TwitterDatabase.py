import pandas as pd

class TwitterDatabase:
    def __init__(self, db_connection, db_driver):
        self.db_connection = db_connection     
        self.db_driver = db_driver
    
    #used in the filter to keep moving forward
    def get_last_tweet_id(self):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT MAX(TweetID) FROM Tweets")
                last_tweet_id = cursor.fetchone()[0]
                
            return last_tweet_id
        except Exception as e:
            print(f"Error fetching last tweet ID: {e}")
            return None
    
    #Helper function for switching between mssql and mysql        
    def format_query( self, query):
        if self.db_driver == 'pyodbc':
            return query.replace('%s', '?')
        elif self.db_driver == 'pymysql':
            return query
        else:
            raise ValueError("Unsupported database driver")

    def store_tweets(self, tweets):
        cursor = None
        try:
            data = {
                "TweetID": [tweet['TweetID'] for tweet in tweets],
                "TweetText": [tweet['TweetText'] for tweet in tweets],
                "CreatedAt": [tweet['CreatedAt'] for tweet in tweets]
            }
            df = pd.DataFrame(data)
            df['CreatedAt'] = pd.to_datetime(df['CreatedAt'])
            
            # Insert tweets into the database
            cursor = self.db_connection.cursor()
            for _, row in df.iterrows():
                check_query = self.format_query("SELECT COUNT(*) FROM Tweets WHERE TweetID = %s")
                cursor.execute(check_query, (row.TweetID,))
                if cursor.fetchone()[0] == 0:  # No record found
                    insert_query = self.format_query("""
                        INSERT INTO Tweets (TweetID, TweetText, CreatedAt)
                        VALUES (%s, %s, %s)
                    """)
                    cursor.execute(insert_query, (row.TweetID, row.TweetText, row.CreatedAt))
                    print(f"New tweet inserted: {row.TweetID}")
                else:
                    print(f"Duplicate tweet found, skipping: {row.TweetID}")

            self.db_connection.commit()

        except Exception as e:
            print(f"Error storing tweets: {e}")
            self.db_connection.rollback()
        finally:
            if cursor:
                cursor.close()

    def save_tweets_to_file(self, tweets, data_file):
        data = {
            "TweetID": [tweet.id for tweet in tweets],
            "TweetText": [tweet.text for tweet in tweets],
            "CreatedAt": [tweet.created_at for tweet in tweets]
        }

        df = pd.DataFrame(data)
        df.to_csv(data_file, index=False)
        print(f"Data saved to file: {data_file}")

        return df
