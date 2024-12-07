from time import sleep
from Business.business_access_layer import BusinessAccessLayer
from Data.data_access_layer import DataAccessLayer

dal = DataAccessLayer()

def check_traffic_incidents(user_location, dal):
    """
    Checks traffic data from the database and sends notifications for nearby incidents.
    """
    # Get traffic data from the database based on user location
    traffic_data = dal.get_traffic_incidents_by_location(user_location)
    
    # If there are incidents in the user's location, prepare notifications
    notifications = []
    for incident in traffic_data:
        notifications.append(f"Notification: {incident['incident_description']}")
    
    return notifications
