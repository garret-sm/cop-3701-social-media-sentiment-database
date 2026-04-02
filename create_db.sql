--user: myuser
--password: mypassword


create table User_(
    user_id number PRIMARY KEY,
    username varchar(30),
    email varchar(60),    
    account_created_date varchar(100), 
    follower_count number
);

create table user_profile(
    user_id number,
    Bio varchar(200),
    Profile_Picture varchar(60),
    URL_ varchar(50),
    Verified_Status number,
    CONSTRAINT fk_User
    FOREIGN KEY (user_id) REFERENCES User_(user_id)
);

create table tweet(
    tweet_ID number PRIMARY KEY,
    content varchar(500),
    posted_at varchar(100),
    language_ varchar(40),
    retweet_count number,
    flag varchar(20),
    user_id number,
    CONSTRAINT fk_User1
    FOREIGN KEY (user_id)
    REFERENCES User_(user_id)
);


create table hashtag(
    tag_id number PRIMARY KEY,
    tag_text varchar(250),
    first_seen varchar(250)
);

create table tweet_tag(
    tweet_ID number,
    tag_id number,
    position_in_tweet number,
    CONSTRAINT fktweet
    FOREIGN KEY (tweet_ID)
    REFERENCES tweet(tweet_ID),
    CONSTRAINT fktag
    FOREIGN KEY (tag_id)
    REFERENCES hashtag(tag_id)
);

CREATE TABLE sentiment_category (
    category_id NUMBER PRIMARY KEY,
    label VARCHAR(40),
    description_ VARCHAR(200)
);

CREATE TABLE sentiment_score (
    score_id NUMBER PRIMARY KEY,
    tweet_id NUMBER REFERENCES tweet(tweet_id),
    score_value NUMBER,
    model_used VARCHAR(20),
    analyzed_at VARCHAR(60),
    confidence NUMBER,
    category_id NUMBER REFERENCES sentiment_category(category_id)
);