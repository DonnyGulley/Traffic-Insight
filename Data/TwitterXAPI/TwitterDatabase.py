import pyodbc
import pandas as pd

class TwitterDatabase:
    def __init__(self, db_connection_string):
        self.db_connection_string = db_connection_string
        self.conn = self.create_connection()

    def create_connection(self):
        try:
            conn = pyodbc.connect(self.db_connection_string)
            print("Connection to SQL Server successful")
            return conn
        except pyodbc.Error as e:
            print(f"Error connecting to SQL Server: {e}")
            return None
    #used in the filter to keep moving forward
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

    def store_tweets(self, tweets):
        cursor = None
        try:
            data = {
                "TweetID": [tweet['TweetID'] for tweet in tweets],
                "TweetText": [tweet['TweetText'] for tweet in tweets],
                "CreatedAt": [tweet['CreatedAt'] for tweet in tweets]
            }
            df = pd.DataFrame(data)

            # Insert tweets into the database
            cursor = self.conn.cursor()
            for _, row in df.iterrows():
                cursor.execute("SELECT COUNT(*) FROM Tweets WHERE TweetID = ?", row.TweetID)
                if cursor.fetchone()[0] == 0:  # No record found
                    cursor.execute("""
                        INSERT INTO Tweets (TweetID, TweetText, CreatedAt)
                        VALUES (?, ?, ?)
                    """, row.TweetID, row.TweetText, row.CreatedAt)
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
