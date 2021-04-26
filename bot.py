import tweepy
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

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

# Tweeting out the information 
def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")
            print("tweet.id", (tweet.id))
            print("tweet.user.id", (tweet.user.id))
            print(api.get_status)
            api.update_status(
                status='@'+ tweet.user.screen_name+" Please reach us via DM DM DM DM",
                in_reply_to_user_id=tweet.user.id,
                in_reply_to_status_id=tweet.id
                # in_reply_to_user_id_str=str(tweet.id)
            )
    return new_since_id

def main():
    since_id = 1
    while True:
        since_id = check_mentions(api, ["help", "support"], since_id)
        logger.info("Waiting...")
        time.sleep(5)

if __name__ == "__main__":
    main()
