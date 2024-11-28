import tweepy
import time

class TwitterXAPI:
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.api = self.authenticate()

    def authenticate(self):
        try:
            client = tweepy.Client(bearer_token=self.bearer_token)
            print("Authentication successful")
            return client
        except Exception as e:
            print(f"Error during authentication: {e}")
            return None

    def search_tweets(self, query, max_results=10, last_tweet_id=None):  
        backoff_time = 60  # Initial backoff time in seconds
        max_backoff_time = 3600  # Max backoff time (1 hour) to prevent indefinite sleeping
        retries = 0
        while True:
            try:
                response = self.api.search_recent_tweets(query=query, max_results=max_results, since_id=last_tweet_id, tweet_fields=['created_at', 'text'])
                print("Tweets fetched successfully")
                
                # Retrieve last tweet ID
                last_tweet_id = response.data[-1].id if response.data else None
                return response.data, response.meta  # Return the tweet data and metadata

            except tweepy.errors.TooManyRequests as e:
                print(f"Rate limit exceeded: {e}")
                reset_time = e.response.headers.get('x-rate-limit-reset')
                reset_time = int(reset_time) if reset_time else time.time() + 60
                sleep_time = max(reset_time - time.time(), backoff_time)
                print(f"Sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)

                retries += 1
                if retries >= 5:
                    print("Max retries reached. Exiting.")
                    return [], {}
                backoff_time = min(backoff_time * 2, max_backoff_time)

            except tweepy.errors.Forbidden as e:
                print(f"Usage cap exceeded: {e}")
                print("You have reached your monthly usage cap. Please upgrade your subscription or wait until the next billing cycle.")
                return [], {}

            except Exception as e:
                print(f"Error fetching tweets: {e}")
                return [], {}
