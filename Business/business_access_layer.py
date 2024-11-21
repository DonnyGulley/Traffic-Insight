from Data.data_access_layer import DataAccessLayer

dal = DataAccessLayer()
#business layer - pass requests to the data layer
class BusinessAccessLayer:
    
    def __init__(self):
        pass


    def PlotAccidents(self):


        dal.PlotAccidentsbyImpactType()    
    
