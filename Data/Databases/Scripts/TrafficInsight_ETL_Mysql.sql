CREATE DATABASE `TrafficInsight_ETL`;

USE `TrafficInsight_ETL`;

CREATE TABLE `AccidentDetails` (
    `OBJECTID` INT NOT NULL,
    `AccidentNumber` VARCHAR(50) NULL,
    `AccidentDate` DATETIME NULL,
    `AccidentYear` INT NULL,
    `AccidentMonth` INT NULL,
    `AccidentDay` INT NULL,
    `AccidentHour` INT NULL,
    `AccidentMinute` INT NULL,
    `AccidentSecond` INT NULL,
    `AccidentWeekday` VARCHAR(50) NULL,
    `XCoordinate` FLOAT NULL,
    `YCoordinate` FLOAT NULL,
    `Longitude` FLOAT NULL,
    `Latitude` FLOAT NULL,
    `AccidentLocation` VARCHAR(255) NULL,
    `CollisionTypeID` INT NULL,
    `ClassificationofAccidentID` INT NULL,
    `ImpactLocationID` INT NULL,
    `InitialDirectionOfTravelOne` VARCHAR(50) NULL,
    `InitialDirectionOfTravelTwo` VARCHAR(50) NULL,
    `InitialImpactType` VARCHAR(50) NULL,
    `IntTrafficControl` VARCHAR(50) NULL,
    `LightID` INT NULL,
    `LightForReport` VARCHAR(50) NULL,
    `RoadJurisdiction` VARCHAR(50) NULL,
    `TrafficControlID` INT NULL,
    `TrafficControlCondition` VARCHAR(50) NULL,
    `ThruLaneNo` INT NULL,
    `NorthboundDisobeyCount` INT NULL,
    `SouthboundDisobeyCount` INT NULL,
    `PedestrianInvolved` BIT NULL,
    `CyclistInvolved` BIT NULL,
    `MotorcyclistInvolved` BIT NULL,
    `EnvironmentCondition1` VARCHAR(50) NULL,
    `SelfReported` BIT NULL,
    `XmlImportNotes` VARCHAR(255) NULL,
    `LastEditedDate` DATETIME NULL,
    PRIMARY KEY (`OBJECTID`)
);

CREATE TABLE `ClassificationofAccident` (
    `ClassificationofAccidentID` INT AUTO_INCREMENT NOT NULL,
    `ClassificationofAccident` VARCHAR(50) NULL,
    PRIMARY KEY (`ClassificationofAccidentID`)
);

CREATE TABLE `CollisionTypes` (
    `CollisionTypeID` INT AUTO_INCREMENT NOT NULL,
    `CollisionType` VARCHAR(50) NULL,
    PRIMARY KEY (`CollisionTypeID`)
);

CREATE TABLE `ImpactLocations` (
    `ImpactLocationID` INT AUTO_INCREMENT NOT NULL,
    `ImpactLocation` VARCHAR(50) NULL,
    PRIMARY KEY (`ImpactLocationID`)
);

CREATE TABLE `LightConditions` (
    `LightID` INT AUTO_INCREMENT NOT NULL,
    `Light` VARCHAR(50) NULL,
    PRIMARY KEY (`LightID`)
);

CREATE TABLE `TrafficControls` (
    `TrafficControlID` INT AUTO_INCREMENT NOT NULL,
    `TrafficControl` VARCHAR(50) NULL,
    PRIMARY KEY (`TrafficControlID`)
);

ALTER TABLE `AccidentDetails` 
    ADD CONSTRAINT `FK_AccidentDetails_Classifications` 
    FOREIGN KEY (`ClassificationofAccidentID`) 
    REFERENCES `ClassificationofAccident` (`ClassificationofAccidentID`);

ALTER TABLE `AccidentDetails` 
    ADD CONSTRAINT `FK_AccidentDetails_CollisionTypes` 
    FOREIGN KEY (`CollisionTypeID`) 
    REFERENCES `CollisionTypes` (`CollisionTypeID`);

ALTER TABLE `AccidentDetails` 
    ADD CONSTRAINT `FK_AccidentDetails_ImpactLocations` 
    FOREIGN KEY (`ImpactLocationID`) 
    REFERENCES `ImpactLocations` (`ImpactLocationID`);

ALTER TABLE `AccidentDetails` 
    ADD CONSTRAINT `FK_AccidentDetails_LightConditions1` 
    FOREIGN KEY (`LightID`) 
    REFERENCES `LightConditions` (`LightID`);

ALTER TABLE `AccidentDetails` 
    ADD CONSTRAINT `FK_AccidentDetails_TrafficControls` 
    FOREIGN KEY (`TrafficControlID`) 
    REFERENCES `TrafficControls` (`TrafficControlID`);
