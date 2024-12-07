-- Create database
CREATE DATABASE TrafficInsight_Tweets;
GO

-- Use the database
USE TrafficInsight_Tweets;
GO



-- Create table for tweets
CREATE TABLE Tweets (
    TweetID BIGINT PRIMARY KEY,
    TweetText NVARCHAR(280),
    CreatedAt DATETIME,
    City NVARCHAR(100)
);
GO

-- Create table for hashtags
CREATE TABLE Hashtags (
    HashtagID INT IDENTITY(1,1) PRIMARY KEY,
    TweetID BIGINT,
    Hashtag NVARCHAR(100),
    FOREIGN KEY (TweetID) REFERENCES Tweets(TweetID)
);
GO
