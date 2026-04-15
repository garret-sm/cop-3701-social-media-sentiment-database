import streamlit as st
import oracledb
import pandas as pd
from getpass import getpass
from dataload import load_data


# Project Goals:
#     Rank tweets by retweet_count
#     Find count of tweet tags with a given hashtag
#     Find average sentiment score of a tweet
#     Random tweet button
#     Get username and bio from email



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
    load_data(st.session_state["cursor"])
    st.session_state["data_loaded"] = True


# 1 - Top tweets in range ranked by retweet_count:
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


# 2 - Find count of tweet tags with a given hashtag:
with st.expander("Tweet Tag Counter"):
    st.write("Amount of tweet tags with a given hashtag")
    desired_tag = st.text_input("Desired hashtag") or ""
    desired_tag = desired_tag.replace("#", "").strip()
    if desired_tag != "":
        tag_df = pd.read_sql_query("SELECT tag_id FROM Hashtag "\
            "WHERE tag_text = :1", st.session_state["conn"], params=[desired_tag])
        if len(tag_df) > 0:
            tag_id = tag_df["TAG_ID"][0]
            tag_count = len(pd.read_sql_query(\
                "SELECT tag_id FROM Tweet_Tag "\
                f"WHERE tag_id = {tag_id}",\
                st.session_state["conn"]))
            
            if tag_count == 1:
                st.write(f"There is 1 tag with tag #{desired_tag}")
            else:
                st.write(f"There are {tag_count} tags with tag #{desired_tag}")
        else:
            st.warning(f"No posts found with tag #{desired_tag}")


# 3 - Find average sentiment score of a tweet
with st.expander("Sentiment Score Evaluator"):
    st.write("Find average sentiment score of a post")
    tweet_id = st.number_input("Tweet ID", min_value=0) or -1
    if tweet_id != -1:
        pass
        

# 4 - Random tweet button
with st.expander("Random Tweet"):
    if st.button("Find Random Tweet"):
        st.write("Not implemented =p")


# 5 - Get username and bio from email
with st.expander("Info From Email"):
    entered_email = st.text_input("Email")
    if st.button("Find Username and Bio"):
        pass