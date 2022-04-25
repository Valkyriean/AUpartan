import  tweepy
import secret

#api key and api key secret here,need elevated account to run
auth = tweepy.OAuthHandler(secret.key, secret.keysecret)
    
api = tweepy.API(auth, wait_on_rate_limit=True)

#geocode="latitude, longitude,xxkm" (also acceptble for "ml" if you are an American),more detail see documentation
tweets = api.search_tweets("covid", geocode="-37.79825,144.96367,1.5km",lang="en") 

#print(tweets)
