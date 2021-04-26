import tweepy
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
sleepTime=32
# Authenticate to Twitter
auth = tweepy.OAuthHandler("CyyqO4JspGaoBGCb4roFSWHa0", "TFA9K8uPY0D5mZ9SmDNC72X8dmMxuspo0dH9D7ljbl9LNJjK49")
auth.set_access_token("1386623704612753411-40wyu5cND5uHFNYFpP1aZcXxFeWWGm", "urnEKiiEXpt0RjgScaliSeCcZgmk8EVSkuoLPfjzZKLpJ")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# prints error message
def getExceptionMessage(msg):
    words = msg.split(' ')

    errorMsg = ""
    for index, word in enumerate(words):
        if index not in [0,1,2]:
            errorMsg = errorMsg + ' ' + word
    errorMsg = errorMsg.rstrip("\'}]")
    errorMsg = errorMsg.lstrip(" \'")

    return errorMsg

# Tweeting out the information 
def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    try:
        sleepTime = 1
        new_since_id = since_id
        for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
            new_since_id = max(tweet.id, new_since_id)
            if tweet.in_reply_to_status_id is not None:
                continue
            # if any(keyword in tweet.text.lower() for keyword in keywords):
            
            logger.info(f"Answering to {tweet.user.name}")
            if tweet.text.lower().split(' ')[1]=='help':
                api.update_status(
                    status='@'+ tweet.user.screen_name+" "+"Help giving",
                    in_reply_to_status_id=tweet.id
                    # in_reply_to_user_id_str=str(tweet.id)
                )
            elif tweet.text.lower().split(' ')[1]=='contribute':
                api.update_status(
                    status='@'+ tweet.user.screen_name+" "+"Taking your contribution",
                    in_reply_to_status_id=tweet.id
                    # in_reply_to_user_id_str=str(tweet.id)
                )
            else:
                api.update_status(
                    status='@'+ tweet.user.screen_name+" "+"Loading",
                    in_reply_to_status_id=tweet.id
                    # in_reply_to_user_id_str=str(tweet.id)
                )
        return new_since_id
    
    except tweepy.TweepError as e:
        print(e.api_code)
        print(getExceptionMessage(e.reason))
        if sleepTime>=300:
            sleepTime/=2
        time.sleep(sleepTime)
        sleepTime *= 2

def main():
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(5)

if __name__ == "__main__":
    main()