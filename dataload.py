import oracledb
import pandas as pd


def fetch_data(table_name: str):
    # Use pandas to read from the DB connection
    return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)


LIB_DIR = r"C:\oracle\instantclient_11_2"  # Your Instant Client Path
DB_USER = "system"
DB_PASS = "PitchBlack55732"
DB_DSN  = "localhost:1521/xe"

# Initialize Thick Mode (Required for FreeSQL/Cloud)
if LIB_DIR:
    oracledb.init_oracle_client(lib_dir=LIB_DIR)
else:
    oracledb.enable_thin_mode()


conn=oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)

cursor = conn.cursor()



#Copy this for all tables

#user data
user_data = pd.read_csv("data/user.csv")
user_sql = "INSERT INTO User_ (user_id, username, email, account_created_date, follower_count) VALUES (:1, :2, :3, :4, :5)"
for (user_id, username, email, acc_creation_date, follower_count) in user_data.itertuples(index=False):
    cursor.execute(user_sql, [user_id, username, email, acc_creation_date, follower_count])

#user profile
user_profile = pd.read_csv("data/userprofile.csv")
user_profile_sql = "INSERT INTO user_profile (user_id, bio, profile_picture, URL_, Verified_Status) VALUES (:1, :2, :3, :4, :5)"
for (user_id, bio, profile_picture, url_, verified_status) in user_profile.itertuples(index=False, name=None):
    cursor.execute(user_profile_sql, [user_id, bio, profile_picture, url_, verified_status])

#tweets

tweets = pd.read_csv("data/tweets.csv")
tweets_sql = "INSERT INTO tweet (tweet_id, content, posted_at, language_, retweet_count, flag, user_id) VALUES (:1, :2, :3, :4, :5, :6, :7)"
for (tweet_id, content, posted_at, language, retweet_count, flag, user_id) in tweets.itertuples(index=False, name=None):
    cursor.execute(tweets_sql, [tweet_id, content, posted_at, language, retweet_count, flag, user_id])

#hashtags
hashtag = pd.read_csv("data/hashtag.csv")
hashtag = hashtag.fillna('')  
hashtag_sql = "INSERT INTO hashtag (tag_id, tag_text, first_seen) VALUES (:1, :2, :3)"
for (tag_id, tag_text, first_seen) in hashtag.itertuples(index=False, name=None):
    cursor.execute(hashtag_sql, [tag_id, tag_text, first_seen])

#tweet_tag
tweet_tag = pd.read_csv("data/tweet_tag.csv")
tweett_sql = "INSERT INTO tweet_tag (tweet_id, tag_id, position_in_tweet) VALUES (:1, :2, :3)"
for (tweet_id, tag_id, position_in_tweet) in tweet_tag.itertuples(index=False, name=None):
    cursor.execute(tweett_sql, [tweet_id, tag_id, position_in_tweet])
#sentiment_category
sentiment_category = pd.read_csv("data/sentiment_category.csv")
sentimentsql_category = "INSERT INTO sentiment_category (category_id, label, description_) VALUES (:1, :2, :3)"
for (category_id, label, description_) in sentiment_category.itertuples(index=False, name=None):
    cursor.execute(sentimentsql_category, [category_id, label, description_])
#sentiment_score
sentiment_score = pd.read_csv("data/sentiment_score.csv")
sentimentsql_score = "INSERT INTO sentiment_score (score_id, tweet_id, score_value, model_used, analyzed_at, confidence, category_id) VALUES (:1,:2,:3,:4,:5,:6,:7)"
for (score_id, tweet_id, score_value, model_used, analyzed_at, confidence, category_id) in sentiment_score.itertuples(index=False, name=None):
    cursor.execute(sentimentsql_score, [score_id, tweet_id, score_value, model_used, analyzed_at, confidence, category_id])



# Fetch tables from DB and write results
user_db = fetch_data("user_")
user_db.to_csv("results/user.csv", index=False)

user_profile_db = fetch_data("user_profile")
user_profile_db.to_csv("results/userprofile.csv", index=False)

tweets_db = fetch_data("tweet")
tweets_db.to_csv("results/tweet.csv", index=False)

tweet_tag_db = fetch_data("tweet_tag")
tweet_tag_db.to_csv("results/tweet_tag.csv", index=False)

hashtag_db = fetch_data("hashtag")
hashtag_db.to_csv("results/hashtag.csv", index=False)

sentiment_category_db = fetch_data("sentiment_category")
sentiment_category_db.to_csv("results/sentiment_category.csv", index=False)

sentiment_score_db = fetch_data("sentiment_score")
sentiment_score_db.to_csv("results/sentiment_score.csv", index=False)

cursor.close()
conn.close()