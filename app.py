import streamlit as st
import oracledb
import pandas as pd
from getpass import getpass
from dataload import load_data
import random


# Project Goals:
# 1 - Top tweets in range ranked by retweet_count
# 2 - Find count of tweets with a given hashtag
# 3 - Find average sentiment score of a tweet
#     Random tweet button
# 5 - Get username and bio from email



LIB_DIR = r"C:\oracle\instantclient_11_2"  # Your Instant Client Path
DB_DSN  = "localhost:1521/xe"
if "db_user" not in st.session_state:
    st.session_state["db_user"] = input("User (likely system): ")
if "db_pass" not in st.session_state:
    st.session_state["db_pass"] = getpass("Password: ")

# Initialize Thick Mode (Required for FreeSQL/Cloud)
if LIB_DIR:
    oracledb.init_oracle_client(lib_dir=LIB_DIR)
else:
    oracledb.enable_thin_mode()


if "conn" not in st.session_state:
    st.session_state["conn"] = oracledb.connect(user=st.session_state["db_user"], password=st.session_state["db_pass"], dsn=DB_DSN)

if "cursor" not in st.session_state:
    st.session_state["cursor"] = st.session_state["conn"].cursor()

if "data_loaded" not in st.session_state or not st.session_state["data_loaded"]:
    print("Loading Data")
    load_data(st.session_state["cursor"])
    print("Data Loaded")
    st.session_state["data_loaded"] = True


st.header("Tweet Analyzer")

# 1 - Top tweets in range ranked by retweet_count
with st.expander("Tweet Ranker"):
    st.write("Top X to Y tweets by retweet")
    highest_tweet = st.number_input("Highest Ranking", min_value=1) or -1
    lowest_tweet = st.number_input("Lowest Ranking", min_value=2) or -1
    if st.button("Find Top Tweets"):
        if highest_tweet != -1 and lowest_tweet != -1 and lowest_tweet >= highest_tweet:
            st.dataframe(pd.read_sql_query(\
                "SELECT ranking, retweet_count, content, posted_at "\
                "FROM (SELECT RANK() OVER (ORDER BY retweet_count DESC) AS ranking, "\
                    "retweet_count, content, posted_at "
                    "FROM Tweet) "\
                f"WHERE ranking BETWEEN {highest_tweet} AND {lowest_tweet}",\
                st.session_state["conn"]), hide_index=True)
        else:
            st.warning("Invalid range!")


# 2 - Find count of tweets with a given hashtag
with st.expander("Hashtag Usage Counter"):
    st.write("Amount of tweet tags with a given hashtag")
    desired_tag = st.text_input("Desired hashtag") or ""
    desired_tag = desired_tag.replace("#", "").strip()
    if desired_tag != "":
        tag_count = len(pd.read_sql_query(\
            "SELECT tw.tweet_id FROM "\
            "Hashtag h JOIN Tweet_Tag tt "\
            "ON h.tag_id = tt.tag_id "\
            "JOIN Tweet tw "\
            "ON tt.tweet_id = tw.tweet_id "\
            "WHERE h.tag_text = :1",\
            st.session_state["conn"], params=[desired_tag]))
            
        if tag_count == 1:
            st.write(f"There is 1 tweet with tag #{desired_tag}")
        else:
            st.write(f"There are {tag_count} tweets with tag #{desired_tag}")


# 3 - Find average sentiment score of a tweet
with st.expander("Sentiment Score Evaluator"):
    st.write("Find average sentiment score of a post")
    tweet_id = st.number_input("Tweet ID", min_value=0) or -1
    if tweet_id != -1:
        avg_sentiment = pd.read_sql_query(\
            "SELECT AVG(s.score_value) AS avg_sentiment "\
            "FROM Tweet t JOIN Sentiment_Score s "\
            "ON t.tweet_id = s.tweet_id AND "\
            "t.tweet_id = :1",\
            st.session_state["conn"], params=[tweet_id])["AVG_SENTIMENT"][0]
        if avg_sentiment is not None:
            st.write(f"The average sentiment of the tweet with ID {tweet_id} is {avg_sentiment}")
        else:
            st.write(f"No sentiment data exists for the tweet with ID {tweet_id}")
        

# 4 - Random tweet button
with st.expander("Random Tweet"):
    if st.button("Find Random Tweet"):
        results_table: pd.DataFrame = pd.read_sql_query(\
            "SELECT tweet_id, content, retweet_count, user_id\n"\
            "FROM Tweet", st.session_state["conn"])
        
        results = results_table.loc[random.randrange(0, len(results_table))]
        st.write(f"Tweet ID: {results["TWEET_ID"]}")
        st.write(f"User ID: {results["USER_ID"]}")
        st.write(f"Retweets: {results["RETWEET_COUNT"]}")
        st.write(f"Content: {results["CONTENT"]}")


# 5 - Get username and bio from email
with st.expander("Info From Email"):
    entered_email = st.text_input("Email").strip().lower()
    if st.button("Find Username and Bio"):
        results_table = pd.read_sql_query(\
            "SELECT u.username, p.bio FROM "\
            "User_ u JOIN User_Profile p "\
            "ON u.user_id = p.user_id "\
            "WHERE u.email = :1",\
            st.session_state["conn"], params=[entered_email])
        
        if len(results_table) == 0:
            st.write(f"No users known have email {entered_email}")
        elif len(results_table) == 1:
            st.write(f"Email: {entered_email}")
            st.write(f"Username: {results_table["USERNAME"][0]}")
            st.write(f"Bio: {results_table["BIO"][0]}")
            
        else:
            st.write(f"Multiple users found with email {entered_email}:")
            for i in range(len(results_table)):
                st.write(f"User: {i + 1}")
                st.write(f"- Email: {entered_email}")
                st.write(f"- Username: {results_table["USERNAME"][0]}")
                st.write(f"- Bio: {results_table["BIO"][0]}")