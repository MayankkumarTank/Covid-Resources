import tweepy
import logging
import time
import psycopg2
import urllib.parse as urlparse
import os
import requests

url = urlparse.urlparse("postgres://myetoimjbtajmy:59d16a587c226904afd0903826a21c9d5c51e1a3688c66f21adcd420bca2060a@ec2-3-233-43-103.compute-1.amazonaws.com:5432/d1tg803nk52arh")
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )
cur = con.cursor()
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
                table = "Select * from Resources;"
                cur.execute(table)
                # Retrieve query results
                records = cur.fetchall()
                arr = []
                for i in range(0,len(records)):
                    api.update_status(
                        status='@'+ tweet.user.screen_name+" "+"UseFul Link: "+records[i][0],
                        in_reply_to_status_id=tweet.id
                        # in_reply_to_user_id_str=str(tweet.id)
                    )  
            elif tweet.text.lower().split(' ')[1]=='contribute':
                #If verified then insert if not
                table = "Select * from Resources;"
                cur.execute(table)
                # Retrieve query results
                records = cur.fetchall()
                arr = []
                for i in range(0,len(records)):
                    arr.append(records[i][0])
                cur.execute("Select * from Contributions;")
                records = cur.fetchall()
                for i in range(0,len(records)):
                    arr.append(records[i][0])
                
                len1 = len(tweet.text.split(' ')[0]) + 12
                
                c_link = tweet.text[len1:]
                print(c_link)
                if c_link not in arr:
                    cur.execute("Insert into Contributions values ('"+c_link+"');")
                    con.commit()
                    api.update_status(
                        status='@'+ tweet.user.screen_name+" "+"Thanks for your contribution. Your link will be added to our database after verification by our team.",
                        in_reply_to_status_id=tweet.id
                        # in_reply_to_user_id_str=str(tweet.id)
                    )
                else:
                    api.update_status(
                        status='@'+ tweet.user.screen_name+" "+"We already have this source but thanks for contributing.",
                        in_reply_to_status_id=tweet.id
                        # in_reply_to_user_id_str=str(tweet.id)
                    )
            else:
                api.update_status(
                    status='@'+ tweet.user.screen_name+" "+"🤖: Please provide keywords like 'help' (which gives a link to the resources) and 'contribute' (to contribute the COVID-related resources/leads). \nView my Bio for more info @CovidResource14.",
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
