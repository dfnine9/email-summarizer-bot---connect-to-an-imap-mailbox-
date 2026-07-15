"""
This script uses the Tweepy library to fetch tweets based on a specific hashtag or keyword.
It handles errors gracefully and prints the results to stdout.
"""

import tweepy

# Set up your credentials
API_KEY = 'your_api_key'
API_SECRET_KEY = 'your_api_secret_key'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

def fetch_tweets_by_hashtag(hashtag):
    """
    Fetches tweets containing the specified hashtag.
    
    Args:
        hashtag (str): The hashtag to search for.
        
    Returns:
        list: A list of tweets containing the hashtag.
    """
    # Authenticate to Twitter
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    tweets = []
    
    try:
        # Fetch tweets
        for tweet in tweepy.Cursor(api.search_tweets, q=hashtag, lang='en').items(10):
            tweets.append(tweet.text)
            
    except tweepy.TweepError as e:
        print(f"Error fetching tweets: {e}")
    
    return tweets

if __name__ == "__main__":
    hashtag_to_search = input("Enter a hashtag to search for: ")
    results = fetch_tweets_by_hashtag(hashtag_to_search)
    
    if results:
        print("Fetched Tweets:")
        for tweet in results:
            print(tweet)
    else:
        print("No tweets found.")