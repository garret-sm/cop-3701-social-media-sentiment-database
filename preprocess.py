import pandas as pd
import random

def RandomDate():
    return f"{random.randrange(1,12)} / {random.randrange(1,28)} / {random.randrange(1984, 2026)}"

def RandomFollowers():
    return random.randrange(0, 126000)

def RandomBool():
    return random.randrange(0,2)

def RandomModel():
    return random.randrange(0,8)

def RandomConfidence():
    return random.randrange(0, 11)
line_count = 0
bio = "hi im a bio"
pfp = "hi i'm a profile picture link!!!"
language = "English"

data = pd.read_csv("data.csv")

user_data = []
user_profile = []
tweets = []
tweet_tag = []
hashtag = []
sentiment_score = []
sentiment_category = []
description = "Placeholder description here."
sentiment_label = "Label"

for (target, ids, date, flag, username, text) in data.itertuples(index = False):
    #user profile
    user_profile.append((len(user_data), bio, pfp, "https://" + username + ".twitter.com/", RandomBool()))
    #tweets
    tweets.append((len(tweets), text, date, language, RandomFollowers(), flag, len(user_data)))
    #user data
    user_data.append((len(user_data), username, username + "@twitter.com", RandomDate(), RandomFollowers()))
    #hashtag
    hashindex=0
    while True:
        hashindex=text.find("#", hashindex) + 1
        if hashindex == 0:
            break
        hashendindex=text.find(" ", hashindex)
        hashtext = text[hashindex:hashendindex]
        if not any(hashtext == hashtext2 for(hashid,hashtext2,first_seen_date) in hashtag):
            hashtag.append((len(hashtag), hashtext, RandomDate()))
        tweet_tag.append((len(tweets)-1, [hashid for(hashid,hashtext2,first_seen_date) in hashtag if hashtext==hashtext2][0], 0))
    sentiment_score.append((len(sentiment_score), len(tweets)-1, target, RandomModel(), RandomDate(), RandomConfidence(), len(sentiment_category)))
    sentiment_category.append((len(sentiment_category), sentiment_label, description))
    
  
    
# dataframes
userdf = pd.DataFrame(user_data, columns=["user_id", "username", "email", "acc_creation_date", "follower_count"])
userpf = pd.DataFrame(user_profile, columns=["user_id", "bio", "profile picture", "URL", "Verified_Status"])
tweetsf = pd.DataFrame(tweets, columns = ["tweet_id", "content", "posted_at", "language", "retweet_count", "flag", "user_id"])
hashtextf = pd.DataFrame(hashtag, columns=["tag_id", "tag_text", "first_seen_date"])
tweet_tagf = pd.DataFrame(tweet_tag, columns=["tweet_id", "tag_id", "position_in_tweet"])
sentimentf_score = pd.DataFrame(sentiment_score, columns=["score_id", "tweet_id", "score_value", "model_used", "analyzed_at", "confidence", "category_id"])
sentimentf_category = pd.DataFrame(sentiment_category, columns = ["category_id", "label", "description_"])
#tocsv
userdf.to_csv("data/user.csv", index=False)
userpf.to_csv("data/userprofile.csv", index=False)
tweetsf.to_csv("data/tweets.csv", index=False)
hashtextf.to_csv("data/hashtag.csv", index=False)
tweet_tagf.to_csv("data/tweet_tag.csv", index=False)
sentimentf_score.to_csv("data/sentiment_score.csv", index=False)
sentimentf_category.to_csv("data/sentiment_category.csv", index=False)
