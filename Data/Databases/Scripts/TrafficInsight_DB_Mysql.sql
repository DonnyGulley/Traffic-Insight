-- Create database
CREATE DATABASE TrafficInsight;
USE TrafficInsight;

-- Create Bookmarks table
CREATE TABLE Bookmarks (
    BookmarkId INT AUTO_INCREMENT PRIMARY KEY,
    UserId INT NOT NULL,
    Route VARCHAR(50) NOT NULL,
    DateAdded DATETIME NOT NULL
);

-- Create Notifications table
CREATE TABLE Notifications (
    NotificationId INT AUTO_INCREMENT PRIMARY KEY,
    UserId INT NOT NULL,
    Message TEXT NOT NULL,
    DateAdded DATETIME NOT NULL,
    FOREIGN KEY (UserId) REFERENCES User(UserId) ON DELETE CASCADE
);

-- Create Roles table
CREATE TABLE Roles (
    RoleId INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(60) NOT NULL,
    Description TEXT NOT NULL
);

-- Create SearchHistory table
CREATE TABLE SearchHistory (
    SearchHistoryId INT AUTO_INCREMENT PRIMARY KEY,
    UserId INT NOT NULL,
    FOREIGN KEY (UserId) REFERENCES User(UserId)
);

-- Create TrafficCollision table
CREATE TABLE TrafficCollision (
    TrafficCollisionId INT AUTO_INCREMENT PRIMARY KEY,
    AccidentDate DATETIME NOT NULL,
    COLLISIONTYPEID INT NOT NULL,
    INITIALIMPACTTYPEID INT NOT NULL,
    ACCIDENT_MONTH INT NOT NULL,
    Accident_Day INT NOT NULL,
    `Accident year` INT NOT NULL
);

-- Create TrafficCollisionCategorys table
CREATE TABLE TrafficCollisionCategorys (
    TrafficCollisionCategoryId INT AUTO_INCREMENT PRIMARY KEY
);

-- Create User table
CREATE TABLE User (
    UserId INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password BINARY(256) NOT NULL,
    email VARCHAR(100) NOT NULL,
    Consent BIT,
    RoleTypeId INT,
    SecurityQuestion VARCHAR(255),
    SecurityAnswer VARCHAR(255),
    FOREIGN KEY (RoleTypeId) REFERENCES Roles(RoleId)
);

-- Insert default admin user
INSERT INTO User (username, password, email, Consent, RoleTypeId, SecurityQuestion, SecurityAnswer)
VALUES ('admin', CONVERT(BINARY(256), 'password'), 'admin@example.com', 1, 1, 'adminkey', '1234');

-- Create SurveyResponses table
CREATE TABLE SurveyResponses (
    SurveyResponseId INT AUTO_INCREMENT PRIMARY KEY,
    UserId INT NOT NULL,
    Question VARCHAR(255) NOT NULL,
    Answer VARCHAR(255) NOT NULL,
    DateSubmitted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserId) REFERENCES User(UserId) ON DELETE CASCADE
);
