from Data.data_access_layer import DataAccessLayer
from Data.TrafficData.TrafficInsight_ETL_CRUD import TrafficInsight_ETL_CRUD
from Visualization.TrafficCollision import Visualization
import os


class BusinessAccessLayer:
    def __init__(self):
        # server = os.getenv("DB_SERVER", "OBIORA\\INSTANCE_ONE_SQL")
        # self.dal = DataAccessLayer(server=server, database=database)
        server = os.getenv("DB_SERVER", "lp-windows11\\DGSQL")
        databaseETL = os.getenv("DB_NAME", "TrafficInsight_ETL")
        databaseTrafficInsight = os.getenv("DB_NAME", "TrafficInsight")

        self.dalTrafficInsight = DataAccessLayer(server=server, database=databaseTrafficInsight)
        self.dalETL = TrafficInsight_ETL_CRUD(server=server, database=databaseETL)
    def get_activity_logs(self):
        return self.dalTrafficInsight.get_activity_logs()


    def plot_accidents_by_collisionDate(self, start_date, end_date):
        
        data = self.dalETL.get_accident_data()
        visualization = Visualization()
        visualization.PlotAccidentsbyCollisionDate(data, start_date, end_date)
        
        # Log this activity
        log_details = f"Start Date: {start_date}, End Date: {end_date}, Records: {len(data)}"
        self.dalTrafficInsight.log_activity("Plot Accidents by Collision Date", log_details)


    def plot_accidents_by_impact_type(self, impact_type, impact_type_name):
        # self.dal = DataAccessLayer("lp-windows11\DGSQL","TrafficInsight_ETL")
        data =  self.dalETL.get_accident_data()
        visualization = Visualization()
        visualization.PlotAccidentsbyImpactType(data, impact_type,impact_type_name)
        
        # Log this activity
        log_details = f"Impact Type: {impact_type_name} ({impact_type}), Records: {len(data)}"
        self.dalTrafficInsight.log_activity("Plot Accidents by Impact Type", log_details)


    def plot_accidents_by_road_jurisdiction(self):
        # self.dal = DataAccessLayer("lp-windows11\DGSQL","TrafficInsight_ETL")
        data =  self.dalETL.get_accident_data()
        visualization = Visualization()
        visualization.PlotAccidentsbyRoadJurisdiction(data)
        
        # Log this activity
        log_details = f"Records: {len(data)}"
        self.dalTrafficInsight.log_activity("Plot Accidents by Road Jurisdiction", log_details)

    
    def plot_accidents_by_traffic_condition(self):
        # self.dal = DataAccessLayer("lp-windows11\DGSQL","TrafficInsight_ETL")
        data =  self.dalETL.get_accident_data()
        visualization = Visualization()
        visualization.PlotAccidentsbyTrafficControlCondition(data)
        
        # Log this activity
        log_details = f"Records: {len(data)}"
        self.dalTrafficInsight.log_activity("Plot Accidents by Traffic Condition", log_details)


    def create_dashboard(self):
        # self.dal = DataAccessLayer("lp-windows11\DGSQL","TrafficInsight_ETL")
        data =  self.dalETL.get_accident_data()
        visualization = Visualization()
        visualization.create_dashboard(data)
        
        # Log this activity
        log_details = f"Records: {len(data)}"
        self.dalTrafficInsight.log_activity("Create Dashboard", log_details)
                
    def add_feedback(self, user_id, content, db):
        """
        Adds feedback by delegating to the data access layer.
        """
        return self.dalTrafficInsight.add_feedback(user_id, content, db)

    def update_feedback(self, feedback_id, new_content, db):
        """
        Updates feedback by delegating to the data access layer.
        """
        return self.dalTrafficInsight.update_feedback(feedback_id, new_content, db)

    def search_feedback(self, user_id, db):
        """
        Searches feedback by delegating to the data access layer.
        """
        return self.dalTrafficInsight.search_feedback(user_id, db)
