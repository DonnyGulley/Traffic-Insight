from Data.data_access_layer import DataAccessLayer
from Visualization.TrafficCollision import Visualization

dal = DataAccessLayer

class BusinessAccessLayer:
    def __init__(self):
        pass

    def plot_accidents_by_collisionDate(self, start_date, end_date):
        self.dal = DataAccessLayer("lp-windows11\DGSQL","TrafficInsight_ETL")
        data = self.dal.get_accident_data()
        visualization = Visualization()
        visualization.PlotAccidentsbyCollisionDate(data, start_date, end_date)

    def plot_accidents_by_impact_type(self, impact_type, impact_type_name):
        self.dal = DataAccessLayer("lp-windows11\DGSQL","TrafficInsight_ETL")
        data =  self.dal.get_accident_data()
        visualization = Visualization()
        visualization.PlotAccidentsbyImpactType(data, impact_type,impact_type_name)

    def plot_accidents_by_road_jurisdiction(self):
        self.dal = DataAccessLayer("lp-windows11\DGSQL","TrafficInsight_ETL")
        data =  self.dal.get_accident_data()
        visualization = Visualization()
        visualization.PlotAccidentsbyRoadJurisdiction(data)
    
    def plot_accidents_by_traffic_condition(self):
        self.dal = DataAccessLayer("lp-windows11\DGSQL","TrafficInsight_ETL")
        data =  self.dal.get_accident_data()
        visualization = Visualization()
        visualization.PlotAccidentsbyTrafficControlCondition(data)

    def create_dashboard(self):
        self.dal = DataAccessLayer("lp-windows11\DGSQL","TrafficInsight_ETL")
        data =  self.dal.get_accident_data()
        visualization = Visualization()
        visualization.create_dashboard(data)