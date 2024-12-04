-- Create database
CREATE DATABASE `TrafficInsight_Tweets`;

-- Use the database
USE `TrafficInsight_Tweets`;

-- Create table for tweets
CREATE TABLE `Tweets` (
    `TweetID` BIGINT PRIMARY KEY,
    `TweetText` VARCHAR(280),
    `CreatedAt` DATETIME,
    `City` VARCHAR(100)
);

-- Create table for hashtags
CREATE TABLE `Hashtags` (
    `HashtagID` INT AUTO_INCREMENT PRIMARY KEY,
    `TweetID` BIGINT,
    `Hashtag` VARCHAR(100),
    FOREIGN KEY (`TweetID`) REFERENCES `Tweets`(`TweetID`)
);
