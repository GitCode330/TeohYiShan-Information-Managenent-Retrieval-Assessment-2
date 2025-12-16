-- CW2_Database_Setup.sql
-- Run this in Azure Data Studio to set up CW2 schema

-- Create the CW2 schema if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'CW2')
BEGIN
    EXEC('CREATE SCHEMA CW2');
END;
GO

-- 1. Create the USER table in CW2 schema
CREATE TABLE CW2.[USER] (
    OwnerUserID INT NOT NULL PRIMARY KEY,
    UserName NVARCHAR(100) NOT NULL
);
GO

-- 2. Create the TRAIL table in CW2 schema
CREATE TABLE CW2.Trail (
    TrailID INT IDENTITY(1,1) PRIMARY KEY,
    TrailName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500),
    Difficulty NVARCHAR(20) NOT NULL CHECK (Difficulty IN ('Easy', 'Moderate', 'Hard')),
    Length DECIMAL(5,2) NOT NULL CHECK (Length > 0),
    ElevationGain INT NOT NULL CHECK (ElevationGain >= 0),
    OwnerUserID INT NOT NULL,
    CONSTRAINT FK_Trail_User_CW2 FOREIGN KEY (OwnerUserID) REFERENCES CW2.[USER](OwnerUserID)
);
GO

-- 3. Create the FEATURE table in CW2 schema
CREATE TABLE CW2.Feature (
    FeatureID INT IDENTITY(1,1) PRIMARY KEY,
    FeatureName NVARCHAR(50) NOT NULL UNIQUE
);
GO

-- 4. Create the TRAIL_FEATURE link table in CW2 schema
CREATE TABLE CW2.Trail_Feature (
    TrailID INT NOT NULL,
    FeatureID INT NOT NULL,
    CONSTRAINT PK_Trail_Feature_CW2 PRIMARY KEY (TrailID, FeatureID),
    CONSTRAINT FK_Trail_Feature_Trail_CW2 FOREIGN KEY (TrailID) REFERENCES CW2.Trail(TrailID) ON DELETE CASCADE,
    CONSTRAINT FK_Trail_Feature_Feature_CW2 FOREIGN KEY (FeatureID) REFERENCES CW2.Feature(FeatureID)
);
GO

-- 5. Create the TRAIL_AUDIT_LOG table in CW2 schema
CREATE TABLE CW2.TrailAuditLog (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    TrailID INT NOT NULL,
    TrailName NVARCHAR(100) NOT NULL,
    AddedByUserID INT NOT NULL,
    DateAdded DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);
GO

-- Insert Sample Data (same as CW1 but in CW2)
INSERT INTO CW2.[USER] (OwnerUserID, UserName) VALUES
(101, 'Ada Lovelace'),
(102, 'Tim Berners-Lee'),
(103, 'Grace Hopper');
GO

-- Insert Sample Data into TRAIL table
INSERT INTO CW2.Trail (TrailName, Description, Difficulty, Length, ElevationGain, OwnerUserID) VALUES
('Penang Hill Heritage Trail', 'A challenging hike from Temple Road to the summit, passing historical stations and offering rich biodiversity.', 'Hard', 5.0, 691, 101),
('Plymbridge Circular', 'A gentle and scenic walk through ancient woodland and along a river valley.', 'Easy', 3.5, 85, 102),
('Dartmoor Summit Challenge', 'A tough, exposed hike across moorland to the top of a prominent tor.', 'Hard', 8.75, 450, 103);
GO

-- Insert Sample Data into FEATURE table
INSERT INTO CW2.Feature (FeatureName) VALUES
('Forest'),
('River'),
('Wildlife'),
('Historic Site'),
('Stairs'),
('Mountain View'),
('Steep Climb');
GO

-- Insert Sample Data into TRAIL_FEATURE link table
INSERT INTO CW2.Trail_Feature (TrailID, FeatureID) VALUES
(1, 5), -- Penang Hill has 'Stairs'
(1, 6), -- Penang Hill has 'Mountain View'
(1, 7), -- Penang Hill has 'Steep Climb'
(1, 4), -- Penang Hill has 'Historic Site'
(2, 1), -- Plymbridge has 'Forest'
(2, 2), -- Plymbridge has 'River'
(2, 3), -- Plymbridge has 'Wildlife'
(3, 6), -- Dartmoor has 'Mountain View'
(3, 7); -- Dartmoor has 'Steep Climb'
GO
