from TrafficAccident.Traffic_Collisions_Historic_by_AccidentDate_Bars import AccidentDate


#data layer - database - fiels -services
class DataAccessLayer:
    def __init__(self):
        pass


    def __del__(self):
        pass


    def create_connection(self):
        pass

    ### plotting functions   
    def PlotAccidentsbyImpactType(self):
        AccidentDate.Plot()       
