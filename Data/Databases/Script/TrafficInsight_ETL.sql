CREATE DATABASE [TrafficInsight_ETL]
GO

USE [TrafficInsight_ETL]
GO
/****** Object:  Table [dbo].[AccidentDetails]    Script Date: 2024-11-28 9:29:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[AccidentDetails](
	[OBJECTID] [int] NOT NULL,
	[AccidentNumber] [varchar](50) NULL,
	[AccidentDate] [datetime] NULL,
	[AccidentYear] [int] NULL,
	[AccidentMonth] [int] NULL,
	[AccidentDay] [int] NULL,
	[AccidentHour] [int] NULL,
	[AccidentMinute] [int] NULL,
	[AccidentSecond] [int] NULL,
	[AccidentWeekday] [varchar](50) NULL,
	[XCoordinate] [float] NULL,
	[YCoordinate] [float] NULL,
	[Longitude] [float] NULL,
	[Latitude] [float] NULL,
	[AccidentLocation] [varchar](255) NULL,
	[CollisionTypeID] [int] NULL,
	[ClassificationofAccidentID] [int] NULL,
	[ImpactLocationID] [int] NULL,
	[InitialDirectionOfTravelOne] [varchar](50) NULL,
	[InitialDirectionOfTravelTwo] [varchar](50) NULL,
	[InitialImpactType] [varchar](50) NULL,
	[IntTrafficControl] [varchar](50) NULL,
	[LightID] [int] NULL,
	[LightForReport] [varchar](50) NULL,
	[RoadJurisdiction] [varchar](50) NULL,
	[TrafficControlID] [int] NULL,
	[TrafficControlCondition] [varchar](50) NULL,
	[ThruLaneNo] [int] NULL,
	[NorthboundDisobeyCount] [int] NULL,
	[SouthboundDisobeyCount] [int] NULL,
	[PedestrianInvolved] [bit] NULL,
	[CyclistInvolved] [bit] NULL,
	[MotorcyclistInvolved] [bit] NULL,
	[EnvironmentCondition1] [varchar](50) NULL,
	[SelfReported] [bit] NULL,
	[XmlImportNotes] [varchar](255) NULL,
	[LastEditedDate] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[OBJECTID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ClassificationofAccident]    Script Date: 2024-11-28 9:29:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ClassificationofAccident](
	[ClassificationofAccidentID] [int] IDENTITY(1,1) NOT NULL,
	[ClassificationofAccident] [varchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[ClassificationofAccidentID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CollisionTypes]    Script Date: 2024-11-28 9:29:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CollisionTypes](
	[CollisionTypeID] [int] IDENTITY(1,1) NOT NULL,
	[CollisionType] [varchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[CollisionTypeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ImpactLocations]    Script Date: 2024-11-28 9:29:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ImpactLocations](
	[ImpactLocationID] [int] IDENTITY(1,1) NOT NULL,
	[ImpactLocation] [varchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[ImpactLocationID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LightConditions]    Script Date: 2024-11-28 9:29:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LightConditions](
	[LightID] [int] IDENTITY(1,1) NOT NULL,
	[Light] [varchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[LightID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TrafficControls]    Script Date: 2024-11-28 9:29:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TrafficControls](
	[TrafficControlID] [int] IDENTITY(1,1) NOT NULL,
	[TrafficControl] [varchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[TrafficControlID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[AccidentDetails]  WITH CHECK ADD  CONSTRAINT [FK_AccidentDetails_Classifications] FOREIGN KEY([ClassificationofAccidentID])
REFERENCES [dbo].[ClassificationofAccident] ([ClassificationofAccidentID])
GO
ALTER TABLE [dbo].[AccidentDetails] CHECK CONSTRAINT [FK_AccidentDetails_Classifications]
GO
ALTER TABLE [dbo].[AccidentDetails]  WITH CHECK ADD  CONSTRAINT [FK_AccidentDetails_CollisionTypes] FOREIGN KEY([CollisionTypeID])
REFERENCES [dbo].[CollisionTypes] ([CollisionTypeID])
GO
ALTER TABLE [dbo].[AccidentDetails] CHECK CONSTRAINT [FK_AccidentDetails_CollisionTypes]
GO
ALTER TABLE [dbo].[AccidentDetails]  WITH CHECK ADD  CONSTRAINT [FK_AccidentDetails_ImpactLocations] FOREIGN KEY([ImpactLocationID])
REFERENCES [dbo].[ImpactLocations] ([ImpactLocationID])
GO
ALTER TABLE [dbo].[AccidentDetails] CHECK CONSTRAINT [FK_AccidentDetails_ImpactLocations]
GO
ALTER TABLE [dbo].[AccidentDetails]  WITH CHECK ADD  CONSTRAINT [FK_AccidentDetails_LightConditions1] FOREIGN KEY([LightID])
REFERENCES [dbo].[LightConditions] ([LightID])
GO
ALTER TABLE [dbo].[AccidentDetails] CHECK CONSTRAINT [FK_AccidentDetails_LightConditions1]
GO
ALTER TABLE [dbo].[AccidentDetails]  WITH CHECK ADD  CONSTRAINT [FK_AccidentDetails_TrafficControls] FOREIGN KEY([TrafficControlID])
REFERENCES [dbo].[TrafficControls] ([TrafficControlID])
GO
ALTER TABLE [dbo].[AccidentDetails] CHECK CONSTRAINT [FK_AccidentDetails_TrafficControls]
GO
