USE [TrafficInsight]
GO
/****** Object:  Table [dbo].[Bookmarks]    Script Date: 2024-11-21 5:26:07 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Bookmarks](
	[BookmarkId] [int] IDENTITY(1,1) NOT NULL,
	[UserId] [int] NOT NULL,
	[Route] [varchar](50) NOT NULL,
	[DateAdded] [datetime] NOT NULL,
CONSTRAINT [PK_Bookmarks] PRIMARY KEY CLUSTERED 
(
	[BookmarkId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Notifications]    Script Date: 2024-11-21 5:26:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Notifications](
	[NotificationId] [int] IDENTITY(1,1) NOT NULL,
	[UserId] [int] NOT NULL,
	[Message] [text] NOT NULL,
	[DateAdded] [datetime] NOT NULL,
CONSTRAINT [PK_Notifications] PRIMARY KEY CLUSTERED 
(
	[NotificationId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE dbo.Notifications
DROP CONSTRAINT FK_Notifications_User;

ALTER TABLE dbo.Notifications
ADD CONSTRAINT FK_Notifications_User
FOREIGN KEY (UserId) REFERENCES dbo.[User](UserId)
ON DELETE CASCADE;
GO
/****** Object:  Table [dbo].[Roles]    Script Date: 2024-11-21 5:26:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Roles](
	[RoleId] [int] IDENTITY(1,1) NOT NULL,
	[Name] [varchar](60) NOT NULL,
	[Description] [text] NOT NULL,
CONSTRAINT [PK_Roles] PRIMARY KEY CLUSTERED 
(
	[RoleId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SearchHistory]    Script Date: 2024-11-21 5:26:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SearchHistory](
	[SearchHistoryId] [int] IDENTITY(1,1) NOT NULL,
	[UserId] [int] NOT NULL,
CONSTRAINT [PK_SearchHistory] PRIMARY KEY CLUSTERED 
(
	[SearchHistoryId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TrafficCollision]    Script Date: 2024-11-21 5:26:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TrafficCollision](
	[TrafficCollisionId] [int] IDENTITY(1,1) NOT NULL,
	[AccidentDate] [datetime] NOT NULL,
	[COLLISIONTYPEID] [int] NOT NULL,
	[INITIALIMPACTTYPEID] [int] NOT NULL,
	[ACCIDENT_MONTH] [int] NOT NULL,
	[Accident_Day] [int] NOT NULL,
	[Accident year] [int] NOT NULL,
CONSTRAINT [PK_TrafficCollision] PRIMARY KEY CLUSTERED 
(
	[TrafficCollisionId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TrafficCollisionCategorys]    Script Date: 2024-11-21 5:26:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TrafficCollisionCategorys](
	[TrafficCollisionCategoryId] [int] IDENTITY(1,1) NOT NULL,
CONSTRAINT [PK_TrafficCollisionCategorys] PRIMARY KEY CLUSTERED 
(
	[TrafficCollisionCategoryId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[User]    Script Date: 2024-11-21 5:26:08 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[User](
	[UserId] [int] IDENTITY(1,1) NOT NULL,
	[username] [varchar](50) NOT NULL,
	[password] [binary](256) NOT NULL,
	[email] [varchar](100) NOT NULL,
	[Consent] [bit] NULL,
	[RoleTypeId] [int] NULL,
CONSTRAINT [PK_User] PRIMARY KEY CLUSTERED 
(
	[UserId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Bookmarks]  WITH CHECK ADD  CONSTRAINT [FK_Bookmarks_User] FOREIGN KEY([UserId])
REFERENCES [dbo].[User] ([UserId])
GO
ALTER TABLE [dbo].[Bookmarks] CHECK CONSTRAINT [FK_Bookmarks_User]
GO
ALTER TABLE [dbo].[Notifications]  WITH CHECK ADD  CONSTRAINT [FK_Notifications_User] FOREIGN KEY([UserId])
REFERENCES [dbo].[User] ([UserId])
GO
ALTER TABLE [dbo].[Notifications] CHECK CONSTRAINT [FK_Notifications_User]
GO
ALTER TABLE [dbo].[SearchHistory]  WITH CHECK ADD  CONSTRAINT [FK_SearchHistory_User] FOREIGN KEY([UserId])
REFERENCES [dbo].[User] ([UserId])
GO
ALTER TABLE [dbo].[SearchHistory] CHECK CONSTRAINT [FK_SearchHistory_User]
GO
ALTER TABLE [dbo].[User]  WITH CHECK ADD  CONSTRAINT [FK_User_Roles] FOREIGN KEY([RoleTypeId])
REFERENCES [dbo].[Roles] ([RoleId])
GO
ALTER TABLE [dbo].[User] CHECK CONSTRAINT [FK_User_Roles]
GO



ALTER TABLE [User]
ADD SecurityQuestion VARCHAR(255), SecurityAnswer VARCHAR(255);
GO
-- Insert default admin user
INSERT INTO [dbo].[User] 
    ([username], [password], [email], [Consent], [RoleTypeId], [SecurityQuestion], [SecurityAnswer])
VALUES 
    ('admin', 
    CONVERT(binary(256), 'password'), 
    'admin@example.com', 
    1,  -- Consent (1 for yes, 0 for no)
    1,  -- RoleTypeId (1 could represent Admin, adjust as needed based on your RoleType table)
    'adminkey', 
    '1234');
GO


CREATE TABLE [dbo].[SurveyResponses] (
    [SurveyResponseId] INT IDENTITY(1,1) PRIMARY KEY,  -- Auto-incrementing ID
    [UserId] INT NOT NULL,                             -- Foreign key to the User table
    [Question] VARCHAR(255) NOT NULL,                  -- Survey question
    [Answer] VARCHAR(255) NOT NULL,                    -- User's answer
    [DateSubmitted] DATETIME NOT NULL DEFAULT GETDATE(), -- Date and time of submission
    CONSTRAINT FK_SurveyResponses_User FOREIGN KEY ([UserId]) REFERENCES [dbo].[User]([UserId]) ON DELETE CASCADE  -- Foreign key constraint
);
GO

